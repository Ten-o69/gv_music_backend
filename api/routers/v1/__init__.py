from fastapi import APIRouter


from . import (
    govno_music,
)

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(govno_music.router)
