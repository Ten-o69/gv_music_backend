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


@app.middleware("http")
async def restrict_access_to_hosts(request: Request, call_next):
    """
    Middleware to restrict access based on allowed client IPs.

    Checks whether the client's resolved IP is in the list of allowed hosts.
    If not, returns a 403 Forbidden response.
    """
    client_host = request.state.ip

    if client_host not in API_ALLOW_HOSTS:
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Access denied for host: {client_host}",
            }
        )

    return await call_next(request)


@app.middleware("http")
async def log_ip(request: Request, call_next):
    """
    Middleware to log client IP address.

    Logs the IP from the "X-Forwarded-For" header and the resolved request IP.
    Useful for debugging and tracking clients behind proxies.
    """
    logger.debug(f"Client IP from header: {request.headers.get('x-forwarded-for')}")
    logger.debug(f"Client IP resolved: {request.client.host}")

    return await call_next(request)


@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    """
    Middleware to extract real client IP address.

    Uses the "X-Forwarded-For" header if available to assign a
    trusted `request.state.ip` value for use in other middleware.
    """
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        real_ip = forwarded_for.split(",")[0].strip()
        request.state.ip = real_ip
    else:
        request.state.ip = request.client.host

    return await call_next(request)


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
