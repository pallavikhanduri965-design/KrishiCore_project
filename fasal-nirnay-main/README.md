# 🌾 Fasal Nirnay (फसल निर्णय) — Backend API

> **AI-Powered Agricultural Advisory, Mandi Price & Quality Forecasting, and Virtual Pooling Engine for Indian Farmers.**

---

## 📌 Overview

**Fasal Nirnay** is a high-performance FastAPI backend designed to empower farmers and Farmer Producer Organizations (FPOs) with:
1. **Virtual Produce Pooling & Logistics Optimization** — Auto-clustering farmers within a 10 km geographic radius and computing net profit across regional mandis accounting for transport costs and quality grading.
2. **Hybrid ML Price & Grade Forecasting** — Ensemble model stack combining **XGBoost + LightGBM + PyTorch LSTM** for mandi price forecasting and quality grade classification.
3. **Contextual Farming Advisory** — LLM-driven advisory integrating live weather forecasts and agricultural news.
4. **Indic Speech Services** — Speech-to-Text and Text-to-Speech endpoints with Sarvam AI / Bhashini integration.

---

## 🗂️ Project Structure

```
fasal-nirnay/
├── app/
│   ├── main.py                      # FastAPI application entry point & router setup
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py                # Pydantic Settings & environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py               # Centralized Pydantic v2 data models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pooling.py               # POST /pool/ (Virtual Pooling & Optimization)
│   │   ├── weather.py               # GET /weather/forecast
│   │   ├── news.py                  # GET /news/latest
│   │   ├── chat.py                  # POST /chat/query
│   │   └── speech.py                # POST /speech/stt, POST /speech/tts
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prediction.py            # ML Model loader & inference pipeline
│   │   ├── weather_service.py       # WeatherAPI integration with mock fallback
│   │   ├── news_service.py          # GNews API integration
│   │   ├── chat_service.py          # Advisory generation engine
│   │   ├── speech_service.py        # Sarvam AI STT & TTS integration
│   │   └── virtual_pooling/
│   │       ├── __init__.py
│   │       ├── pool_engine.py       # Geo-clustering & aggregation (10km radius)
│   │       └── optimizer.py         # Truck-capacity transport & net-payout optimizer
│   └── utils/
│       ├── __init__.py
│       └── geo.py                   # OpenCage geocoding & Haversine distance
│
├── conftest.py                      # Shared pytest fixtures
├── test_geo.py                      # Geographic calculation & geocoding tests
├── test_optimizer.py                # Transport & mandi profit optimizer tests
├── test_pool_engine.py              # Proximity clustering & pooling tests
├── test_pooling.py                  # FastAPI route integration tests
├── requirements.txt                 # Backend & ML dependencies
├── .env.example                     # Environment configuration template
└── README.md                        # Documentation
```

---

## 🚀 API Endpoints

### 1. Virtual Pooling & Optimization (`POST /pool/`)
Clusters farmers by produce type and geographic proximity (10 km radius), runs ML price/grade inference for candidate mandis, and optimizes net payout after logistics.

**Request:**
```json
{
  "farmers": [
    { "farmer_id": 1, "quantity": 50.0, "location": "Jhajjar", "crop": "wheat" },
    { "farmer_id": 2, "quantity": 80.0, "location": "Bahadurgarh", "crop": "wheat" }
  ],
  "price_history": [2150.0, 2180.0, 2200.0]
}
```

**Response:**
```json
{
  "status": "success",
  "total_pools": 1,
  "pools": [
    {
      "pool_id": "POOL-A1B2C3D4",
      "crop": "wheat",
      "total_quantity": 130.0,
      "num_farmers": 2,
      "centroid": { "lat": 28.65, "lon": 76.79 },
      "recommendation": {
        "mandi": "Azadpur",
        "price": 2250.0,
        "predicted_price": 2250.0,
        "grade": "FAQ",
        "grade_multiplier": 1.0,
        "grade_confidence": 0.88,
        "effective_price": 2250.0,
        "distance_km": 42.5,
        "trucks_needed": 1,
        "transport_cost": 8.17,
        "net_price": 2241.83
      },
      "total_earnings": 291437.9
    }
  ]
}
```

---

### 2. Weather Forecast (`GET /weather/forecast`)
Fetches live weather and multi-day agricultural forecast.
- Query Params: `location=Pune`, `crop=wheat`, `days=3`

---

### 3. Agricultural News (`GET /news/latest`)
Fetches localized market and crop news.
- Query Params: `location=Maharashtra`, `crop=sugarcane`, `category=mandi`

---

### 4. AI Advisory Chat (`POST /chat/query`)
Context-aware advisory chatbot combining user inquiry, localized weather, and market updates.

---

### 5. Speech-to-Text & Text-to-Speech (`POST /speech/stt`, `POST /speech/tts`)
Voice interface supporting Indic languages for rural farmers.

---

## 🔧 Setup & Installation

### 1. Prerequisites
- Python 3.10+
- pip / virtualenv

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
```

### 4. Run the API Server
```bash
uvicorn app.main:app --reload --port 8000
```

Interactive OpenAPI documentation available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🧪 Running Tests

Run the full pytest suite:
```bash
pytest -v
```

Tests cover:
- `test_geo.py`: Haversine distance, centroid calculation, geocoding cache & error handling.
- `test_pool_engine.py`: Farmer validation, quantity aggregation, 10km proximity clustering.
- `test_optimizer.py`: Truck-capacity aware transport cost, net price math, best mandi selection.
- `test_pooling.py`: Route validation, error codes (400/422/500), multi-crop & multi-cluster pools.

---

*Fasal Nirnay — Empowering Indian Agriculture with AI & Virtual Pooling.*

