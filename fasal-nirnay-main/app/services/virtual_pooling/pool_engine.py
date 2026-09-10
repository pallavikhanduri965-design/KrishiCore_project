"""
Virtual Pool Engine

Responsible for:
- Creating pools
- Validating input data
- Aggregating farmer data
- Geo-based pooling (10 km radius)
- Auto pooling by crop
"""

from typing import List, Dict
import uuid

from app.utils.geo import get_coordinates, haversine

MAX_RADIUS_KM = 10


# -------------------------------
# VALIDATION
# -------------------------------
def validate_farmers(farmers: List[Dict]) -> None:
    if not farmers:
        raise ValueError("Farmers list cannot be empty")

    for f in farmers:
        if "farmer_id" not in f:
            raise ValueError("Missing farmer_id")
        if "quantity" not in f:
            raise ValueError("Missing quantity")
        if "location" not in f:
            raise ValueError("Missing location")
        if "crop" not in f:
            raise ValueError("Missing crop")

        if f["quantity"] <= 0:
            raise ValueError("Quantity must be positive")


# -------------------------------
# HELPERS
# -------------------------------
def generate_pool_id() -> str:
    return f"POOL-{uuid.uuid4().hex[:8].upper()}"


def aggregate_quantity(farmers: List[Dict]) -> float:
    return sum(f["quantity"] for f in farmers)


def group_by_location(farmers: List[Dict]) -> Dict:
    location_map = {}

    for f in farmers:
        loc = f["location"]

        if loc not in location_map:
            location_map[loc] = {
                "total_quantity": 0,
                "farmers": []
            }

        location_map[loc]["total_quantity"] += f["quantity"]
        location_map[loc]["farmers"].append(f)

    return location_map


# -------------------------------
# GEO FILTER
# -------------------------------
def filter_farmers_within_radius(farmers: List[Dict]) -> List[Dict]:
    if not farmers:
        return []

    base_location = farmers[0]["location"]
    base_lat, base_lon = get_coordinates(base_location)

    filtered = []

    for f in farmers:
        lat, lon = get_coordinates(f["location"])

        distance = haversine(base_lat, base_lon, lat, lon)

        print(f"Distance from {base_location} to {f['location']} = {distance:.2f} km")

        if distance <= MAX_RADIUS_KM:
            filtered.append(f)

    return filtered


# -------------------------------
# AUTO POOLING (NEW 🔥)
# -------------------------------
def group_farmers_by_crop(farmers: List[Dict]) -> Dict[str, List[Dict]]:
    crop_groups = {}

    for f in farmers:
        crop = f["crop"].lower()

        if crop not in crop_groups:
            crop_groups[crop] = []

        crop_groups[crop].append(f)

    return crop_groups


def create_auto_pools(farmers: List[Dict]) -> List[Dict]:
    """
    Auto create pools:
    - Group by crop
    - Apply 10 km geo filter
    """

    validate_farmers(farmers)

    crop_groups = group_farmers_by_crop(farmers)

    all_pools = []

    for crop, farmer_group in crop_groups.items():

        filtered_farmers = filter_farmers_within_radius(farmer_group)

        if not filtered_farmers:
            continue

        total_quantity = aggregate_quantity(filtered_farmers)
        location_summary = group_by_location(filtered_farmers)

        pool = {
            "pool_id": generate_pool_id(),
            "crop": crop,
            "farmers": filtered_farmers,
            "total_quantity": total_quantity,
            "location_summary": location_summary
        }

        all_pools.append(pool)

    return all_pools