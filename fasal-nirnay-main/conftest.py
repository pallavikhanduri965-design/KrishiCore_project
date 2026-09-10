# conftest.py
# Shared pytest fixtures and configuration for the Virtual Pooling test suite.

import pytest
from unittest.mock import patch


# ---------------------------------------------------------------
# Auto-clear the geo location cache before every test
# so cached API responses from one test don't bleed into another.
# ---------------------------------------------------------------
@pytest.fixture(autouse=True)
def clear_geo_cache():
    from app.utils import geo
    geo.location_cache.clear()
    yield
    geo.location_cache.clear()


# ---------------------------------------------------------------
# Reusable farmer factory fixture
# ---------------------------------------------------------------
@pytest.fixture
def make_farmer():
    def _make(farmer_id, location, quantity=100, crop="wheat"):
        return {
            "farmer_id": farmer_id,
            "location":  location,
            "quantity":  quantity,
            "crop":      crop,
        }
    return _make


# ---------------------------------------------------------------
# Standard close-cluster farmers (all within 10 km)
# ---------------------------------------------------------------
@pytest.fixture
def close_wheat_farmers(make_farmer):
    return [
        make_farmer(1, "Jhajjar",       quantity=100, crop="wheat"),
        make_farmer(2, "Jhajjar",       quantity=150, crop="wheat"),
        make_farmer(3, "Bahadurgarh",   quantity=80,  crop="wheat"),
    ]


# ---------------------------------------------------------------
# Two farmers far apart — should create 2 pools for same crop
# ---------------------------------------------------------------
@pytest.fixture
def far_wheat_farmers(make_farmer):
    return [
        make_farmer(1, "Jhajjar", quantity=100, crop="wheat"),
        make_farmer(2, "Rohtak",  quantity=200, crop="wheat"),
    ]


# ---------------------------------------------------------------
# Sample mandi price data
# ---------------------------------------------------------------
@pytest.fixture
def sample_mandi_data():
    return [
        {"mandi": "Azadpur",   "price": 2200},
        {"mandi": "Karnal",    "price": 2100},
        {"mandi": "Najafgarh", "price": 2150},
    ]


# ---------------------------------------------------------------
# A pre-built pool object (as returned by create_auto_pools)
# ---------------------------------------------------------------
@pytest.fixture
def sample_pool():
    return {
        "pool_id":         "POOL-FIXTURE1",
        "crop":            "wheat",
        "total_quantity":  330,
        "centroid":        (28.6, 76.9),
        "farmers":         [{"farmer_id": i} for i in range(3)],
        "location_summary": {},
        "cluster_index":   1,
    }
