from fastapi import APIRouter, HTTPException
from app.services.virtual_pooling.pool_engine import create_auto_pools
from app.services.virtual_pooling.optimizer import optimize_pool
from app.services.prediction import get_mandi_predictions
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/pool", tags=["Virtual Pooling"])


# ─────────────────────────────────────────────
# REQUEST MODELS
# ─────────────────────────────────────────────
class Farmer(BaseModel):
    farmer_id: int
    quantity:  float       # quintals
    location:  str         # village / city — geocoded via OpenCage
    crop:      str         # e.g. "wheat", "mustard"


class PoolRequest(BaseModel):
    farmers:       List[Farmer]
    price_history: Optional[List[float]] = None
    # Optional: last N days of prices (₹/quintal) for the crop.
    # If provided, passed to LSTM for better price forecasting.
    # e.g. [2050.0, 2080.0, 2095.0, 2110.0]


# ─────────────────────────────────────────────
# MAIN API
# ─────────────────────────────────────────────
@router.post("/")
def pool_and_optimize(data: PoolRequest):
    """
    POST /pool/

    Step 1 — Group farmers by crop, cluster within 10 km radius.
             Farmers >10 km apart in the same crop = separate pools.

    Step 2 — For each pool:
             a. Run price model (XGB + LGB + LSTM meta stack) per mandi.
             b. Run grade model (LGB classifier) per mandi.
             c. Compute net profit:
                    effective_price = predicted_price × grade_multiplier
                    net_price       = effective_price − transport_cost/q
             d. Return the mandi with the highest net_price.

    Request body:
        {
            "farmers": [
                { "farmer_id": 1, "quantity": 50, "location": "Jhajjar", "crop": "wheat" },
                { "farmer_id": 2, "quantity": 80, "location": "Rohtak",  "crop": "wheat" }
            ],
            "price_history": [2050, 2060, 2080]   // optional, last N days
        }
    """
    try:
        farmers_list  = [f.dict() for f in data.farmers]
        price_history = data.price_history  # may be None

        # ── Step 1: build geo-clustered pools ────────────────────────
        pools = create_auto_pools(farmers_list)

        if not pools:
            raise ValueError(
                "No valid pools could be created. "
                "Ensure at least two farmers with the same crop are within 10 km."
            )

        # ── Step 2: predict + optimize each pool ─────────────────────
        results = []

        for pool in pools:
            crop = pool["crop"]

            # Get per-mandi price + grade predictions from the ML models
            mandi_data = get_mandi_predictions(crop, price_history)

            if not mandi_data:
                results.append({
                    "pool_id": pool["pool_id"],
                    "crop":    crop,
                    "error":   f"No mandi predictions available for crop: {crop}",
                })
                continue

            # Run optimizer: applies grade multiplier + transport cost equation
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
