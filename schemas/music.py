from typing import Optional, List

from pydantic import BaseModel, UUID4, HttpUrl


class TrackSchema(BaseModel):
    id: UUID4
    title: Optional[str] = None
    artist: Optional[str] = None
    url: HttpUrl
    duration: int

    class Config:
        from_attributes = True


class TrackListResponse(BaseModel):
    total: int
    offset: int
    limit: int
    tracks: Optional[List[TrackSchema]] = None
    next_offset: Optional[int] = None
