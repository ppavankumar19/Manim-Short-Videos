"""
Speech service selector for Dhimant Manim Voiceover animations.

Uses EdgeSpeechService with en-IN-PrabhatNeural (Indian accent) as the
production voice on Linux/Windows. Falls back to macOS `say` or gTTS.
"""

from __future__ import annotations

import os
import platform

from pathlib import Path

from manim import logger


def get_speech_service(
    *, cache_dir: str | os.PathLike[str] | None = None,
    rate: str | None = None,
):
    """Return the appropriate speech service based on OS platform.

    `rate` overrides EDGE_RATE for this call only — used by the video-first
    scenes, where each beat's narration is tuned (via tts_tune.py) to a
    specific edge-tts rate so the spoken duration matches that beat's
    planned animation length.
    """
    system = platform.system()
    cache_dir_str = str(Path(cache_dir)) if cache_dir is not None else None

    # macOS: use Jamie (Premium) via the say command
    if system == "Darwin":
        try:
            from jamie_speech_service import JamieSpeechService
            return JamieSpeechService(
                voice=os.getenv("VOICE", "Jamie (Premium)"),
                rate=int(os.getenv("RATE", "170")),
                cache_dir=cache_dir_str,
            )
        except Exception:
            logger.warning("JamieSpeechService unavailable, trying EdgeSpeechService")

    # Check for Google Gemini Zephyr TTS
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(usecwd=True))

    google_api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    google_voice = os.getenv("GOOGLE_TTS_VOICE", "")
    tts_provider = os.getenv("TTS_PROVIDER", "")
    voice_env = os.getenv("VOICE", "")

    if google_api_key and (
        tts_provider.lower() in ("gemini", "google")
        or "zephyr" in google_voice.lower()
        or "zephyr" in voice_env.lower()
    ):
        try:
            from gemini_speech_service import GeminiZephyrSpeechService
            return GeminiZephyrSpeechService(
                api_key=google_api_key,
                voice=google_voice or "Zephyr",
                cache_dir=cache_dir_str,
            )
        except Exception as exc:
            logger.warning(f"GeminiZephyrSpeechService unavailable ({exc}), falling back to EdgeSpeechService")

    # Linux / Windows: use Edge TTS with Indian English accent
    try:
        from edge_speech_service import EdgeSpeechService
        return EdgeSpeechService(
            voice=os.getenv("EDGE_VOICE", "en-IN-PrabhatNeural"),
            rate=rate or os.getenv("EDGE_RATE", "+9%"),
            pitch=os.getenv("EDGE_PITCH", "+0Hz"),
            cache_dir=cache_dir_str,
        )
    except Exception as exc:
        logger.warning(f"EdgeSpeechService unavailable ({exc}), falling back to gTTS")

    # Last resort fallback
    from manim_voiceover.services.gtts import GTTSService
    logger.warning(
        "Using gTTS fallback. This is NOT the approved production voice. "
        "Install edge-tts for en-IN-PrabhatNeural."
    )
    return GTTSService(lang="en", tld="co.in", cache_dir=cache_dir_str)
