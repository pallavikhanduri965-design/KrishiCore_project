"""
Speech Routes
=============
Placeholder endpoints for Speech-to-Text (STT) and Text-to-Speech (TTS).
Replace mock logic with Google Cloud STT/TTS or BHASHINI later.
"""

from fastapi import APIRouter, HTTPException
from app.services.speech_service import speech_to_text, text_to_speech
from app.models.schemas import STTRequest, STTResponse, TTSRequest, TTSResponse

router = APIRouter()


@router.post("/stt", response_model=STTResponse)
async def stt_endpoint(request: STTRequest):
    """
    Speech-to-Text endpoint.
    Accepts base64-encoded audio and returns the transcribed text.
    Currently returns mock output if no speech provider is configured.
    """
    try:
        result = await speech_to_text(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"STT service error: {str(e)}")


@router.post("/tts", response_model=TTSResponse)
async def tts_endpoint(request: TTSRequest):
    """
    Text-to-Speech endpoint.
    Accepts text and language, returns base64-encoded audio.
    Currently returns mock output if no speech provider is configured.
    """
    try:
        result = await text_to_speech(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS service error: {str(e)}")
