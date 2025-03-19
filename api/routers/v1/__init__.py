from fastapi import APIRouter


from . import (
    govno_music,
)

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(govno_music.router)
