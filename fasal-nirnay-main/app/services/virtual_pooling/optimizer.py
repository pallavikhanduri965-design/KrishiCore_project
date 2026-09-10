"""
Pooling Optimization Engine — FasalNirnay AI

Net profit equation per quintal:

    effective_price  = predicted_price × grade_multiplier
    transport_cost   = (num_trucks × TRUCK_BASE_COST_PER_KM × distance) / quantity
    net_price        = effective_price − transport_cost

Where:
    predicted_price  → from XGB + LGB + LSTM meta stack  (prediction.py)
    grade_multiplier → based on grade classifier output   (see GRADE_MULTIPLIER)
    distance         → Haversine from pool centroid to mandi
    num_trucks       → ceil(quantity / TRUCK_CAPACITY_QUINTALS)
"""

import math
from typing import List, Dict, Optional

from app.utils.geo import haversine


# ─────────────────────────────────────────────
# MANDI COORDINATES
# Must stay in sync with MANDI_CONFIG in prediction.py.
# ─────────────────────────────────────────────
MANDI_COORDINATES: Dict[str, tuple] = {
    "Azadpur":    (28.7333, 77.1667),
    "Karnal":     (29.6857, 76.9905),
    "Rohtak":     (28.8955, 76.6066),
    "Najafgarh":  (28.6092, 76.9798),
    "Jaipur":     (26.9124, 75.7873),
    "Alwar":      (27.5530, 76.6346),
    "Hisar":      (29.1492, 75.7217),
    "Sonipat":    (28.9929, 77.0151),
}

# ─────────────────────────────────────────────
# GRADE MULTIPLIER TABLE
#
# How to read this:
#   A "Best" grade crop fetches ~5% premium over base price.
#   A "Common" grade crop fetches ~8% less.
#   "FAQ" (Fair Average Quality) is the baseline (1.0).
#
# Calibrate these from real Agmarknet/eNAM arrival data
# once you have enough grade-vs-price pairs.
# ─────────────────────────────────────────────
GRADE_MULTIPLIER: Dict[str, float] = {
    "Best":   1.05,    # premium grade  → +5%
    "FAQ":    1.00,    # fair average   → baseline
    "Common": 0.92,    # below average  → −8%
    "Poor":   0.80,    # rejected lots  → −20%
}
DEFAULT_GRADE_MULTIPLIER = 1.00   # fallback for unknown grade labels


# ─────────────────────────────────────────────
# TRUCK MODEL CONSTANTS
# ─────────────────────────────────────────────
TRUCK_CAPACITY_QUINTALS = 200    # max load per truck
TRUCK_BASE_COST_PER_KM  = 25     # ₹ per km per truck
FALLBACK_DISTANCE_KM    = 100    # used when mandi coords are unknown


# ─────────────────────────────────────────────
# DISTANCE
# ─────────────────────────────────────────────
def get_distance_to_mandi(centroid: tuple, mandi_name: str) -> float:
    """
    Haversine distance (km) from pool centroid to mandi.
    Falls back to FALLBACK_DISTANCE_KM if mandi not in our map.
    """
    if mandi_name not in MANDI_COORDINATES:
        print(
            f"  ⚠ '{mandi_name}' not in MANDI_COORDINATES — "
            f"using fallback {FALLBACK_DISTANCE_KM} km"
        )
        return FALLBACK_DISTANCE_KM

    m_lat, m_lon = MANDI_COORDINATES[mandi_name]
    p_lat, p_lon = centroid
    return haversine(p_lat, p_lon, m_lat, m_lon)


# ─────────────────────────────────────────────
# TRANSPORT COST  (truck-capacity aware)
# ─────────────────────────────────────────────
def transport_cost(distance: float, quantity: float) -> float:
    """
    Per-quintal transport cost.

    Formula:
        num_trucks  = ceil(quantity / TRUCK_CAPACITY)
        total_cost  = num_trucks × TRUCK_BASE_COST_PER_KM × distance
        cost_per_q  = total_cost / quantity

    Pooling more quantity onto fewer trucks lowers cost per quintal,
    but unlike quantity^0.5 scaling, cost never drops below the
    actual truck floor.
    """
    if quantity <= 0:
        return float("inf")

    num_trucks = math.ceil(quantity / TRUCK_CAPACITY_QUINTALS)
    total_cost = num_trucks * TRUCK_BASE_COST_PER_KM * distance
    return total_cost / quantity


# ─────────────────────────────────────────────
# NET PROFIT EQUATION
# ─────────────────────────────────────────────
def compute_net_price(predicted_price: float,
                      grade: str,
                      grade_confidence: float,
                      distance: float,
                      quantity: float) -> Dict:
    """
    Core equation:

        effective_price = predicted_price × grade_multiplier
        transport_cost  = truck-aware cost per quintal
        net_price       = effective_price − transport_cost

    grade_confidence is used for display/logging only — the
    multiplier already encodes the expected price impact of the grade.

    Returns a dict with all intermediate values for transparency.
    """
    multiplier     = GRADE_MULTIPLIER.get(grade, DEFAULT_GRADE_MULTIPLIER)
    effective      = predicted_price * multiplier
    t_cost         = transport_cost(distance, quantity)
    net            = effective - t_cost
    num_trucks     = math.ceil(quantity / TRUCK_CAPACITY_QUINTALS)

    return {
        "predicted_price":   round(predicted_price, 2),
        "grade":             grade,
        "grade_multiplier":  multiplier,
        "grade_confidence":  round(grade_confidence, 4),
        "effective_price":   round(effective, 2),     # after grade adjustment
        "distance_km":       round(distance, 1),
        "trucks_needed":     num_trucks,
        "transport_cost":    round(t_cost, 2),
        "net_price":         round(net, 2),           # ← final profit metric
    }


# ─────────────────────────────────────────────
# MAIN OPTIMIZER
# ─────────────────────────────────────────────
def optimize_pool(pool: Dict, mandi_data: List[Dict]) -> Dict:
    """
    Find the most profitable mandi for a given pool.

    `mandi_data` must come from get_mandi_predictions() and contain:
        predicted_price, grade, grade_confidence  per mandi.

    The optimizer picks the mandi with the highest net_price where:
        net_price = (predicted_price × grade_multiplier) − transport_cost/q
    """
    centroid = pool.get("centroid")
    if centroid is None:
        return {"error": "Pool is missing centroid — cannot compute distances"}

    print(f"\n{'='*56}")
    print(f"Pool      : {pool['pool_id']}  |  crop: {pool['crop']}")
    print(f"Quantity  : {pool['total_quantity']} quintals  "
          f"|  farmers: {len(pool['farmers'])}")
    print(f"Centroid  : lat={centroid[0]:.4f}, lon={centroid[1]:.4f}")
    print(f"{'='*56}")

    best_option: Optional[Dict] = None
    best_net = -float("inf")

    for mandi in mandi_data:
        mandi_name       = mandi["mandi"]
        predicted_price  = mandi["predicted_price"]
        grade            = mandi.get("grade", "FAQ")
        grade_confidence = mandi.get("grade_confidence", 1.0)

        distance = get_distance_to_mandi(centroid, mandi_name)

        breakdown = compute_net_price(
            predicted_price  = predicted_price,
            grade            = grade,
            grade_confidence = grade_confidence,
            distance         = distance,
            quantity         = pool["total_quantity"],
        )

        print(
            f"\n  Mandi          : {mandi_name}  ({mandi.get('state', '')})"
            f"\n  Predicted price: ₹{predicted_price}/q"
            f"\n  Grade          : {grade} (conf: {grade_confidence*100:.1f}%)"
            f"\n  Grade mult     : ×{breakdown['grade_multiplier']}"
            f"\n  Effective price: ₹{breakdown['effective_price']}/q"
            f"\n  Distance       : {breakdown['distance_km']} km"
            f"\n  Trucks needed  : {breakdown['trucks_needed']}"
            f"\n  Transport cost : ₹{breakdown['transport_cost']}/q"
            f"\n  ─────────────────────────────────"
            f"\n  Net price      : ₹{breakdown['net_price']}/q"
        )

        if breakdown["net_price"] > best_net:
            best_net    = breakdown["net_price"]
            best_option = {"mandi": mandi_name, **breakdown}

    if best_option is None:
        return {"error": "No valid mandi found"}

    print(f"\n  ✅ Best: {best_option['mandi']} @ ₹{best_option['net_price']}/q net")

    total_earnings = round(best_option["net_price"] * pool["total_quantity"], 2)

    return {
        "pool_id":         pool["pool_id"],
        "crop":            pool["crop"],
        "total_quantity":  pool["total_quantity"],
        "num_farmers":     len(pool["farmers"]),
        "centroid":        {"lat": centroid[0], "lon": centroid[1]},
        "recommendation":  best_option,
        "total_earnings":  total_earnings,    # net_price × total_quantity
    }
