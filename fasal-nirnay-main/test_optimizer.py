"""
Tests for optimizer.py

Covers:
- transport_cost()       — truck-capacity aware model
- get_distance_to_mandi() — centroid → mandi haversine
- optimize_pool()        — best mandi selection
"""

import math
import pytest
from unittest.mock import patch

from app.services.virtual_pooling.optimizer import (
    transport_cost,
    get_distance_to_mandi,
    optimize_pool,
    TRUCK_CAPACITY_QUINTALS,
    TRUCK_BASE_COST_PER_KM,
    FALLBACK_DISTANCE_KM,
    MANDI_COORDINATES,
)


# ============================================================
# FIXTURES
# ============================================================

def make_pool(total_quantity=200, crop="wheat", centroid=(28.7, 77.1),
              num_farmers=3, pool_id="POOL-TEST01"):
    return {
        "pool_id":        pool_id,
        "crop":           crop,
        "total_quantity": total_quantity,
        "centroid":       centroid,
        "farmers":        [{"farmer_id": i} for i in range(num_farmers)],
    }


SAMPLE_MANDI_DATA = [
    {"mandi": "Azadpur",   "price": 2200},
    {"mandi": "Karnal",    "price": 2100},
    {"mandi": "Najafgarh", "price": 2150},
]


# ============================================================
# transport_cost()
# ============================================================

class TestTransportCost:

    def test_zero_quantity_returns_inf(self):
        assert transport_cost(100, 0) == float("inf")

    def test_negative_quantity_returns_inf(self):
        assert transport_cost(100, -50) == float("inf")

    def test_one_truck_for_small_quantity(self):
        # 50 quintals < 200 capacity → 1 truck
        cost = transport_cost(distance=100, quantity=50)
        expected = (1 * TRUCK_BASE_COST_PER_KM * 100) / 50
        assert cost == pytest.approx(expected)

    def test_exactly_one_truck_at_capacity(self):
        # 200 quintals == 1 truck capacity → still 1 truck
        cost = transport_cost(distance=100, quantity=200)
        expected = (1 * TRUCK_BASE_COST_PER_KM * 100) / 200
        assert cost == pytest.approx(expected)

    def test_two_trucks_for_201_quintals(self):
        # 201 quintals needs 2 trucks
        cost = transport_cost(distance=100, quantity=201)
        expected = (2 * TRUCK_BASE_COST_PER_KM * 100) / 201
        assert cost == pytest.approx(expected)

    def test_pooling_reduces_per_unit_cost(self):
        # 400 quintals (2 trucks) is cheaper per quintal than 100 quintals (1 truck)
        cost_small = transport_cost(distance=100, quantity=100)
        cost_large = transport_cost(distance=100, quantity=400)
        assert cost_large < cost_small

    def test_longer_distance_increases_cost(self):
        cost_near = transport_cost(distance=50,  quantity=200)
        cost_far  = transport_cost(distance=200, quantity=200)
        assert cost_far > cost_near

    def test_returns_float(self):
        assert isinstance(transport_cost(100, 200), float)


# ============================================================
# get_distance_to_mandi()
# ============================================================

class TestGetDistanceToMandi:

    def test_known_mandi_returns_real_distance(self):
        # Pool centroid near Delhi, Azadpur is in Delhi → short distance
        centroid = (28.70, 77.10)
        dist = get_distance_to_mandi(centroid, "Azadpur")
        assert dist < 50, f"Expected short distance to Azadpur, got {dist:.1f} km"

    def test_unknown_mandi_returns_fallback(self):
        centroid = (28.70, 77.10)
        dist = get_distance_to_mandi(centroid, "UnknownMandiXYZ")
        assert dist == FALLBACK_DISTANCE_KM

    def test_all_known_mandis_return_positive(self):
        centroid = (28.70, 77.10)
        for mandi_name in MANDI_COORDINATES:
            dist = get_distance_to_mandi(centroid, mandi_name)
            assert dist > 0, f"Distance to {mandi_name} should be > 0"

    def test_returns_float(self):
        dist = get_distance_to_mandi((28.7, 77.1), "Karnal")
        assert isinstance(dist, float)

    def test_closer_mandi_has_smaller_distance(self):
        # Pool centroid near Jhajjar (28.6, 76.9)
        # Najafgarh is closer than Karnal to Jhajjar
        centroid = (28.6, 76.9)
        dist_najafgarh = get_distance_to_mandi(centroid, "Najafgarh")
        dist_karnal    = get_distance_to_mandi(centroid, "Karnal")
        assert dist_najafgarh < dist_karnal


# ============================================================
# optimize_pool()
# ============================================================

class TestOptimizePool:

    def test_returns_dict_with_required_keys(self):
        pool = make_pool()
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)

        for key in ["pool_id", "crop", "total_quantity", "num_farmers",
                    "centroid", "recommendation"]:
            assert key in result, f"Missing key: {key}"

    def test_recommendation_has_required_keys(self):
        pool = make_pool()
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)
        rec = result["recommendation"]

        for key in ["mandi", "price", "distance_km", "trucks_needed",
                    "transport_cost", "net_price"]:
            assert key in rec, f"Recommendation missing key: {key}"

    def test_best_mandi_has_highest_net_price(self):
        # Manually check: net_price = price - transport_cost
        pool   = make_pool(total_quantity=200, centroid=(28.7, 77.1))
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)
        rec    = result["recommendation"]

        # Verify the returned net_price is genuinely the best
        for mandi in SAMPLE_MANDI_DATA:
            dist = get_distance_to_mandi(pool["centroid"], mandi["mandi"])
            cost = transport_cost(dist, pool["total_quantity"])
            net  = mandi["price"] - cost
            assert rec["net_price"] >= round(net, 2) - 0.01  # allow rounding

    def test_missing_centroid_returns_error(self):
        pool = make_pool()
        del pool["centroid"]
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)
        assert "error" in result

    def test_empty_mandi_list_returns_error(self):
        pool   = make_pool()
        result = optimize_pool(pool, [])
        assert "error" in result

    def test_pool_id_preserved_in_result(self):
        pool   = make_pool(pool_id="POOL-ABC123")
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)
        assert result["pool_id"] == "POOL-ABC123"

    def test_num_farmers_correct(self):
        pool   = make_pool(num_farmers=5)
        result = optimize_pool(pool, SAMPLE_MANDI_DATA)
        assert result["num_farmers"] == 5

    def test_trucks_needed_correct_in_recommendation(self):
        quantity = 450  # ceil(450/200) = 3 trucks
        pool     = make_pool(total_quantity=quantity)
        result   = optimize_pool(pool, SAMPLE_MANDI_DATA)
        assert result["recommendation"]["trucks_needed"] == 3

    def test_high_price_far_mandi_can_lose_to_cheaper_closer(self):
        """
        A mandi offering ₹200 more but 300 km away should lose
        to a mandi 20 km away with ₹200 less — transport eats the difference.
        """
        pool = make_pool(total_quantity=100, centroid=(28.7, 77.1))

        mandi_data = [
            {"mandi": "Azadpur", "price": 2000},   # ~5 km away
            {"mandi": "Jaipur",  "price": 2200},   # ~265 km away
        ]
        result = optimize_pool(pool, mandi_data)
        # With 100 quintals and 265 km, Jaipur transport cost is very high
        # Azadpur should win despite lower price
        assert result["recommendation"]["mandi"] == "Azadpur"

    def test_centroid_reflected_in_output(self):
        centroid = (28.55, 77.20)
        pool     = make_pool(centroid=centroid)
        result   = optimize_pool(pool, SAMPLE_MANDI_DATA)
        assert result["centroid"]["lat"] == pytest.approx(centroid[0])
        assert result["centroid"]["lon"] == pytest.approx(centroid[1])
