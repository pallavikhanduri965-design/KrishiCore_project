"""
FasalNirnay — Main Application Entry Point
==========================================
This file creates the FastAPI app, adds middleware,
and registers all route modules. Keep this file minimal.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import weather, news, chat, speech, pooling

# ------------------------------------------------------------------------------
# Create the FastAPI application instance
# ------------------------------------------------------------------------------
app = FastAPI(
    title=getattr(settings, "API_TITLE", "FasalNirnay API"),
    description=getattr(settings, "API_DESCRIPTION", "Backend API for FasalNirnay — AI-powered agricultural advisory & virtual pooling platform."),
    version=getattr(settings, "API_VERSION", "1.0.0"),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ------------------------------------------------------------------------------
# CORS Middleware
# ------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Register Routers
# Each feature module has its own router with a URL prefix.
# ------------------------------------------------------------------------------
app.include_router(weather.router, prefix="/weather", tags=["Weather"])
app.include_router(news.router,    prefix="/news",    tags=["News"])
app.include_router(chat.router,    prefix="/chat",    tags=["Chat"])
app.include_router(speech.router,  prefix="/speech",  tags=["Speech"])
app.include_router(pooling.router)


# ------------------------------------------------------------------------------
# Root Endpoint — quick sanity check
# ------------------------------------------------------------------------------
@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint. Confirms the API is running."""
    return {
        "message": "Welcome to FasalNirnay API 🌾",
        "status": "running",
        "version": getattr(settings, "API_VERSION", "1.0.0"),
        "docs": "/docs",
    }


# ------------------------------------------------------------------------------
# Health Endpoint — used by deployment platforms to check if the service is up
# ------------------------------------------------------------------------------
@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": getattr(settings, "APP_ENV", "development"),
        "version": getattr(settings, "API_VERSION", "1.0.0"),
    }

