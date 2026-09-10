"""
Weather Service
===============
Handles all weather data fetching logic.
- If WEATHER_API_KEY is missing → returns mock data (safe for development).
- If WEATHER_API_KEY is present → calls WeatherAPI.com (free tier supported).
"""

import httpx
from typing import Any, Dict
from app.core.config import settings


# ------------------------------------------------------------------------------
# Mock data — returned when no API key is configured
# ------------------------------------------------------------------------------
MOCK_WEATHER: Dict[str, Any] = {
    "location": "Mock Location",
    "crop": "mock_crop",
    "current_temp_c": 28.5,
    "condition": "Partly Cloudy",
    "humidity": 65,
    "wind_kph": 14.0,
    "forecast": [
        {"day": 1, "max_temp_c": 30.0, "min_temp_c": 22.0, "condition": "Sunny",         "rain_chance_pct": 10},
        {"day": 2, "max_temp_c": 29.5, "min_temp_c": 21.5, "condition": "Partly Cloudy", "rain_chance_pct": 25},
        {"day": 3, "max_temp_c": 27.0, "min_temp_c": 20.0, "condition": "Light Rain",    "rain_chance_pct": 70},
    ],
    "source": "mock",
}


async def get_weather_forecast(location: str, crop: str, days: int = 3) -> Dict[str, Any]:
    """
    Fetches weather forecast for the given location.

    Args:
        location: City or region name (e.g., "Pune")
        crop:     Crop name — carried through for advisory context
        days:     Number of forecast days (1–7)

    Returns:
        A dictionary matching the WeatherResponse schema.
    """

    # ------------------------------------------------------------------
    # No API key? Return mock data so the endpoint still works.
    # ------------------------------------------------------------------
    if not settings.WEATHER_API_KEY:
        mock = MOCK_WEATHER.copy()
        mock["location"] = location
        mock["crop"] = crop
        mock["forecast"] = MOCK_WEATHER["forecast"][:days]
        return mock

    # ------------------------------------------------------------------
    # REAL API CALL — WeatherAPI.com
    # Docs: https://www.weatherapi.com/docs/
    # ------------------------------------------------------------------
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key":    settings.WEATHER_API_KEY,
        "q":      location,
        "days":   days,
        "aqi":    "no",
        "alerts": "no",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    # ------------------------------------------------------------------
    # Normalize the WeatherAPI response to our standard format
    # ------------------------------------------------------------------
    current = data["current"]
    forecast_days = data["forecast"]["forecastday"]

    normalized_forecast = [
        {
            "day":             idx + 1,
            "max_temp_c":      day["day"]["maxtemp_c"],
            "min_temp_c":      day["day"]["mintemp_c"],
            "condition":       day["day"]["condition"]["text"],
            "rain_chance_pct": day["day"]["daily_chance_of_rain"],
        }
        for idx, day in enumerate(forecast_days)
    ]

    return {
        "location":       data["location"]["name"],
        "crop":           crop,
        "current_temp_c": current["temp_c"],
        "condition":      current["condition"]["text"],
        "humidity":       current["humidity"],
        "wind_kph":       current["wind_kph"],
        "forecast":       normalized_forecast,
        "source":         "weatherapi.com",
    }
