"""
Virtual Pool Engine — FasalNirnay AI
====================================
Responsible for:
- Validating farmer input payloads
- Aggregating farmer crop quantities
- Geographic clustering within 10 km radius
- Auto pool generation with centroid calculation
"""

from typing import List, Dict, Tuple
import uuid

from app.utils.geo import get_coordinates, haversine, compute_centroid

MAX_RADIUS_KM = 10.0


# ------------------------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------------------------
def validate_farmers(farmers: List[Dict]) -> None:
    """Validate that the farmer list is non-empty and contains required fields."""
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


# ------------------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------------------
def generate_pool_id() -> str:
    """Generate a unique pool identifier."""
    return f"POOL-{uuid.uuid4().hex[:8].upper()}"


def aggregate_quantity(farmers: List[Dict]) -> float:
    """Sum the total quantity in quintals for a group of farmers."""
    return sum(float(f["quantity"]) for f in farmers)


def group_by_location(farmers: List[Dict]) -> Dict[str, Dict]:
    """Group farmers by their location string for delivery coordination."""
    location_map: Dict[str, Dict] = {}

    for f in farmers:
        loc = f["location"]
        if loc not in location_map:
            location_map[loc] = {
                "total_quantity": 0.0,
                "farmers": [],
            }

        location_map[loc]["total_quantity"] += float(f["quantity"])
        location_map[loc]["farmers"].append(f)

    return location_map


def group_farmers_by_crop(farmers: List[Dict]) -> Dict[str, List[Dict]]:
    """Group farmers by crop name (normalized to lower case)."""
    crop_groups: Dict[str, List[Dict]] = {}

    for f in farmers:
        crop = str(f["crop"]).strip().lower()
        if crop not in crop_groups:
            crop_groups[crop] = []
        crop_groups[crop].append(f)

    return crop_groups


# ------------------------------------------------------------------------------
# PROXIMITY CLUSTERING
# ------------------------------------------------------------------------------
def cluster_farmers_by_proximity(farmers: List[Dict]) -> List[List[Dict]]:
    """
    Cluster a group of farmers into geographic sub-clusters where farmers
    within MAX_RADIUS_KM (10 km) of the cluster seed are grouped together.
    """
    if not farmers:
        return []
    if len(farmers) == 1:
        return [[farmers[0]]]

    remaining = list(farmers)
    clusters: List[List[Dict]] = []

    while remaining:
        seed = remaining.pop(0)
        current_cluster = [seed]
        seed_lat, seed_lon = get_coordinates(seed["location"])

        unclustered: List[Dict] = []
        for f in remaining:
            f_lat, f_lon = get_coordinates(f["location"])
            dist = haversine(seed_lat, seed_lon, f_lat, f_lon)
            if dist <= MAX_RADIUS_KM:
                current_cluster.append(f)
            else:
                unclustered.append(f)

        remaining = unclustered
        clusters.append(current_cluster)

    return clusters


def filter_farmers_within_radius(farmers: List[Dict]) -> List[Dict]:
    """Filter farmers within MAX_RADIUS_KM of the first farmer (legacy compatibility)."""
    if not farmers:
        return []

    base_location = farmers[0]["location"]
    base_lat, base_lon = get_coordinates(base_location)

    filtered = []
    for f in farmers:
        lat, lon = get_coordinates(f["location"])
        distance = haversine(base_lat, base_lon, lat, lon)
        if distance <= MAX_RADIUS_KM:
            filtered.append(f)

    return filtered


# ------------------------------------------------------------------------------
# AUTO POOLING
# ------------------------------------------------------------------------------
def create_auto_pools(farmers: List[Dict]) -> List[Dict]:
    """
    Auto create pools:
    - Validates farmer inputs
    - Groups farmers by crop
    - Applies geographic proximity clustering (10 km radius)
    - Computes pool centroid, aggregated quantities, and location summaries
    """
    validate_farmers(farmers)
    crop_groups = group_farmers_by_crop(farmers)
    all_pools = []

    for crop, farmer_group in crop_groups.items():
        clusters = cluster_farmers_by_proximity(farmer_group)

        for cluster in clusters:
            if not cluster:
                continue

            total_quantity = aggregate_quantity(cluster)
            location_summary = group_by_location(cluster)
            centroid = compute_centroid(cluster)

            pool = {
                "pool_id": generate_pool_id(),
                "crop": crop,
                "farmers": cluster,
                "total_quantity": total_quantity,
                "location_summary": location_summary,
                "centroid": centroid,
            }
            all_pools.append(pool)

    return all_pools