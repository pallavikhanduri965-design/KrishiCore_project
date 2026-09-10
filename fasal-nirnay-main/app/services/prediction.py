"""
Prediction Service — FasalNirnay AI

Provides per-mandi price AND grade predictions for a given crop.
These are consumed by the Virtual Pooling optimizer to compute
real net profit after logistics costs and grade adjustments.

Flow:
    get_mandi_predictions(crop)
        └── for each mandi in MANDI_CONFIG:
                build_features(crop, mandi)  → structured feature row
                price model stack (XGB + LGB + LSTM → meta)  → ₹/quintal
                grade model (LGB classifier)  → grade label + confidence
            return list of { mandi, state, predicted_price, grade, grade_confidence }
"""

import math
import numpy as np
import joblib
import torch
import torch.nn as nn
from typing import List, Dict

# ─────────────────────────────────────────────
# MANDI CONFIG
# Maps each mandi name to the state/district that
# label_encoders expects. Extend this as you add mandis.
# ─────────────────────────────────────────────
MANDI_CONFIG: List[Dict] = [
    {"mandi": "Azadpur",   "state": "Delhi",     "district": "delhi"},
    {"mandi": "Karnal",    "state": "Haryana",   "district": "karnal"},
    {"mandi": "Rohtak",    "state": "Haryana",   "district": "rohtak"},
    {"mandi": "Najafgarh", "state": "Delhi",     "district": "delhi"},
    {"mandi": "Jaipur",    "state": "Rajasthan", "district": "jaipur"},
    {"mandi": "Alwar",     "state": "Rajasthan", "district": "alwar"},
    {"mandi": "Hisar",     "state": "Haryana",   "district": "hisar"},
    {"mandi": "Sonipat",   "state": "Haryana",   "district": "sonipat"},
]


# ─────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────
try:
    xgb_model    = joblib.load("app/models/xgb_price_model.pkl")
    price_model  = joblib.load("app/models/price_model.pkl")
    meta_model   = joblib.load("app/models/meta_stacker.pkl")
    grade_model  = joblib.load("app/models/grade_model.pkl")

    price_imputer = joblib.load("app/models/price_imputer.pkl")
    grade_imputer = joblib.load("app/models/grade_imputer.pkl")
    grade_encoder = joblib.load("app/models/grade_label_encoder.pkl")

    label_encoders = joblib.load("app/models/label_encoders.pkl")

    lstm_scaler   = joblib.load("app/models/lstm_seq_scaler.pkl")
    lstm_y_scaler = joblib.load("app/models/lstm_y_scaler.pkl")

    print("✅ All models loaded successfully")

except Exception as e:
    print(f"❌ Model loading error: {e}")
    xgb_model = price_model = meta_model = grade_model = None
    price_imputer = grade_imputer = grade_encoder = label_encoders = None
    lstm_scaler = lstm_y_scaler = None


# ─────────────────────────────────────────────
# LSTM ARCHITECTURE  (must match training)
# ─────────────────────────────────────────────
class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=50, batch_first=True)
        self.fc   = nn.Linear(50, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


try:
    lstm_model = LSTMModel()
    lstm_model.load_state_dict(
        torch.load("app/models/lstm_price_model.pt", map_location="cpu")
    )
    lstm_model.eval()
    print("✅ LSTM model loaded")
except Exception as e:
    print(f"❌ LSTM load error: {e}")
    lstm_model = None


# ─────────────────────────────────────────────
# SAFE LABEL ENCODING
# Returns 0 (unknown bucket) if value not seen during training.
# ─────────────────────────────────────────────
def safe_encode(encoder_key: str, value: str) -> int:
    """
    Look up a label encoder by key and encode `value`.
    Falls back to 0 if the value was unseen during training
    so the pipeline never crashes on new locations or crops.
    """
    if label_encoders is None:
        return 0
    le = label_encoders.get(encoder_key)
    if le is None:
        return 0
    try:
        return int(le.transform([value])[0])
    except ValueError:
        return 0   # unseen value → unknown bucket


# ─────────────────────────────────────────────
# FEATURE BUILDER
#
# ⚠  IMPORTANT FOR YOUR TEAM:
#    The feature order here MUST match the column order used during
#    training in mandi_pipeline.py.
#    Weather + price history fields are left as np.nan and filled
#    by the imputer using training-time medians.
#    Replace the placeholder sections once those pipelines are wired in.
# ─────────────────────────────────────────────
def build_features(crop: str, state: str, district: str) -> np.ndarray:
    """
    Build a structured feature row for price & grade models.

    Features:
        [commodity_enc, variety_enc, state_enc, district_enc,
         month_sin, month_cos, doy_sin, doy_cos,
         heat_stress, frost_risk, drought_flag,
         price_lag1, price_lag7, price_lag30,
         price_roll7, price_roll14, price_roll30]
    """
    import datetime
    now   = datetime.datetime.now()
    month = now.month
    doy   = now.timetuple().tm_yday

    # Categorical encodings
    commodity_enc = safe_encode("Commodity",    crop.capitalize())
    variety_enc   = safe_encode("Variety",       "Other")
    state_enc     = safe_encode("state_norm",    state.lower())
    district_enc  = safe_encode("district_norm", district.lower())

    # Cyclical time encoding
    month_sin = math.sin(2 * math.pi * month / 12)
    month_cos = math.cos(2 * math.pi * month / 12)
    doy_sin   = math.sin(2 * math.pi * doy / 365)
    doy_cos   = math.cos(2 * math.pi * doy / 365)

    # ── Weather placeholders ──────────────────────────────────────────
    # TODO: replace with live call to your weather service once integrated
    heat_stress  = 0
    frost_risk   = 0
    drought_flag = 0

    # ── Price history placeholders ────────────────────────────────────
    # TODO: replace with real DB lookup (last 30 days of arrivals)
    price_lag1   = np.nan
    price_lag7   = np.nan
    price_lag30  = np.nan
    price_roll7  = np.nan
    price_roll14 = np.nan
    price_roll30 = np.nan

    feature_row = np.array([[
        commodity_enc, variety_enc, state_enc, district_enc,
        month_sin, month_cos, doy_sin, doy_cos,
        heat_stress, frost_risk, drought_flag,
        price_lag1, price_lag7, price_lag30,
        price_roll7, price_roll14, price_roll30,
    ]], dtype=float)

    return feature_row


# ─────────────────────────────────────────────
# LSTM SEQUENCE BUILDER
# ─────────────────────────────────────────────
def build_lstm_sequence(price_history: list = None) -> torch.Tensor:
    """
    Build a (1, 10, 1) tensor for the LSTM.

    `price_history` — last N daily prices (₹/quintal) for this crop+mandi.
    If fewer than 10 values, zero-padded on the left.
    If None, all zeros are used (imputer covers it).
    """
    SEQ_LEN = 10

    if price_history and len(price_history) > 0:
        hist = price_history[-SEQ_LEN:]
        pad  = [0.0] * (SEQ_LEN - len(hist))
        seq  = np.array(pad + hist, dtype=float).reshape(-1, 1)
    else:
        seq = np.zeros((SEQ_LEN, 1), dtype=float)

    if lstm_scaler is not None:
        seq = lstm_scaler.transform(seq)

    return torch.tensor(seq.reshape(1, SEQ_LEN, 1), dtype=torch.float32)


# ─────────────────────────────────────────────
# PRICE PREDICTION  (XGB + LGB + LSTM → meta stacker)
# ─────────────────────────────────────────────
def predict_price(crop: str, state: str, district: str,
                  price_history: list = None) -> float:
    """
    Run the full model stack and return predicted ₹/quintal for this
    crop at the given mandi (identified by state + district).
    """
    if any(m is None for m in [xgb_model, price_model, meta_model, price_imputer]):
        raise RuntimeError("Price models not loaded — check model file paths")

    X_raw = build_features(crop, state, district)
    X     = price_imputer.transform(X_raw)

    xgb_pred   = float(xgb_model.predict(X)[0])
    price_pred = float(price_model.predict(X)[0])

    lstm_input = build_lstm_sequence(price_history)
    with torch.no_grad():
        lstm_raw = lstm_model(lstm_input).item() if lstm_model else 0.0
    lstm_pred = float(lstm_y_scaler.inverse_transform([[lstm_raw]])[0][0]) \
                if lstm_y_scaler else lstm_raw

    stacked     = np.array([[xgb_pred, price_pred, lstm_pred]])
    final_price = float(meta_model.predict(stacked)[0])

    return final_price


# ─────────────────────────────────────────────
# GRADE PREDICTION
# ─────────────────────────────────────────────
def predict_grade(crop: str, state: str, district: str) -> Dict:
    """
    Predict the expected crop grade at a given mandi location.

    Returns:
        {
            "grade":       "FAQ",
            "confidence":  0.87,
            "all_grades":  { "FAQ": 0.87, "Best": 0.09, "Common": 0.04 }
        }
    """
    if any(m is None for m in [grade_model, grade_imputer, grade_encoder]):
        # Graceful fallback — FAQ is the most common grade in training data
        return {"grade": "FAQ", "confidence": 1.0, "all_grades": {"FAQ": 1.0}}

    X_raw = build_features(crop, state, district)
    X     = grade_imputer.transform(X_raw)

    probs     = grade_model.predict_proba(X)[0]
    top_idx   = int(np.argmax(probs))
    top_grade = grade_encoder.inverse_transform([top_idx])[0]
    top_conf  = float(probs[top_idx])

    all_grades = {
        grade_encoder.inverse_transform([i])[0]: round(float(p), 4)
        for i, p in enumerate(probs)
    }

    return {
        "grade":      top_grade,
        "confidence": round(top_conf, 4),
        "all_grades": all_grades,
    }


# ─────────────────────────────────────────────
# PUBLIC API  —  called by the optimizer
# ─────────────────────────────────────────────
def get_mandi_predictions(crop: str, price_history: list = None) -> List[Dict]:
    """
    For every mandi in MANDI_CONFIG, run both models and return:

        [
            {
                "mandi":            "Azadpur",
                "state":            "Delhi",
                "predicted_price":  2145.30,    # ₹/quintal from model stack
                "grade":            "FAQ",       # from grade classifier
                "grade_confidence": 0.87,
                "all_grades":       { "FAQ": 0.87, "Best": 0.09, ... }
            },
            ...
        ]

    Mandis where prediction fails are skipped with a warning rather than
    crashing the whole request.
    """
    print(f"\n📊 Running predictions for crop: {crop}")
    results = []

    for mandi_info in MANDI_CONFIG:
        mandi    = mandi_info["mandi"]
        state    = mandi_info["state"]
        district = mandi_info["district"]

        try:
            price_result = predict_price(crop, state, district, price_history)
            grade_result = predict_grade(crop, state, district)

            results.append({
                "mandi":            mandi,
                "state":            state,
                "predicted_price":  round(price_result, 2),
                "grade":            grade_result["grade"],
                "grade_confidence": grade_result["confidence"],
                "all_grades":       grade_result["all_grades"],
            })

            print(
                f"  {mandi:12s} | ₹{price_result:7.2f}/q "
                f"| grade: {grade_result['grade']} "
                f"({grade_result['confidence'] * 100:.1f}%)"
            )

        except Exception as e:
            print(f"  ⚠ Skipping {mandi}: {e}")
            continue

    if not results:
        raise RuntimeError(
            f"Prediction failed for all mandis for crop '{crop}'. "
            "Check model files and label encoders."
        )

    return results
