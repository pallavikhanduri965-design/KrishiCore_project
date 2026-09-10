"""
Speech Service
==============
Placeholder functions for Speech-to-Text and Text-to-Speech.

Current state: Returns mock responses.
Future state:  Replace with Sarvam AI API calls.

Sarvam AI (https://www.sarvam.ai/) is an Indian AI company with
dedicated STT and TTS models for Indic languages including Hindi,
Marathi, Bengali, Tamil, Telugu, Kannada, Gujarati, and more.
It is a great fit for FasalNirnay's farmer-facing use case.

Sarvam API Docs: https://docs.sarvam.ai/
"""

import base64
import httpx
from typing import Any, Dict
from app.core.config import settings
from app.models.schemas import STTRequest, TTSRequest


# ------------------------------------------------------------------------------
# Mock audio — a tiny silent WAV file in base64 (for TTS mock response)
# ------------------------------------------------------------------------------
MOCK_AUDIO_BASE64 = "UklGRiQAAABXQVZFZm10IBAAAA"  # truncated placeholder — not real audio

# ------------------------------------------------------------------------------
# Sarvam API endpoints
# Docs: https://docs.sarvam.ai/
# ------------------------------------------------------------------------------
SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"


async def speech_to_text(request: STTRequest) -> Dict[str, Any]:
    """
    Converts audio to text using Sarvam AI's STT API.

    Args:
        request: STTRequest with base64_audio and language_code.

    Returns:
        Dictionary with transcribed text and confidence score.

    TODO — Steps to activate real Sarvam STT:
    ------------------------------------------
    1. Set SPEECH_PROVIDER=sarvam in your .env file
    2. Set SARVAM_API_KEY=your_key in your .env file
    3. Uncomment the "REAL SARVAM STT CALL" block below
    4. Delete the fallback return at the bottom of this function

    Sarvam STT Docs: https://docs.sarvam.ai/api-reference/speech-to-text
    Supported language codes: hi-IN, mr-IN, bn-IN, ta-IN, te-IN, kn-IN, gu-IN, pa-IN, en-IN
    ------------------------------------------
    """

    # No provider configured → return mock transcript
    if not settings.SPEECH_PROVIDER or settings.SPEECH_PROVIDER == "mock":
        return {
            "transcript": "यह एक परीक्षण संदेश है।",   # "This is a test message." in Hindi
            "confidence": 0.95,
            "language":   request.language_code,
            "source":     "mock",
        }

    # ------------------------------------------------------------------
    # REAL SARVAM STT CALL — uncomment when ready
    # ------------------------------------------------------------------
    # if settings.SPEECH_PROVIDER == "sarvam":
    #     # Decode the base64 audio back to raw bytes
    #     audio_bytes = base64.b64decode(request.base64_audio)
    #
    #     headers = {
    #         "api-subscription-key": settings.SARVAM_API_KEY,
    #     }
    #
    #     # Sarvam STT expects multipart/form-data with the audio file
    #     files = {
    #         "file": (f"audio.{request.audio_format}", audio_bytes, f"audio/{request.audio_format}"),
    #     }
    #     data = {
    #         "language_code": request.language_code,
    #         "model":         "saarika:v2",   # Sarvam's latest STT model
    #     }
    #
    #     async with httpx.AsyncClient(timeout=30.0) as client:
    #         resp = await client.post(SARVAM_STT_URL, headers=headers, files=files, data=data)
    #         resp.raise_for_status()
    #         result = resp.json()
    #
    #     return {
    #         "transcript": result.get("transcript", ""),
    #         "confidence": 1.0,   # Sarvam STT v1 does not return a confidence score
    #         "language":   request.language_code,
    #         "source":     "sarvam",
    #     }

    # Fallback if provider is set but call is not yet uncommented
    return {
        "transcript": f"[STT not yet wired for provider: {settings.SPEECH_PROVIDER}. See TODO in speech_service.py]",
        "confidence": 0.0,
        "language":   request.language_code,
        "source":     settings.SPEECH_PROVIDER,
    }


async def text_to_speech(request: TTSRequest) -> Dict[str, Any]:
    """
    Converts text to audio using Sarvam AI's TTS API.

    Args:
        request: TTSRequest with text, language_code, and optional voice_gender.

    Returns:
        Dictionary with base64-encoded audio and format info.

    TODO — Steps to activate real Sarvam TTS:
    ------------------------------------------
    1. Set SPEECH_PROVIDER=sarvam in your .env file
    2. Set SARVAM_API_KEY=your_key in your .env file
    3. Uncomment the "REAL SARVAM TTS CALL" block below
    4. Delete the fallback return at the bottom of this function

    Sarvam TTS Docs: https://docs.sarvam.ai/api-reference/text-to-speech
    Supported speakers vary by language — see docs for the full list.
    Audio is returned as base64-encoded WAV in the response JSON.
    ------------------------------------------
    """

    # No provider configured → return mock audio
    if not settings.SPEECH_PROVIDER or settings.SPEECH_PROVIDER == "mock":
        return {
            "audio_base64": MOCK_AUDIO_BASE64,
            "format":       "wav",
            "language":     request.language_code,
            "source":       "mock",
        }

    # ------------------------------------------------------------------
    # REAL SARVAM TTS CALL — uncomment when ready
    # ------------------------------------------------------------------
    # if settings.SPEECH_PROVIDER == "sarvam":
    #     headers = {
    #         "api-subscription-key": settings.SARVAM_API_KEY,
    #         "Content-Type": "application/json",
    #     }
    #
    #     # Map voice_gender to a Sarvam speaker name
    #     # Full speaker list: https://docs.sarvam.ai/api-reference/text-to-speech
    #     speaker_map = {
    #         "female": "meera",   # Hindi female — change per language as needed
    #         "male":   "arjun",   # Hindi male
    #     }
    #     speaker = speaker_map.get(request.voice_gender, "meera")
    #
    #     payload = {
    #         "inputs":        [request.text],
    #         "target_language_code": request.language_code,
    #         "speaker":       speaker,
    #         "model":         "bulbul:v2",   # Sarvam's latest TTS model
    #         "enable_preprocessing": True,   # Handles numbers, dates etc. in Indic scripts
    #     }
    #
    #     async with httpx.AsyncClient(timeout=30.0) as client:
    #         resp = await client.post(SARVAM_TTS_URL, headers=headers, json=payload)
    #         resp.raise_for_status()
    #         result = resp.json()
    #
    #     # Sarvam returns a list of base64 audio chunks — join them if needed
    #     audio_b64 = result.get("audios", [""])[0]
    #
    #     return {
    #         "audio_base64": audio_b64,
    #         "format":       "wav",
    #         "language":     request.language_code,
    #         "source":       "sarvam",
    #     }

    # Fallback if provider is set but call is not yet uncommented
    return {
        "audio_base64": f"[TTS not yet wired for provider: {settings.SPEECH_PROVIDER}. See TODO in speech_service.py]",
        "format":       "wav",
        "language":     request.language_code,
        "source":       settings.SPEECH_PROVIDER,
    }
