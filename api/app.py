from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .routers import api_router
from common.constants import (
    DIR_STATIC,
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    API_CORS_HOSTS,
    API_ALLOW_HOSTS,
)

app = FastAPI(
    description="Плейер для говна",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CORS_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Разрешаем все методы (GET, POST, PUT и т.д.)
)

app.mount("/static", StaticFiles(directory=DIR_STATIC), name="static")
app.mount("/music", StaticFiles(directory=DIR_MUSIC), name="static_music")
app.mount("/music_cover", StaticFiles(directory=DIR_MUSIC_COVER), name="static_music_cover")


@app.middleware("http")
async def restrict_access_to_hosts(request: Request, call_next):
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
    print("Client IP from header:", request.headers.get("x-forwarded-for"))
    print("Client IP resolved:", request.client.host)
    return await call_next(request)


@app.middleware("http")
async def get_real_ip(request: Request, call_next):
    forwarded_for = request.headers.get("x-forwarded-for")

    if forwarded_for:
        real_ip = forwarded_for.split(",")[0].strip()
        request.state.ip = real_ip

    else:
        request.state.ip = request.client.host

    response = await call_next(request)
    return response


@app.get("/")
def root():
    return {
        "detail": "API work!",
    }

app.include_router(api_router)
