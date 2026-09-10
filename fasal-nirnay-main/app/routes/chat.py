"""
Chat Routes
===========
Exposes the AI chatbot endpoint.
Combines user query with optional weather/news context,
then passes everything to the chat service for a response.
"""

from fastapi import APIRouter, HTTPException
from app.services.chat_service import get_chat_response
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    Accepts a farmer's question along with context (location, crop, language)
    and returns an AI-generated advisory response.

    If no LLM API key is configured, a structured mock response is returned
    so the endpoint stays testable during development.
    """
    try:
        result = await get_chat_response(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")
