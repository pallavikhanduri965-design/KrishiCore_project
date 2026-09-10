"""
Weather Routes
==============
Exposes HTTP endpoints for weather-related data.
The actual data fetching logic lives in services/weather_service.py.
"""

from fastapi import APIRouter, HTTPException, Query
from app.services.weather_service import get_weather_forecast
from app.models.schemas import WeatherResponse

router = APIRouter()


@router.get("/forecast", response_model=WeatherResponse)
async def weather_forecast(
    location: str = Query(...,  description="City or region name, e.g. 'Pune'"),
    crop: str     = Query(...,  description="Crop name, e.g. 'wheat'"),
    days: int     = Query(3,    description="Number of forecast days (1–7)", ge=1, le=7),
):
    """
    Returns current weather conditions and a multi-day forecast
    for the given location. Useful for crop-specific advisories.
    """
    try:
        result = await get_weather_forecast(location=location, crop=crop, days=days)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weather service error: {str(e)}")
