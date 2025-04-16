from fastapi import APIRouter

from . import (
    music_track,
)

router = APIRouter(prefix="/v1", tags=["v1"])

router.include_router(music_track.router)
