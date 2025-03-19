from fastapi import APIRouter

from . import (
    v1,
)


api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(v1.router, tags=["v1"])
