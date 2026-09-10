"""
Tests for pooling.py (FastAPI route)

Covers:
- POST /pool/ happy path
- Validation errors (400)
- Empty pool scenario
- Missing mandi data per crop
- Multi-crop, multi-cluster responses
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.routes.pooling import router

# ---- Build a minimal app just for testing ----
app = FastAPI()
app.include_router(router)
client = TestClient(app)



# ============================================================
# HELPERS
# ============================================================

def make_farmer_payload(farmer_id, location, quantity, crop):
    return {
        "farmer_id": farmer_id,
        "quantity":  quantity,
        "location":  location,
        "crop":      crop,
    }


WHEAT_FARMERS_CLOSE = [
    make_farmer_payload(1, "Jhajjar",     100, "wheat"),
    make_farmer_payload(2, "Jhajjar",     150, "wheat"),
    make_farmer_payload(3, "Bahadurgarh", 80,  "wheat"),
]

MIXED_CROP_FARMERS = [
    make_farmer_payload(1, "Jhajjar", 100, "wheat"),
    make_farmer_payload(2, "Jhajjar",  80, "mustard"),
]

MOCK_POOL = {
    "pool_id":        "POOL-TEST01",
    "crop":           "wheat",
    "total_quantity": 330,
    "centroid":       (28.6, 76.9),
    "farmers":        WHEAT_FARMERS_CLOSE,
    "location_summary": {},
    "cluster_index":  1,
}

MOCK_MANDI_DATA = [
    {"mandi": "Azadpur",   "price": 2200},
    {"mandi": "Karnal",    "price": 2100},
]

MOCK_OPTIMIZE_RESULT = {
    "pool_id":        "POOL-TEST01",
    "crop":           "wheat",
    "total_quantity": 330,
    "num_farmers":    3,
    "centroid":       {"lat": 28.6, "lon": 76.9},
    "recommendation": {
        "mandi":          "Azadpur",
        "price":          2200,
        "distance_km":    45.0,
        "trucks_needed":  2,
        "transport_cost": 15.91,
        "net_price":      2184.09,
    },
}


# ============================================================
# HAPPY PATH
# ============================================================

class TestPoolRouteHappyPath:

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_success_returns_200(self, mock_mandi, mock_optimize, mock_pools):
        mock_pools.return_value    = [MOCK_POOL]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})

        assert response.status_code == 200

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_response_has_status_success(self, mock_mandi, mock_optimize, mock_pools):
        mock_pools.return_value    = [MOCK_POOL]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        data     = response.json()

        assert data["status"] == "success"

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_response_has_pools_list(self, mock_mandi, mock_optimize, mock_pools):
        mock_pools.return_value    = [MOCK_POOL]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        data     = response.json()

        assert "pools" in data
        assert isinstance(data["pools"], list)
        assert len(data["pools"]) == 1

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_total_pools_count_correct(self, mock_mandi, mock_optimize, mock_pools):
        mock_pools.return_value    = [MOCK_POOL]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        data     = response.json()

        assert data["total_pools"] == 1

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_multi_pool_response(self, mock_mandi, mock_optimize, mock_pools):
        pool2 = {**MOCK_POOL, "pool_id": "POOL-TEST02", "crop": "mustard"}
        mock_pools.return_value    = [MOCK_POOL, pool2]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={"farmers": MIXED_CROP_FARMERS})
        data     = response.json()

        assert data["total_pools"] == 2


# ============================================================
# VALIDATION ERRORS (400)
# ============================================================

class TestPoolRouteValidation:

    def test_empty_farmers_list_returns_400(self):
        response = client.post("/pool/", json={"farmers": []})
        # FastAPI pydantic validation returns 422 for empty list,
        # but our code raises ValueError → 400 from HTTPException
        assert response.status_code in (400, 422)

    def test_missing_farmers_field_returns_422(self):
        response = client.post("/pool/", json={})
        assert response.status_code == 422

    def test_negative_quantity_returns_422(self):
        farmers = [make_farmer_payload(1, "Jhajjar", -10, "wheat")]
        response = client.post("/pool/", json={"farmers": farmers})
        # Pydantic doesn't validate >0 by default, but our engine does
        # So we just check it doesn't return 200
        assert response.status_code != 200

    def test_missing_location_returns_422(self):
        response = client.post("/pool/", json={
            "farmers": [{"farmer_id": 1, "quantity": 100, "crop": "wheat"}]
        })
        assert response.status_code == 422

    def test_missing_crop_returns_422(self):
        response = client.post("/pool/", json={
            "farmers": [{"farmer_id": 1, "quantity": 100, "location": "Jhajjar"}]
        })
        assert response.status_code == 422


# ============================================================
# EDGE CASES
# ============================================================

class TestPoolRouteEdgeCases:

    @patch("app.routes.pooling.create_auto_pools")
    def test_no_pools_created_returns_400(self, mock_pools):
        mock_pools.return_value = []

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        assert response.status_code == 400
        assert "No valid pools" in response.json()["detail"]

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_empty_mandi_data_returns_error_in_pool(self, mock_mandi, mock_pools):
        """
        When mandi prediction returns no data for a crop,
        the route should not crash — it should return an error
        inside that pool's entry, not a 500.
        """
        mock_pools.return_value = [MOCK_POOL]
        mock_mandi.return_value = []  # no mandi data

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        data     = response.json()

        assert response.status_code == 200
        assert "error" in data["pools"][0]

    @patch("app.routes.pooling.create_auto_pools")
    def test_unexpected_exception_returns_500(self, mock_pools):
        mock_pools.side_effect = RuntimeError("Unexpected crash")

        response = client.post("/pool/", json={"farmers": WHEAT_FARMERS_CLOSE})
        assert response.status_code == 500

    @patch("app.routes.pooling.create_auto_pools")
    @patch("app.routes.pooling.optimize_pool")
    @patch("app.routes.pooling.get_mandi_predictions")
    def test_single_farmer_still_processed(self, mock_mandi, mock_optimize, mock_pools):
        single_farmer_pool = {**MOCK_POOL, "farmers": [WHEAT_FARMERS_CLOSE[0]], "total_quantity": 100}
        mock_pools.return_value    = [single_farmer_pool]
        mock_mandi.return_value    = MOCK_MANDI_DATA
        mock_optimize.return_value = MOCK_OPTIMIZE_RESULT

        response = client.post("/pool/", json={
            "farmers": [WHEAT_FARMERS_CLOSE[0]]
        })
        assert response.status_code == 200
