"""
Pydantic Schemas
================
All request and response models for the FasalNirnay API.
FastAPI uses these for automatic validation, serialization,
and documentation generation (visible at /docs).
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ==============================================================================
# WEATHER SCHEMAS
# ==============================================================================

class ForecastDay(BaseModel):
    """A single day in the weather forecast."""
    day:             int   = Field(..., description="Day number (1 = today)")
    max_temp_c:      float = Field(..., description="Maximum temperature in Celsius")
    min_temp_c:      float = Field(..., description="Minimum temperature in Celsius")
    condition:       str   = Field(..., description="Weather condition text")
    rain_chance_pct: int   = Field(..., description="Chance of rain as a percentage")


class WeatherResponse(BaseModel):
    """Response model for the /weather/forecast endpoint."""
    location:       str             = Field(..., description="Location name")
    crop:           str             = Field(..., description="Crop for which forecast was requested")
    current_temp_c: float           = Field(..., description="Current temperature in Celsius")
    condition:      str             = Field(..., description="Current weather condition")
    humidity:       int             = Field(..., description="Humidity percentage")
    wind_kph:       float           = Field(..., description="Wind speed in km/h")
    forecast:       List[ForecastDay] = Field(..., description="Multi-day forecast")
    source:         str             = Field(..., description="Data source: 'weatherapi.com' or 'mock'")


# ==============================================================================
# NEWS SCHEMAS
# ==============================================================================

class NewsArticle(BaseModel):
    """A single news article."""
    title:        str = Field(..., description="Article headline")
    description:  str = Field(..., description="Short summary of the article")
    source:       str = Field(..., description="Publication name")
    published_at: str = Field(..., description="ISO 8601 publication timestamp")
    url:          str = Field(..., description="Link to the full article")


class NewsResponse(BaseModel):
    """Response model for the /news/latest endpoint."""
    location:  str               = Field(..., description="Region filter used")
    crop:      str               = Field(..., description="Crop filter used")
    category:  Optional[str]     = Field(None, description="Category filter used, if any")
    total:     int               = Field(..., description="Total number of articles returned")
    articles:  List[NewsArticle] = Field(..., description="List of news articles")
    source:    str               = Field(..., description="Data source: 'gnews.io' or 'mock'")


# ==============================================================================
# CHAT SCHEMAS
# ==============================================================================

class ChatRequest(BaseModel):
    """Request body for POST /chat/query."""
    farmer_query:    str  = Field(..., description="The farmer's question in their own words")
    location:        str  = Field(..., description="Farmer's location, e.g. 'Nashik, Maharashtra'")
    crop:            str  = Field(..., description="Current crop, e.g. 'onion'")
    language:        str  = Field("English", description="Preferred response language, e.g. 'Hindi', 'Marathi'")
    include_weather: bool = Field(True,  description="Whether to include weather context in the response")
    include_news:    bool = Field(False, description="Whether to include news context in the response")

    class Config:
        json_schema_extra = {
            "example": {
                "farmer_query":    "When should I irrigate my onion crop?",
                "location":        "Nashik, Maharashtra",
                "crop":            "onion",
                "language":        "Hindi",
                "include_weather": True,
                "include_news":    False,
            }
        }


class ChatContextUsed(BaseModel):
    """Metadata about what context was included in the AI response."""
    weather_included: bool
    news_included:    bool


class ChatResponse(BaseModel):
    """Response model for POST /chat/query."""
    answer:       str             = Field(..., description="The AI-generated advisory answer")
    language:     str             = Field(..., description="Language of the response")
    context_used: ChatContextUsed = Field(..., description="What context was used to generate the answer")
    source:       str             = Field(..., description="LLM provider used, or 'mock'")


# ==============================================================================
# SPEECH SCHEMAS
# ==============================================================================

class STTRequest(BaseModel):
    """Request body for POST /speech/stt (Speech-to-Text)."""
    base64_audio:  str = Field(..., description="Base64-encoded audio data")
    language_code: str = Field("hi-IN", description="BCP-47 language code, e.g. 'hi-IN', 'mr-IN', 'en-IN'")
    audio_format:  str = Field("wav",   description="Audio format: 'wav', 'mp3', 'ogg'")

    class Config:
        json_schema_extra = {
            "example": {
                "base64_audio":  "<base64-encoded audio string>",
                "language_code": "hi-IN",
                "audio_format":  "wav",
            }
        }


class STTResponse(BaseModel):
    """Response model for POST /speech/stt."""
    transcript:  str   = Field(..., description="Transcribed text")
    confidence:  float = Field(..., description="Confidence score between 0.0 and 1.0")
    language:    str   = Field(..., description="Language code used for recognition")
    source:      str   = Field(..., description="Provider used: 'google', 'bhashini', or 'mock'")


class TTSRequest(BaseModel):
    """Request body for POST /speech/tts (Text-to-Speech)."""
    text:          str = Field(..., description="Text to convert to speech")
    language_code: str = Field("hi-IN",  description="BCP-47 language code, e.g. 'hi-IN'")
    voice_gender:  str = Field("female", description="Voice gender: 'male' or 'female'")

    class Config:
        json_schema_extra = {
            "example": {
                "text":          "आपकी फसल के लिए सिंचाई का सही समय सुबह है।",
                "language_code": "hi-IN",
                "voice_gender":  "female",
            }
        }


class TTSResponse(BaseModel):
    """Response model for POST /speech/tts."""
    audio_base64: str = Field(..., description="Base64-encoded audio output")
    format:       str = Field(..., description="Audio format: 'mp3' or 'wav'")
    language:     str = Field(..., description="Language code used")
    source:       str = Field(..., description="Provider used: 'google', 'bhashini', or 'mock'")


# ==============================================================================
# VIRTUAL POOLING SCHEMAS
# ==============================================================================

class Farmer(BaseModel):
    """A farmer entry submitted for virtual pooling."""
    farmer_id: int   = Field(..., description="Unique identifier for the farmer")
    quantity:  float = Field(..., gt=0, description="Crop produce quantity in quintals")
    location:  str   = Field(..., min_length=1, description="Village / City / District name")
    crop:      str   = Field(..., min_length=1, description="Crop name, e.g. 'wheat', 'mustard'")

    class Config:
        json_schema_extra = {
            "example": {
                "farmer_id": 1,
                "quantity": 50.0,
                "location": "Jhajjar",
                "crop": "wheat",
            }
        }


class PoolRequest(BaseModel):
    """Request payload for POST /pool/."""
    farmers:       List[Farmer]              = Field(..., min_items=1, description="List of farmers to cluster and pool")
    price_history: Optional[List[float]]     = Field(None, description="Optional historical daily prices (₹/q) for LSTM forecasting")

    class Config:
        json_schema_extra = {
            "example": {
                "farmers": [
                    {"farmer_id": 1, "quantity": 50.0, "location": "Jhajjar", "crop": "wheat"},
                    {"farmer_id": 2, "quantity": 80.0, "location": "Bahadurgarh", "crop": "wheat"},
                ],
                "price_history": [2150.0, 2180.0, 2200.0],
            }
        }


class Centroid(BaseModel):
    """Geographic centroid coordinate."""
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")


class PoolRecommendation(BaseModel):
    """Best optimized mandi recommendation for a pool."""
    mandi:            str   = Field(..., description="Recommended Mandi name")
    price:            float = Field(..., description="Base predicted price ₹/quintal")
    predicted_price:  float = Field(..., description="Base predicted price ₹/quintal")
    grade:            str   = Field(..., description="Predicted quality grade (e.g. FAQ, Best)")
    grade_multiplier: float = Field(..., description="Quality price multiplier")
    grade_confidence: float = Field(..., description="Confidence score for grade prediction")
    effective_price:  float = Field(..., description="Price after quality adjustment ₹/quintal")
    distance_km:      float = Field(..., description="Haversine distance from pool centroid to mandi in km")
    trucks_needed:    int   = Field(..., description="Calculated number of 200q capacity trucks")
    transport_cost:   float = Field(..., description="Logistics cost per quintal ₹/quintal")
    net_price:        float = Field(..., description="Net payout to farmers per quintal ₹/quintal")


class PoolResult(BaseModel):
    """Result breakdown for an individual virtual pool."""
    pool_id:        str                         = Field(..., description="Unique pool ID")
    crop:           str                         = Field(..., description="Crop pooled")
    total_quantity: Optional[float]             = Field(None, description="Combined quantity across pooled farmers")
    num_farmers:    Optional[int]               = Field(None, description="Number of farmers in this cluster pool")
    centroid:       Optional[Centroid]          = Field(None, description="Geographic centroid coordinates")
    recommendation: Optional[PoolRecommendation]= Field(None, description="Recommended mandi details")
    total_earnings: Optional[float]             = Field(None, description="Estimated total earnings for the pool in ₹")
    error:          Optional[str]               = Field(None, description="Error message if optimization failed for pool")


class PoolResponse(BaseModel):
    """Response payload for POST /pool/."""
    status:      str              = Field("success", description="Response status")
    total_pools: int              = Field(..., description="Total number of pools formed")
    pools:       List[PoolResult] = Field(..., description="List of pooled and optimized clusters")

