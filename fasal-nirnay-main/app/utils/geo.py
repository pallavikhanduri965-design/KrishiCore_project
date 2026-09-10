import requests
import math

API_KEY = "330bfd9138a143ffb0f2077d6cf8f1d3"

location_cache = {}


def get_coordinates(place: str):
    if place in location_cache:
        return location_cache[place]

    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": place,
        "key": API_KEY,
        "countrycode": "in",
        "limit": 1
    }

    response = requests.get(url, params=params).json()

    if response["results"]:
        lat = response["results"][0]["geometry"]["lat"]
        lon = response["results"][0]["geometry"]["lng"]

        location_cache[place] = (lat, lon)
        return lat, lon
    else:
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
