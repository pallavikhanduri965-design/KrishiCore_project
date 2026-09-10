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
