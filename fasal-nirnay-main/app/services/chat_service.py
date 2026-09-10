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

import httpx
from typing import Any, Dict, Optional
from app.core.config import settings
from app.models.schemas import ChatRequest


# ------------------------------------------------------------------------------
# Mock advisory — returned when neither Gemini nor Ollama is accessible
# ------------------------------------------------------------------------------
def _build_mock_response(request: ChatRequest) -> Dict[str, Any]:
    """Generates a structured fallback advisory response for offline development."""
    return {
        "answer": (
            f"[ADVISORY FALLBACK] Based on current conditions in {request.location}, "
            f"your {request.crop} crop may benefit from the following recommendations: "
            "1. Monitor soil moisture closely and schedule irrigation during early morning hours. "
            "2. Inspect crop foliage regularly for signs of localized pest or fungal stress. "
            "3. Apply recommended nutrient supplements in accordance with local soil health guidelines."
        ),
        "language": request.language,
        "context_used": {
            "weather_included": request.include_weather,
            "news_included":    request.include_news,
        },
        "source": "mock",
    }


async def _call_gemini(prompt: str) -> Optional[str]:
    """Call Google Gemini API via REST endpoint."""
    if not getattr(settings, "GEMINI_API_KEY", None):
        return None

    api_key = settings.GEMINI_API_KEY
    model = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
    except Exception as e:
        print(f"⚠️ Google Gemini call failed ({e}) — falling back to Ollama")

    return None


async def _call_ollama(prompt: str) -> Optional[str]:
    """Call local Ollama instance as fallback LLM."""
    base_url = getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = getattr(settings, "OLLAMA_MODEL", "llama3")
    url = f"{base_url}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": false if False else False,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "").strip()
    except Exception as e:
        print(f"⚠️ Ollama fallback failed or unreachable ({e}) — using mock fallback")

    return None


async def get_chat_response(request: ChatRequest) -> Dict[str, Any]:
    """
    Generates an AI advisory response for a farmer's query.

    Priority Order:
      1. Google Gemini API (if GEMINI_API_KEY is configured).
      2. Ollama Local LLM (if Gemini fails or key is omitted).
      3. Mock Advisory Generator (if both are offline).
    """

    # ------------------------------------------------------------------
    # Step 1: Gather weather context
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
    # Step 2: Gather news context
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
    # Step 3: Build the prompt
    # ------------------------------------------------------------------
    system_prompt = (
        "You are FasalNirnay, an expert agricultural advisory assistant for Indian farmers. "
        "Provide practical, concise, and farmer-friendly advice in simple words. "
        f"Respond in {request.language}."
    )

    user_message_parts = [
        system_prompt,
        f"\nFarmer's Query: {request.farmer_query}",
        f"Location: {request.location}",
        f"Crop: {request.crop}",
    ]
    if weather_context:
        user_message_parts.append(f"Weather Context: {weather_context}")
    if news_context:
        user_message_parts.append(f"News Context: {news_context}")

    full_prompt = "\n".join(user_message_parts)

    context_used = {
        "weather_included": request.include_weather,
        "news_included":    request.include_news,
    }

    # ------------------------------------------------------------------
    # Step 4: Primary LLM -> Google Gemini
    # ------------------------------------------------------------------
    gemini_answer = await _call_gemini(full_prompt)
    if gemini_answer:
        return {
            "answer": gemini_answer,
            "language": request.language,
            "context_used": context_used,
            "source": "gemini",
        }

    # ------------------------------------------------------------------
    # Step 5: Secondary Fallback -> Ollama
    # ------------------------------------------------------------------
    ollama_answer = await _call_ollama(full_prompt)
    if ollama_answer:
        return {
            "answer": ollama_answer,
            "language": request.language,
            "context_used": context_used,
            "source": "ollama",
        }

    # ------------------------------------------------------------------
    # Step 6: Tertiary Fallback -> Mock Advisory
    # ------------------------------------------------------------------
    mock_resp = _build_mock_response(request)
    mock_resp["context_used"] = context_used
    return mock_resp

