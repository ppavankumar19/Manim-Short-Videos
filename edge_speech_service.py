"""
Edge TTS adapter for Manim Voiceover.

Provides the approved Linux/Windows production voice for Dhimant lessons:
`en-GB-RyanNeural`. This exists because `manim_voiceover` ships no edge-tts
service, and plan.md Section 4.1 forbids gTTS from silently becoming the
production voice.

Environment overrides:
    EDGE_VOICE  default "en-GB-RyanNeural"
    EDGE_RATE   default "+9%"   (the word-budget anchor in plan.md Section 25)
    EDGE_PITCH  default "+0Hz"
"""

from __future__ import annotations

import asyncio
import os
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

try:
    import edge_tts
except ImportError:  # pragma: no cover - surfaced at call time
    edge_tts = None
    logger.error("Missing package. Run `pip install edge-tts` to use EdgeSpeechService.")


DEFAULT_VOICE = "en-IN-PrabhatNeural"
DEFAULT_RATE = "+9%"
DEFAULT_PITCH = "+0Hz"


class EdgeSpeechService(SpeechService):
    """Microsoft Edge neural TTS, rendered through the `edge_tts` package."""

    def __init__(
        self,
        voice: str | None = None,
        rate: str | None = None,
        pitch: str | None = None,
        **kwargs: object,
    ) -> None:
        if edge_tts is None:
            raise ImportError(
                "edge_tts is not installed. Run: .venv/bin/pip install edge-tts"
            )
        initialize_speech_service(self, kwargs)
        self.voice = voice or os.getenv("EDGE_VOICE", DEFAULT_VOICE)
        self.rate = rate or os.getenv("EDGE_RATE", DEFAULT_RATE)
        self.pitch = pitch or os.getenv("EDGE_PITCH", DEFAULT_PITCH)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        """"""
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {
            "input_text": input_text,
            "service": "edge",
            "voice": self.voice,
            "rate": self.rate,
            "pitch": self.pitch,
            # Bump when the payload shape changes so stale caches regenerate.
            "wb_version": 1,
        }

        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is None:
            # Older cache entries were written before `wb_version` existed.
            legacy_input_data = dict(input_data)
            legacy_input_data.pop("wb_version", None)
            cached_result = self.get_cached_result(legacy_input_data, cache_dir)
            if cached_result is not None:
                cached_result["input_data"] = input_data
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path_to_string(path)

        out_file = Path(cache_dir) / audio_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            word_boundaries = asyncio.run(
                self._synthesize(input_text, str(out_file))
            )
        except Exception as exc:  # noqa: BLE001 - re-raised with context
            logger.error(exc)
            raise Exception(
                "edge-tts failed to synthesize narration. You are either not "
                "connected to the internet, or the voice name is invalid: "
                f"{self.voice!r}."
            )

        json_dict: VoiceoverData = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
            "word_boundaries": word_boundaries,
        }

        return json_dict

    async def _synthesize(self, text: str, out_path: str) -> list[dict]:
        """Stream the audio and collect per-word timings.

        edge-tts emits WordBoundary events carrying the audio offset (in
        100 ns ticks) and the spoken word, but no character offset. We
        recover the character offset by scanning `text` forward for each
        word, which is what `VoiceoverTracker` interpolates against to
        resolve `<bookmark mark='...'/>` positions.
        """
        communicate = edge_tts.Communicate(
            text,
            self.voice,
            rate=self.rate,
            pitch=self.pitch,
            # edge-tts defaults to SentenceBoundary; we need per-word ticks.
            boundary="WordBoundary",
        )

        word_boundaries: list[dict] = []
        search_pos = 0
        last_end_offset = 0

        with open(out_path, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    word = chunk["text"]
                    idx = text.find(word, search_pos)
                    if idx == -1:
                        idx = search_pos
                    else:
                        search_pos = idx + len(word)
                    word_boundaries.append(
                        {
                            "audio_offset": chunk["offset"],
                            "text_offset": idx,
                            "word_length": len(word),
                            "text": word,
                            "boundary_type": "Word",
                        }
                    )
                    last_end_offset = chunk["offset"] + chunk.get("duration", 0)

        # Anchor the end of the text so bookmarks near the close interpolate
        # instead of clamping to the last spoken word.
        if word_boundaries and word_boundaries[-1]["text_offset"] < len(text):
            word_boundaries.append(
                {
                    "audio_offset": last_end_offset,
                    "text_offset": len(text),
                    "word_length": 1,
                    "text": "",
                    "boundary_type": "Word",
                }
            )

        return word_boundaries


__all__ = ["EdgeSpeechService", "DEFAULT_VOICE", "DEFAULT_RATE", "DEFAULT_PITCH"]
