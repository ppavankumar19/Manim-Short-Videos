"""
Gemini Zephyr Speech Service for Manim Voiceover.

Synthesizes high-fidelity voice using Google's Gemini 2.5 Flash Preview TTS
with the prebuilt voice 'Zephyr'. Generates 100ns word boundary ticks
for seamless bookmark tracking in Manim VoiceoverScene.
"""

from __future__ import annotations

import os
import re
import json
import wave
import base64
import requests
from pathlib import Path
from manim import logger

from manim_voiceover._typing import VoiceoverData
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import (
    PathLike,
    SpeechService,
    initialize_speech_service,
    path_to_string,
)

DEFAULT_VOICE = "Zephyr"
DEFAULT_MODEL = "gemini-2.5-flash-preview-tts"


class GeminiZephyrSpeechService(SpeechService):
    """Google Gemini TTS service for Manim voiceover using Zephyr voice."""

    def __init__(
        self,
        api_key: str | None = None,
        voice: str | None = None,
        model: str | None = None,
        **kwargs: object,
    ) -> None:
        initialize_speech_service(self, kwargs)
        self.api_key = (api_key or os.getenv("GOOGLE_API_KEY", "")).strip()
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required for GeminiZephyrSpeechService.")
        
        raw_voice = voice or os.getenv("GOOGLE_TTS_VOICE", DEFAULT_VOICE)
        if "zephyr" in raw_voice.lower():
            self.voice = "Zephyr"
        elif "puck" in raw_voice.lower():
            self.voice = "Puck"
        elif "charon" in raw_voice.lower():
            self.voice = "Charon"
        elif "kore" in raw_voice.lower():
            self.voice = "Kore"
        elif "fenrir" in raw_voice.lower():
            self.voice = "Fenrir"
        elif "aoede" in raw_voice.lower():
            self.voice = "Aoede"
        else:
            self.voice = raw_voice

        self.model = model or DEFAULT_MODEL
        logger.info(f"Initialized GeminiZephyrSpeechService (voice={self.voice}, model={self.model})")

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        if cache_dir is None:
            cache_dir = self.cache_dir

        cache_path = Path(cache_dir)
        cache_path.mkdir(parents=True, exist_ok=True)

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "gemini-zephyr",
            "voice": self.voice,
            "model": self.model,
            "version": 1,
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".wav"
        else:
            audio_path = path_to_string(path)

        out_file = cache_path / audio_path

        # Call Gemini TTS API with retry and generous timeout
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": input_text}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": self.voice
                        }
                    }
                }
            }
        }

        import time
        max_retries = 3
        response = None
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                if response.status_code == 200:
                    break
                logger.warning(f"Gemini TTS attempt {attempt} returned {response.status_code}: {response.text[:200]}")
            except Exception as e:
                logger.warning(f"Gemini TTS attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2 * attempt)

        if response is None or response.status_code != 200:
            err = response.text if response is not None else "Timeout / Connection Error"
            raise RuntimeError(f"Gemini TTS request failed: {err}")

        res_json = response.json()
        part = res_json["candidates"][0]["content"]["parts"][0]
        raw_pcm = base64.b64decode(part["inlineData"]["data"])

        # Write 24kHz mono 16-bit WAV
        with wave.open(str(out_file), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(raw_pcm)

        # Measure audio duration
        with wave.open(str(out_file), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration_sec = frames / float(rate)

        # Calculate word boundaries (100ns ticks matching edge-tts specification)
        total_ticks = int(duration_sec * 10_000_000)
        word_boundaries = self._calculate_word_boundaries(input_text, total_ticks)

        json_dict: VoiceoverData = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
            "word_boundaries": word_boundaries,
        }

        return json_dict

    def _calculate_word_boundaries(self, text: str, total_ticks: int) -> list[dict]:
        """Calculates per-word audio offsets based on character distribution and pause weighting."""
        tokens = []
        for m in re.finditer(r"\S+", text):
            word = m.group()
            start = m.start()
            weight = len(word)
            if word[-1] in ".!?":
                weight += 4.0
            elif word[-1] in ",;:":
                weight += 2.0
            tokens.append((word, start, weight))

        if not tokens:
            return []

        total_weight = sum(t[2] for t in tokens)
        word_boundaries = []
        accum_weight = 0.0

        for word, start, weight in tokens:
            offset = int((accum_weight / total_weight) * total_ticks)
            word_boundaries.append({
                "audio_offset": offset,
                "text_offset": start,
                "word_length": len(word),
                "text": word,
                "boundary_type": "Word",
            })
            accum_weight += weight

        word_boundaries.append({
            "audio_offset": total_ticks,
            "text_offset": len(text),
            "word_length": 1,
            "text": "",
            "boundary_type": "Word",
        })

        return word_boundaries


__all__ = ["GeminiZephyrSpeechService", "DEFAULT_VOICE", "DEFAULT_MODEL"]
