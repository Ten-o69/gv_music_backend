from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ten_utils.log import Logger

from .routers import api_router
from common.constants import (
    DIR_STATIC,
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    API_CORS_ALLOW_METHODS,
    API_CORS_ALLOW_ORIGINS,
    API_CORS_ALLOW_CREDENTIALS,
    API_ALLOW_HOSTS,
)

logger = Logger(__name__)

# Create FastAPI application instance
app = FastAPI(
    description="API for self-hosted player gv_music",
    version="0.0.5",
)

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CORS_ALLOW_ORIGINS,
    allow_credentials=API_CORS_ALLOW_CREDENTIALS,
    allow_methods=API_CORS_ALLOW_METHODS,
)

# Mount static directories to serve media files
app.mount(
    "/static",
    StaticFiles(directory=DIR_STATIC),
    name="static",
)
app.mount(
    "/music_tracks",
    StaticFiles(directory=DIR_MUSIC),
    name="static_music_tracks",
)
app.mount(
    "/music_track_covers",
    StaticFiles(directory=DIR_MUSIC_COVER),
    name="static_music_track_covers",
)


@app.get("/")
def root():
    """
    Health check endpoint.

    Returns a simple JSON message to indicate the API is running.
    """
    return {
        "detail": "API work!",
    }


app.include_router(api_router)
