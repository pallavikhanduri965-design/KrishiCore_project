"""
Tests for geo.py

Covers:
- haversine() distance formula
- get_coordinates() with mocking (no real API calls)
- compute_centroid() correctness
"""

import pytest
from unittest.mock import patch, MagicMock

# ---- import the module under test ----
from app.utils.geo import haversine, get_coordinates, compute_centroid


# ============================================================
# haversine()
# ============================================================

class TestHaversine:

    def test_same_point_is_zero(self):
        assert haversine(28.7041, 77.1025, 28.7041, 77.1025) == 0.0

    def test_delhi_to_karnal_approx(self):
        # Delhi (28.7041, 77.1025) → Karnal (29.6857, 76.9905) ≈ 110 km
        dist = haversine(28.7041, 77.1025, 29.6857, 76.9905)
        assert 100 < dist < 125, f"Expected ~110 km, got {dist:.2f}"

    def test_delhi_to_jaipur_approx(self):
        # Delhi → Jaipur ≈ 265 km
        dist = haversine(28.7041, 77.1025, 26.9124, 75.7873)
        assert 250 < dist < 285, f"Expected ~265 km, got {dist:.2f}"

    def test_symmetry(self):
        d1 = haversine(28.7041, 77.1025, 29.6857, 76.9905)
        d2 = haversine(29.6857, 76.9905, 28.7041, 77.1025)
        assert abs(d1 - d2) < 0.001

    def test_short_distance_within_10km(self):
        # Two points ~5 km apart (within pooling radius)
        dist = haversine(28.7041, 77.1025, 28.7490, 77.1025)
        assert dist < 10, f"Expected < 10 km, got {dist:.2f}"

    def test_returns_float(self):
        result = haversine(28.0, 77.0, 29.0, 78.0)
        assert isinstance(result, float)


# ============================================================
# get_coordinates()
# ============================================================

MOCK_OPENCAGE_RESPONSE = {
    "results": [
        {
            "geometry": {
                "lat": 28.7041,
                "lng": 77.1025
            }
        }
    ]
}

MOCK_EMPTY_RESPONSE = {"results": []}


class TestGetCoordinates:

    def setup_method(self):
        # Clear cache before each test so tests don't bleed into each other
        from app.utils import geo
        geo.location_cache.clear()

    @patch("app.utils.geo.requests.get")
    def test_returns_correct_lat_lon(self, mock_get):
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = MOCK_OPENCAGE_RESPONSE

        lat, lon = get_coordinates("Delhi")
        assert lat == 28.7041
        assert lon == 77.1025

    @patch("app.utils.geo.requests.get")
    def test_caches_result(self, mock_get):
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = MOCK_OPENCAGE_RESPONSE

        get_coordinates("Delhi")
        get_coordinates("Delhi")

        # API should only be called once despite two calls
        assert mock_get.call_count == 1

    @patch("app.utils.geo.requests.get")
    def test_raises_on_empty_result(self, mock_get):
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = MOCK_EMPTY_RESPONSE

        with pytest.raises(ValueError, match="Location not found"):
            get_coordinates("NonExistentVillageXYZ")

    @patch("app.utils.geo.requests.get")
    def test_different_locations_called_separately(self, mock_get):
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = MOCK_OPENCAGE_RESPONSE

        get_coordinates("Delhi")
        get_coordinates("Karnal")

        assert mock_get.call_count == 2


# ============================================================
# compute_centroid()
# ============================================================

class TestComputeCentroid:

    @patch("app.utils.geo.get_coordinates")
    def test_single_farmer_centroid_equals_location(self, mock_coords):
        mock_coords.return_value = (28.7041, 77.1025)
        farmers = [{"farmer_id": 1, "location": "Delhi", "quantity": 50, "crop": "wheat"}]
        lat, lon = compute_centroid(farmers)
        assert lat == 28.7041
        assert lon == 77.1025

    @patch("app.utils.geo.get_coordinates")
    def test_two_farmers_centroid_is_midpoint(self, mock_coords):
        mock_coords.side_effect = [
            (28.0, 77.0),
            (29.0, 78.0),
        ]
        farmers = [
            {"farmer_id": 1, "location": "A", "quantity": 50, "crop": "wheat"},
            {"farmer_id": 2, "location": "B", "quantity": 50, "crop": "wheat"},
        ]
        lat, lon = compute_centroid(farmers)
        assert lat == pytest.approx(28.5)
        assert lon == pytest.approx(77.5)

    @patch("app.utils.geo.get_coordinates")
    def test_four_farmers_centroid(self, mock_coords):
        mock_coords.side_effect = [
            (28.0, 77.0),
            (28.0, 78.0),
            (29.0, 77.0),
            (29.0, 78.0),
        ]
        farmers = [{"farmer_id": i, "location": str(i), "quantity": 10, "crop": "wheat"} for i in range(4)]
        lat, lon = compute_centroid(farmers)
        assert lat == pytest.approx(28.5)
        assert lon == pytest.approx(77.5)

    @patch("app.utils.geo.get_coordinates")
    def test_returns_tuple(self, mock_coords):
        mock_coords.return_value = (28.7041, 77.1025)
        farmers = [{"farmer_id": 1, "location": "Delhi", "quantity": 50, "crop": "wheat"}]
        result = compute_centroid(farmers)
        assert isinstance(result, tuple)
        assert len(result) == 2
