"""
News Routes
===========
Exposes HTTP endpoints for agricultural news.
The actual fetching logic lives in services/news_service.py.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.news_service import get_latest_news
from app.models.schemas import NewsResponse

router = APIRouter()


@router.get("/latest", response_model=NewsResponse)
async def latest_news(
    location: str           = Query(...,  description="State or region, e.g. 'Maharashtra'"),
    crop: str               = Query(...,  description="Crop name, e.g. 'sugarcane'"),
    category: Optional[str] = Query(None, description="Optional category: mandi, weather, scheme, etc."),
):
    """
    Returns the latest agricultural news articles filtered by
    location, crop, and optional category.
    """
    try:
        result = await get_latest_news(location=location, crop=crop, category=category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News service error: {str(e)}")
