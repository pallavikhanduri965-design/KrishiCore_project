"""
News Service
============
Handles all news fetching logic.
- If NEWS_API_KEY is missing → returns mock articles (safe for development).
- If NEWS_API_KEY is present → calls GNews API.
"""

import httpx
from typing import Any, Dict, List, Optional
from app.core.config import settings


# ------------------------------------------------------------------------------
# Mock data — returned when no API key is configured
# ------------------------------------------------------------------------------
MOCK_ARTICLES: List[Dict[str, Any]] = [
    {
        "title":        "Government Raises MSP for Wheat by ₹150",
        "description":  "The central government has announced a hike in the Minimum Support Price for wheat ahead of the Rabi season.",
        "source":       "Mock Agriculture News",
        "published_at": "2024-10-15T08:30:00Z",
        "url":          "https://example.com/news/1",
    },
    {
        "title":        "IMD Predicts Above-Normal Monsoon for Vidarbha Region",
        "description":  "The Indian Meteorological Department has issued a positive monsoon forecast for key agricultural zones.",
        "source":       "Mock Weather News",
        "published_at": "2024-10-14T10:00:00Z",
        "url":          "https://example.com/news/2",
    },
    {
        "title":        "PM Kisan Samman Nidhi — Next Installment Date Announced",
        "description":  "Eligible farmers will receive the next PM-KISAN installment by the end of this month.",
        "source":       "Mock Government News",
        "published_at": "2024-10-13T07:45:00Z",
        "url":          "https://example.com/news/3",
    },
]


async def get_latest_news(
    location: str,
    crop: str,
    category: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetches the latest agricultural news for a given location and crop.

    Args:
        location: State or region (e.g., "Maharashtra")
        crop:     Crop name (e.g., "sugarcane")
        category: Optional filter — "mandi", "weather", "scheme", etc.

    Returns:
        A dictionary matching the NewsResponse schema.
    """

    # ------------------------------------------------------------------
    # No API key? Return mock articles.
    # ------------------------------------------------------------------
    if not settings.NEWS_API_KEY:
        return {
            "location": location,
            "crop":     crop,
            "category": category,
            "total":    len(MOCK_ARTICLES),
            "articles": MOCK_ARTICLES,
            "source":   "mock",
        }

    # ------------------------------------------------------------------
    # Build a smart search query from the inputs
    # ------------------------------------------------------------------
    query_parts = [crop, location, "agriculture", "farming"]
    if category:
        query_parts.append(category)
    query = " ".join(query_parts)

    # ------------------------------------------------------------------
    # REAL API CALL — GNews API
    # Docs: https://gnews.io/docs/
    # Free tier: 100 requests/day, 10 articles/response
    # ------------------------------------------------------------------
    url = "https://gnews.io/api/v4/search"
    params = {
        "q":      query,
        "lang":   "en",
        "country": "in",      # India
        "max":    10,
        "apikey": settings.NEWS_API_KEY,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    # ------------------------------------------------------------------
    # Normalize GNews response to our standard format
    # ------------------------------------------------------------------
    articles = [
        {
            "title":        article.get("title", ""),
            "description":  article.get("description", ""),
            "source":       article.get("source", {}).get("name", "Unknown"),
            "published_at": article.get("publishedAt", ""),
            "url":          article.get("url", ""),
        }
        for article in data.get("articles", [])
    ]

    return {
        "location": location,
        "crop":     crop,
        "category": category,
        "total":    len(articles),
        "articles": articles,
        "source":   "gnews.io",
    }
