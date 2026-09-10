# 🌾 Fasal Nirnay (फसल निर्णय)

> **Crop Decision** — An AI-powered advisory platform for Indian farmers to predict mandi prices, assess crop grades, and receive contextual farming recommendations.

---

## 📌 Overview

Fasal Nirnay combines historical mandi data, real-time weather intelligence, and news signals to help farmers make smarter selling and harvesting decisions. It uses a hybrid ML pipeline (XGBoost + LSTM + LightGBM) to predict crop prices and grades across major agricultural states in India.

---

## ✨ Features

- **Mandi Price Prediction** — Forecasts minimum price (₹/quintal) using weather, historical prices, and seasonal patterns
- **Crop Grade Classification** — Predicts produce grade (FAQ, Best, etc.) with confidence scores
- **Weather Intelligence** — Integrates Open-Meteo forecasts with synthetic historical data (2001–2024)
- **News-Driven Advisory** — Pulls mandi updates, government policies, and weather disruption signals via GNews/NewsAPI
- **AI Chatbot (Advisory Engine)** — LLM-powered context-aware recommendations with mock fallback for low-connectivity areas
- **Speech Layer (Planned)** — STT/TTS endpoints designed for Bhashini (Indic language) and Google Cloud Speech integration

---

## 🗂️ Project Structure

```
fasal-nirnay/
├── app/                        # FastAPI backend (modular)
├── .vscode/                    # Editor config
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── __init__.py
│
├── fasal_nirnay_clean.ipynb    # Data cleaning & EDA notebook
├── fasalnirnay-xgb-lstm.ipynb  # XGBoost + LSTM hybrid model notebook
│
├── price_model.pkl             # LGB regression model (Min_Price)
├── grade_model.pkl             # LGB classification model (Grade)
├── xgb_price_model.pkl         # XGBoost price model
├── lstm_price_model.pt         # LSTM price model (PyTorch)
├── meta_stacker.pkl            # Ensemble stacking meta-learner
│
├── price_imputer.pkl           # Imputer for price features
├── grade_imputer.pkl           # Imputer for grade features
├── label_encoders.pkl          # Label encoders (commodity, state, etc.)
├── grade_label_encoder.pkl     # Label encoder for grade classes
├── lstm_seq_scaler.pkl         # Scaler for LSTM input sequences
└── lstm_y_scaler.pkl           # Scaler for LSTM price targets
```

---

## 🧠 ML Pipeline

### Models

| Model | Type | Target | Algorithm |
|---|---|---|---|
| Price Model | Regression | `Min_Price` (₹/quintal) | LightGBM |
| Grade Model | Classification | `Grade` (FAQ, Best, etc.) | LightGBM |
| Hybrid Price | Regression | `Min_Price` | XGBoost + LSTM (stacked) |

### Data Flow

```
Weather CSV ──┐
              ├──► Merge on (state + district + date)
Mandi ZIPs ───┘
              │
              ▼
       Feature Engineering
       ┌─────────────────────────────────────┐
       │ Calendar (cyclical month/doy)       │
       │ Weather (VPD, heat stress, etc.)    │
       │ Soil composite stress index         │
       │ Price lags (1d / 7d / 30d)          │
       │ Rolling mean & std (7/14/30d)       │
       │ Encoded categoricals                │
       └─────────────────────────────────────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
Price Model        Grade Model
(xgb-lstm Regressor)    (LGB Classifier)
     │                 │
  ₹ prediction     Grade label
  SELL / HOLD      + confidence %
```

### Train / Validation Split

Temporal split to prevent data leakage:
- **Train**: 2001–2021
- **Validation**: 2022–2024

### Key Feature Engineering

| Feature | Description |
|---|---|
| `temp_range` | Max − Min temperature (harvest stress indicator) |
| `heat_stress` | Flag if Tmax > 40°C |
| `frost_risk` | Flag if Tmin < 4°C |
| `drought_flag` | Flag if rainfall < 2mm AND humidity < 30% |
| `vpd` | Vapour Pressure Deficit (plant water stress) |
| `soil_stress` | Composite of soil temperature + inverse of moisture |
| `month_sin/cos` | Cyclical month encoding |
| `doy_sin/cos` | Cyclical day-of-year encoding |
| `price_lag1/7/30` | Previous day / week / month prices |
| `price_roll7/14/30` | Rolling mean prices |
| `price_std7/14/30` | Rolling price volatility |
| `daily_listings` | Market supply proxy (entries per commodity/state/day) |

---

## 🌦️ Weather Coverage

Real-time forecasts via Open-Meteo + synthetic historical data (2001–2024) for representative agricultural hubs:

| State | Cities |
|---|---|
| Punjab | Amritsar, Ludhiana, Patiala, Pathankot, Bathinda |
| Haryana | Hisar, Karnal, Kaithal, Rohtak, Sirsa, Gurugram |
| Uttar Pradesh | Lucknow, Kanpur, Varanasi, Bareilly, Meerut, Gorakhpur, Agra |
| Rajasthan | Jaipur, Jodhpur, Udaipur, Kota, Bikaner, Mount Abu |
| Anchors | Delhi, Chandigarh |

---

## 🔧 Setup & Installation

### Prerequisites

- Python 3.9+
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

Or for the ML pipeline only:

```bash
pip install pandas numpy scikit-learn joblib pyarrow lightgbm torch
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Expected variables (refer to `.env.example`):
```
OPENAI_API_KEY=...
GNEWS_API_KEY=...
NEWSAPI_KEY=...
```

### Run the backend

```bash
uvicorn app.main:app --reload
```

---

## 🚀 Inference Example

```python
import joblib

price_model   = joblib.load("price_model.pkl")
price_imputer = joblib.load("price_imputer.pkl")
grade_model   = joblib.load("grade_model.pkl")
grade_imputer = joblib.load("grade_imputer.pkl")
grade_enc     = joblib.load("grade_label_encoder.pkl")
le_dict       = joblib.load("label_encoders.pkl")

from mandi_pipeline import predict_best_sell_window, predict_grade

weather_today = {
    "temperature_mean": 28.5, "temperature_max": 35.0, "temperature_min": 22.0,
    "humidity": 60.0, "precipitation": 0.0, "rainfall": 0.0,
    "wind_speed": 12.0, "wind_direction": 180,
    "soil_temperature_0_7cm": 26.0, "soil_moisture_0_7cm": 0.25,
    "solar_radiation": 220.0,
    "year": 2025, "month": 4, "quarter": 2, "week_of_year": 15,
    "day_of_year": 105,
    # ... (cyclical encodings, stress flags, etc.)
}

result = predict_best_sell_window(
    weather_row=weather_today,
    commodity_enc=le_dict["Commodity"].transform(["Wheat"])[0],
    variety_enc=le_dict["Variety"].transform(["Sharbati"])[0],
    state_enc=le_dict["state_norm"].transform(["Punjab"])[0],
    district_enc=le_dict["district_norm"].transform(["ludhiana"])[0],
    price_history=[2100, 2110, 2095, ...],  # last 30 days
    price_model=price_model,
    price_imputer=price_imputer,
)
# → {"predicted_price": 2145.30, "recommendation": "SELL"}

grade_result = predict_grade(
    weather_row=weather_today,
    commodity_enc=le_dict["Commodity"].transform(["Wheat"])[0],
    variety_enc=le_dict["Variety"].transform(["Sharbati"])[0],
    state_enc=le_dict["state_norm"].transform(["Punjab"])[0],
    district_enc=le_dict["district_norm"].transform(["ludhiana"])[0],
    grade_model=grade_model,
    grade_imputer=grade_imputer,
    grade_encoder=grade_enc,
)
# → {"predicted_grade": "FAQ", "confidence": 0.87, "all_probabilities": {...}}
```

---

## 🏗️ Backend Architecture

The FastAPI backend follows a modular, API-first design:

- **Weather Service** — Fetches and merges forecast + historical weather data
- **News Service** — Categorizes mandi/policy/weather news into advisory signals
- **Chatbot Service** — Combines farmer query + weather + news + price prediction into LLM-driven recommendations; includes mock fallback for offline/poor-connectivity scenarios
- **Speech Service** *(planned)* — STT/TTS endpoints for Indic language support via Bhashini

---

## 📋 Data Requirements

Mandi ZIP files (one per year, e.g. `2001.zip`) must contain CSVs with exactly these columns:

```
State, District, Market, Commodity, Variety, Grade,
Arrival_Date, Min_Price, Commodity_Code
```

---

## 📝 Notes

- District-to-weather location matching uses exact string match first, then falls back to state-level daily average weather.
- Price model accuracy improves significantly when `price_lag1` is available. For sparse commodities, rolling features carry more weight.
- Grade model uses `class_weight="balanced"` to handle skewed grade distributions (most produce graded FAQ).

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI (Python) |
| ML | LightGBM, XGBoost, PyTorch (LSTM), scikit-learn |
| Weather API | Open-Meteo |
| News API | GNews, NewsAPI |
| LLM | OpenAI API |
| Speech *(planned)* | Google Cloud Speech, Bhashini |

---

## 📄 License

This project does not currently specify a license.

---

*Fasal Nirnay — empowering Indian farmers with data-driven crop decisions.*
