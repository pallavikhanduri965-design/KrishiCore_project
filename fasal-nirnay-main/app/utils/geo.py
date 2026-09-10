import requests
import math
from typing import Tuple, List, Dict
from app.core.config import settings

location_cache: Dict[str, Tuple[float, float]] = {}

# Fallback coordinates for common agricultural regions in case network/quota fails
FALLBACK_COORDINATES: Dict[str, Tuple[float, float]] = {
    "delhi": (28.7041, 77.1025),
    "jhajjar": (28.6067, 76.6565),
    "rohtak": (28.8955, 76.6066),
    "bahadurgarh": (28.6924, 76.9240),
    "karnal": (29.6857, 76.9905),
    "sonipat": (28.9929, 77.0151),
    "hisar": (29.1492, 75.7217),
    "jaipur": (26.9124, 75.7873),
    "alwar": (27.5530, 76.6346),
    "pune": (18.5204, 73.8567),
    "nashik": (19.9975, 73.7898),
}


def get_coordinates(place: str) -> Tuple[float, float]:
    """
    Get geographic coordinates (lat, lon) for a location name.
    Uses in-memory cache, OpenCage Geocoding API, and fallback defaults.
    """
    if not place:
        raise ValueError("Location string cannot be empty")

    normalized = place.strip().lower()
    if place in location_cache:
        return location_cache[place]
    if normalized in location_cache:
        return location_cache[normalized]

    api_key = getattr(settings, "OPENCAGE_API_KEY", "330bfd9138a143ffb0f2077d6cf8f1d3")
    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": place,
        "key": api_key,
        "countrycode": "in",
        "limit": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10.0)
        data = response.json()
        if data.get("results"):
            lat = float(data["results"][0]["geometry"]["lat"])
            lon = float(data["results"][0]["geometry"]["lng"])
            location_cache[place] = (lat, lon)
            location_cache[normalized] = (lat, lon)
            return lat, lon
    except Exception as e:
        # If network fails, try known fallback coordinates before raising
        if normalized in FALLBACK_COORDINATES:
            lat, lon = FALLBACK_COORDINATES[normalized]
            location_cache[place] = (lat, lon)
            return lat, lon
        raise ValueError(f"Location not found: {place}") from e

    # If results list is empty
    if normalized in FALLBACK_COORDINATES:
        lat, lon = FALLBACK_COORDINATES[normalized]
        location_cache[place] = (lat, lon)
        return lat, lon

    raise ValueError(f"Location not found: {place}")


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def compute_centroid(farmers: list) -> tuple:
    """
    Compute the geographic centroid (average lat/lon)
    of a group of farmers based on their location strings.
    Returns (avg_lat, avg_lon)
    """
    coords = [get_coordinates(f["location"]) for f in farmers]
    avg_lat = sum(c[0] for c in coords) / len(coords)
    avg_lon = sum(c[1] for c in coords) / len(coords)
    return avg_lat, avg_lon
