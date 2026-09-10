"""
Tests for pool_engine.py

Covers:
- validate_farmers()
- aggregate_quantity()
- group_by_location()
- cluster_farmers_by_proximity()  ← key new logic
- create_auto_pools()
"""

import pytest
from unittest.mock import patch

from app.services.virtual_pooling.pool_engine import (
    validate_farmers,
    aggregate_quantity,
    group_by_location,
    cluster_farmers_by_proximity,
    create_auto_pools,
    generate_pool_id,
)


# ============================================================
# FIXTURES
# ============================================================

def make_farmer(farmer_id, location, quantity=100, crop="wheat"):
    return {
        "farmer_id": farmer_id,
        "location": location,
        "quantity": quantity,
        "crop": crop,
    }


# Farmers close together (within 10 km of each other)
CLOSE_FARMERS = [
    make_farmer(1, "Jhajjar",   quantity=100, crop="wheat"),
    make_farmer(2, "Jhajjar",   quantity=150, crop="wheat"),
    make_farmer(3, "Bahadurgarh", quantity=80, crop="wheat"),  # ~8 km from Jhajjar
]

# Farmers far apart — should form 2 separate clusters
FAR_FARMERS = [
    make_farmer(1, "Jhajjar",  quantity=100, crop="wheat"),  # cluster A
    make_farmer(2, "Rohtak",   quantity=200, crop="wheat"),  # cluster B (~40 km away)
]

# Mixed crops
MIXED_CROP_FARMERS = [
    make_farmer(1, "Jhajjar", quantity=100, crop="wheat"),
    make_farmer(2, "Jhajjar", quantity=80,  crop="mustard"),
    make_farmer(3, "Jhajjar", quantity=60,  crop="wheat"),
]


# ============================================================
# validate_farmers()
# ============================================================

class TestValidateFarmers:

    def test_valid_farmers_passes(self):
        validate_farmers(CLOSE_FARMERS)  # should not raise

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_farmers([])

    def test_missing_farmer_id_raises(self):
        with pytest.raises(ValueError, match="farmer_id"):
            validate_farmers([{"quantity": 10, "location": "Delhi", "crop": "wheat"}])

    def test_missing_quantity_raises(self):
        with pytest.raises(ValueError, match="quantity"):
            validate_farmers([{"farmer_id": 1, "location": "Delhi", "crop": "wheat"}])

    def test_missing_location_raises(self):
        with pytest.raises(ValueError, match="location"):
            validate_farmers([{"farmer_id": 1, "quantity": 10, "crop": "wheat"}])

    def test_missing_crop_raises(self):
        with pytest.raises(ValueError, match="crop"):
            validate_farmers([{"farmer_id": 1, "quantity": 10, "location": "Delhi"}])

    def test_zero_quantity_raises(self):
        with pytest.raises(ValueError, match="positive"):
            validate_farmers([{"farmer_id": 1, "quantity": 0, "location": "Delhi", "crop": "wheat"}])

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError, match="positive"):
            validate_farmers([{"farmer_id": 1, "quantity": -50, "location": "Delhi", "crop": "wheat"}])


# ============================================================
# aggregate_quantity()
# ============================================================

class TestAggregateQuantity:

    def test_sums_correctly(self):
        farmers = [make_farmer(i, "A", quantity=q) for i, q in enumerate([100, 150, 80])]
        assert aggregate_quantity(farmers) == 330

    def test_single_farmer(self):
        assert aggregate_quantity([make_farmer(1, "A", quantity=75)]) == 75

    def test_float_quantities(self):
        farmers = [make_farmer(i, "A", quantity=q) for i, q in enumerate([33.5, 66.5])]
        assert aggregate_quantity(farmers) == pytest.approx(100.0)


# ============================================================
# group_by_location()
# ============================================================

class TestGroupByLocation:

    def test_groups_same_location(self):
        farmers = [
            make_farmer(1, "Jhajjar", quantity=100),
            make_farmer(2, "Jhajjar", quantity=200),
        ]
        result = group_by_location(farmers)
        assert "Jhajjar" in result
        assert result["Jhajjar"]["total_quantity"] == 300
        assert len(result["Jhajjar"]["farmers"]) == 2

    def test_separates_different_locations(self):
        farmers = [
            make_farmer(1, "Jhajjar",   quantity=100),
            make_farmer(2, "Bahadurgarh", quantity=150),
        ]
        result = group_by_location(farmers)
        assert "Jhajjar" in result
        assert "Bahadurgarh" in result

    def test_single_farmer(self):
        farmers = [make_farmer(1, "Rohtak", quantity=50)]
        result = group_by_location(farmers)
        assert result["Rohtak"]["total_quantity"] == 50


# ============================================================
# generate_pool_id()
# ============================================================

class TestGeneratePoolId:

    def test_starts_with_pool_prefix(self):
        pool_id = generate_pool_id()
        assert pool_id.startswith("POOL-")

    def test_unique_ids(self):
        ids = {generate_pool_id() for _ in range(100)}
        assert len(ids) == 100  # all unique


# ============================================================
# cluster_farmers_by_proximity()
# ============================================================

class TestClusterFarmersByProximity:

    def test_empty_input_returns_empty(self):
        result = cluster_farmers_by_proximity([])
        assert result == []

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_all_close_farmers_form_one_cluster(self, mock_haversine, mock_coords):
        mock_coords.side_effect = lambda loc: (28.7, 77.1)
        mock_haversine.return_value = 5.0  # everyone is 5 km apart

        farmers = [make_farmer(i, "Jhajjar") for i in range(3)]
        clusters = cluster_farmers_by_proximity(farmers)

        assert len(clusters) == 1
        assert len(clusters[0]) == 3

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_far_farmers_form_two_clusters(self, mock_haversine, mock_coords):
        """
        Farmer 1 (Jhajjar) and Farmer 2 (Rohtak) are 40 km apart →
        they should form 2 separate clusters.
        """
        mock_coords.side_effect = [
            (28.6, 76.9),   # Jhajjar
            (28.9, 76.6),   # Rohtak
        ]
        mock_haversine.return_value = 40.0  # always >10 km

        farmers = [
            make_farmer(1, "Jhajjar"),
            make_farmer(2, "Rohtak"),
        ]
        clusters = cluster_farmers_by_proximity(farmers)

        assert len(clusters) == 2
        assert len(clusters[0]) == 1
        assert len(clusters[1]) == 1

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_mixed_proximity_correct_split(self, mock_haversine, mock_coords):
        """
        Farmer 1 & 2 are close (5 km), Farmer 3 is far (50 km).
        Expected: cluster A = [F1, F2], cluster B = [F3]
        """
        mock_coords.side_effect = lambda loc: (28.7, 77.1)

        # haversine is called to compare seed vs each other farmer
        # seed=F1 vs F2 → 5 km (join), seed=F1 vs F3 → 50 km (don't join)
        mock_haversine.side_effect = [5.0, 50.0]

        farmers = [
            make_farmer(1, "Jhajjar"),
            make_farmer(2, "Bahadurgarh"),
            make_farmer(3, "Rohtak"),
        ]
        clusters = cluster_farmers_by_proximity(farmers)

        assert len(clusters) == 2
        assert len(clusters[0]) == 2  # F1 + F2
        assert len(clusters[1]) == 1  # F3

    def test_single_farmer_forms_one_cluster(self):
        with patch("app.services.virtual_pooling.pool_engine.get_coordinates") as mock_coords:
            mock_coords.return_value = (28.7, 77.1)
            farmers = [make_farmer(1, "Delhi")]
            clusters = cluster_farmers_by_proximity(farmers)
            assert len(clusters) == 1
            assert clusters[0][0]["farmer_id"] == 1


# ============================================================
# create_auto_pools()
# ============================================================

class TestCreateAutoPools:

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_returns_list_of_pools(self, mock_haversine, mock_coords):
        mock_coords.return_value = (28.7, 77.1)
        mock_haversine.return_value = 3.0  # everyone close

        pools = create_auto_pools(CLOSE_FARMERS)
        assert isinstance(pools, list)
        assert len(pools) > 0

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_pool_has_required_keys(self, mock_haversine, mock_coords):
        mock_coords.return_value = (28.7, 77.1)
        mock_haversine.return_value = 3.0

        pools = create_auto_pools(CLOSE_FARMERS)
        pool = pools[0]

        for key in ["pool_id", "crop", "farmers", "total_quantity", "location_summary", "centroid"]:
            assert key in pool, f"Missing key: {key}"

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_centroid_is_tuple_of_two_floats(self, mock_haversine, mock_coords):
        mock_coords.return_value = (28.7, 77.1)
        mock_haversine.return_value = 3.0

        pools = create_auto_pools(CLOSE_FARMERS)
        centroid = pools[0]["centroid"]

        assert isinstance(centroid, tuple)
        assert len(centroid) == 2

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_separate_crops_make_separate_pools(self, mock_haversine, mock_coords):
        mock_coords.return_value = (28.7, 77.1)
        mock_haversine.return_value = 3.0  # all close

        pools = create_auto_pools(MIXED_CROP_FARMERS)
        crops_in_pools = {p["crop"] for p in pools}

        assert "wheat" in crops_in_pools
        assert "mustard" in crops_in_pools

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_far_apart_same_crop_makes_two_pools(self, mock_haversine, mock_coords):
        mock_coords.side_effect = lambda loc: (28.7, 77.1)
        mock_haversine.return_value = 40.0  # always far

        pools = create_auto_pools(FAR_FARMERS)

        # Both are wheat but 40 km apart → 2 separate pools
        assert len(pools) == 2
        assert all(p["crop"] == "wheat" for p in pools)

    @patch("app.services.virtual_pooling.pool_engine.get_coordinates")
    @patch("app.services.virtual_pooling.pool_engine.haversine")
    def test_total_quantity_correct(self, mock_haversine, mock_coords):
        mock_coords.return_value = (28.7, 77.1)
        mock_haversine.return_value = 3.0

        farmers = [
            make_farmer(1, "Jhajjar", quantity=100, crop="wheat"),
            make_farmer(2, "Jhajjar", quantity=200, crop="wheat"),
        ]
        pools = create_auto_pools(farmers)
        assert pools[0]["total_quantity"] == 300

    def test_empty_farmers_raises(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            create_auto_pools([])

    def test_invalid_farmer_raises(self):
        with pytest.raises(ValueError):
            create_auto_pools([{"farmer_id": 1}])  # missing quantity, location, crop
