"""
Chat Service
============
Combines farmer query + location + crop + language + optional context
and produces an advisory response.

- If LLM_PROVIDER / OPENAI_API_KEY is missing → returns a structured mock response.
- If configured → placeholder section clearly marked for your LLM integration.

Multilingual note:
  The `language` field is passed through so a future translation step
  (e.g., IndicTrans2 or Google Translate) can wrap the response.
"""

from typing import Any, Dict, Optional
from app.core.config import settings
from app.models.schemas import ChatRequest


# ------------------------------------------------------------------------------
# Mock advisory — returned when no LLM API key is present
# ------------------------------------------------------------------------------
def _build_mock_response(request: ChatRequest) -> Dict[str, Any]:
    """Generates a structured but fake advisory response for development."""
    return {
        "answer": (
            f"[MOCK RESPONSE] Based on current conditions in {request.location}, "
            f"your {request.crop} crop may benefit from the following advisory: "
            "Ensure adequate soil moisture before the next predicted rain. "
            "Monitor for early signs of pest activity given the humid conditions. "
            "Consider applying a light dose of nitrogen fertilizer this week."
        ),
        "language": request.language,
        "context_used": {
            "weather_included": request.include_weather,
            "news_included":    request.include_news,
        },
        "source": "mock",
    }


async def get_chat_response(request: ChatRequest) -> Dict[str, Any]:
    """
    Generates an AI advisory response for a farmer's query.

    Steps:
      1. Optionally fetch weather context.
      2. Optionally fetch news context.
      3. Build a rich prompt.
      4. Call the LLM (or return mock if key is missing).

    Args:
        request: A ChatRequest Pydantic model with query, location, crop, language.

    Returns:
        A dictionary matching the ChatResponse schema.
    """

    # ------------------------------------------------------------------
    # Step 1: Optionally gather weather context
    # ------------------------------------------------------------------
    weather_context: Optional[str] = None
    if request.include_weather:
        try:
            from app.services.weather_service import get_weather_forecast
            wx = await get_weather_forecast(location=request.location, crop=request.crop, days=3)
            weather_context = (
                f"Current weather in {wx['location']}: {wx['condition']}, "
                f"{wx['current_temp_c']}°C, humidity {wx['humidity']}%, "
                f"wind {wx['wind_kph']} kph."
            )
        except Exception:
            weather_context = "Weather data unavailable."

    # ------------------------------------------------------------------
    # Step 2: Optionally gather news context
    # ------------------------------------------------------------------
    news_context: Optional[str] = None
    if request.include_news:
        try:
            from app.services.news_service import get_latest_news
            news_data = await get_latest_news(location=request.location, crop=request.crop)
            headlines = [a["title"] for a in news_data.get("articles", [])[:3]]
            news_context = "Recent news: " + " | ".join(headlines) if headlines else "No recent news."
        except Exception:
            news_context = "News data unavailable."

    # ------------------------------------------------------------------
    # No LLM key configured → return mock response
    # ------------------------------------------------------------------
    if not settings.OPENAI_API_KEY:
        return _build_mock_response(request)

    # ------------------------------------------------------------------
    # Step 3: Build the prompt
    # ------------------------------------------------------------------
    system_prompt = (
        "You are FasalNirnay, an expert agricultural advisor for Indian farmers. "
        "Give concise, practical, and farmer-friendly advice in simple language. "
        f"Respond in {request.language}."
    )

    user_message_parts = [
        f"Farmer's question: {request.farmer_query}",
        f"Location: {request.location}",
        f"Crop: {request.crop}",
    ]
    if weather_context:
        user_message_parts.append(f"Weather context: {weather_context}")
    if news_context:
        user_message_parts.append(f"News context: {news_context}")

    user_message = "\n".join(user_message_parts)

    # ------------------------------------------------------------------
    # Step 4: Call the LLM
    # =====================================================================
    # TODO: Replace this section with your preferred LLM provider.
    #
    # Option A — OpenAI (GPT-4o, GPT-3.5-turbo):
    #   pip install openai
    #   from openai import AsyncOpenAI
    #   client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    #   completion = await client.chat.completions.create(
    #       model="gpt-4o-mini",
    #       messages=[
    #           {"role": "system", "content": system_prompt},
    #           {"role": "user",   "content": user_message},
    #       ],
    #       max_tokens=500,
    #       temperature=0.7,
    #   )
    #   answer = completion.choices[0].message.content
    #
    # Option B — Google Gemini:
    #   pip install google-generativeai
    #   import google.generativeai as genai
    #   genai.configure(api_key=settings.GEMINI_API_KEY)
    #
    # Option C — Anthropic Claude:
    #   pip install anthropic
    #   from anthropic import AsyncAnthropic
    #
    # Option D — Local model via Ollama (no key needed):
    #   POST http://localhost:11434/api/chat
    # =====================================================================

    # --- REMOVE THIS LINE once you plug in a real LLM above ---
    answer = _build_mock_response(request)["answer"] + " [LLM key detected but call not yet wired]"

    return {
        "answer":   answer,
        "language": request.language,
        "context_used": {
            "weather_included": request.include_weather,
            "news_included":    request.include_news,
        },
        "source": settings.LLM_PROVIDER or "mock",
    }
