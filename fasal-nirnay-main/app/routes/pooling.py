"""
Virtual Pooling Routes — FasalNirnay AI
=======================================
Exposes HTTP endpoints for auto-pooling and mandi profit optimization.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.models.schemas import PoolRequest, PoolResponse, Farmer
from app.services.virtual_pooling.pool_engine import create_auto_pools
from app.services.virtual_pooling.optimizer import optimize_pool
from app.services.prediction import get_mandi_predictions

router = APIRouter(prefix="/pool", tags=["Virtual Pooling"])


# ─────────────────────────────────────────────
# MAIN API
# ─────────────────────────────────────────────
@router.post("/", response_model=PoolResponse)
def pool_and_optimize(data: PoolRequest):
    """
    POST /pool/

    Step 1 — Group farmers by crop, cluster within 10 km radius.
             Farmers >10 km apart in the same crop form separate pools.

    Step 2 — For each pool:
             a. Run price model stack per mandi.
             b. Run grade model classifier per mandi.
             c. Compute net profit:
                    effective_price = predicted_price × grade_multiplier
                    net_price       = effective_price − transport_cost/q
             d. Return the mandi with the highest net_price.
    """
    try:
        farmers_list = [
            f.model_dump() if hasattr(f, "model_dump") else f.dict()
            for f in data.farmers
        ]
        price_history = data.price_history

        # ── Step 1: build geo-clustered pools ────────────────────────
        pools = create_auto_pools(farmers_list)

        if not pools:
            raise ValueError(
                "No valid pools could be created. "
                "Ensure at least one valid farmer group is provided within geographic bounds."
            )

        # ── Step 2: predict + optimize each pool ─────────────────────
        results = []

        for pool in pools:
            crop = pool["crop"]

            # Get per-mandi price + grade predictions from the ML models / baseline
            try:
                mandi_data = get_mandi_predictions(crop, price_history)
            except Exception as pred_err:
                results.append({
                    "pool_id": pool["pool_id"],
                    "crop":    crop,
                    "error":   f"Prediction error for crop {crop}: {str(pred_err)}",
                })
                continue

            if not mandi_data:
                results.append({
                    "pool_id": pool["pool_id"],
                    "crop":    crop,
                    "error":   f"No mandi predictions available for crop: {crop}",
                })
                continue

            # Run optimizer: applies grade multiplier + truck transport cost equation
            result = optimize_pool(pool, mandi_data)
            results.append(result)

        return {
            "status":      "success",
            "total_pools": len(results),
            "pools":       results,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

