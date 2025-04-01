from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from .routers import api_router
from common.constants import (
    DIR_STATIC,
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    ALLOW_HOSTS,
)

app = FastAPI(
    description="Плейер для говна",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://212.192.248.169", "http://localhost", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Разрешаем все методы (GET, POST, PUT и т.д.)
)

app.mount("/static", StaticFiles(directory=DIR_STATIC), name="static")
app.mount("/music", StaticFiles(directory=DIR_MUSIC), name="static_music")
app.mount("/music_cover", StaticFiles(directory=DIR_MUSIC_COVER), name="static_music_cover")


@app.middleware("http")
async def restrict_access_to_hosts(request: Request, call_next):
    client_host = request.client.host

    if client_host not in ALLOW_HOSTS:
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Access denied for host: {client_host}",
            }
        )

    return await call_next(request)


@app.get("/")
def root():
    return {
        "detail": "API work!",
    }

app.include_router(api_router)
