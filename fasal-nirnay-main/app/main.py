"""
FasalNirnay — Main Application Entry Point
==========================================
This file creates the FastAPI app, adds middleware,
and registers all route modules. Keep this file minimal.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

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
# Health Endpoint
# ------------------------------------------------------------------------------
@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": getattr(settings, "APP_ENV", "development"),
        "version": getattr(settings, "API_VERSION", "1.0.0"),
    }


# ------------------------------------------------------------------------------
# Mount Frontend Static Assets & Web App UI
# ------------------------------------------------------------------------------
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

if os.path.exists(frontend_dir):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
    assets_path = os.path.join(frontend_dir, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

    @app.get("/", tags=["Frontend"])
    async def serve_spa():
        """Serves the FasalNirnay AI Frontend Web Application."""
        return FileResponse(os.path.join(frontend_dir, "index.html"))
else:
    @app.get("/", tags=["Root"])
    def read_root():
        """Welcome endpoint fallback."""
        return {
            "message": "Welcome to FasalNirnay API 🌾",
            "status": "running",
            "version": getattr(settings, "API_VERSION", "1.0.0"),
            "docs": "/docs",
        }


