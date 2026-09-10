"""
Configuration
=============
Loads all environment variables from the .env file.
Uses pydantic-settings for type-safe config management.

Usage anywhere in the app:
    from app.core.config import settings
    print(settings.WEATHER_API_KEY)
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    All application settings loaded from environment variables.
    Fields marked Optional[str] = None are safe to omit —
    the service will fall back to mock data automatically.
    """

    # ------------------------------------------------------------------
    # Weather
    # Get a free key at: https://www.weatherapi.com/
    # ------------------------------------------------------------------
    WEATHER_API_KEY: Optional[str] = None

    # ------------------------------------------------------------------
    # News
    # Get a free key at: https://gnews.io/
    # Alternative: https://newsapi.org/ (change service accordingly)
    # ------------------------------------------------------------------
    NEWS_API_KEY: Optional[str] = None

    # ------------------------------------------------------------------
    # LLM / AI Chatbot (Gemini Primary + Ollama Fallback)
    # ------------------------------------------------------------------
    # Google Gemini API key (https://aistudio.google.com/app/apikey)
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Ollama Local LLM Fallback (http://localhost:11434)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    # ------------------------------------------------------------------
    # Speech (STT / TTS)
    # ------------------------------------------------------------------
    # Path to your Google Cloud service account JSON file
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None

    # SPEECH_PROVIDER options: "sarvam", "google", "mock"
    SPEECH_PROVIDER: str = "mock"

    # Sarvam AI API key (https://www.sarvam.ai/)
    # Get your key at: https://dashboard.sarvam.ai/
    SARVAM_API_KEY: Optional[str] = None

    # ------------------------------------------------------------------
    # OpenCage Geocoding API
    # ------------------------------------------------------------------
    OPENCAGE_API_KEY: str = "330bfd9138a143ffb0f2077d6cf8f1d3"

    # ------------------------------------------------------------------
    # ML Models Directory
    # ------------------------------------------------------------------
    MODEL_DIR: Optional[str] = None

    # ------------------------------------------------------------------
    # App settings
    # ------------------------------------------------------------------
    APP_ENV: str = "development"   # "development" | "production"
    APP_PORT: int = 8000
    API_TITLE: str = "FasalNirnay API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Backend API for FasalNirnay — AI-powered agricultural advisory & virtual pooling platform."

    class Config:
        # Automatically reads from a .env file in the project root
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Allows extra fields without throwing errors (useful during development)
        extra = "ignore"


# ------------------------------------------------------------------------------
# Single shared instance — import this everywhere
# ------------------------------------------------------------------------------
settings = Settings()
