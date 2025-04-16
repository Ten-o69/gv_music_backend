from typing import Optional, List

from pydantic import BaseModel, UUID4, HttpUrl


class MusicTrackSchema(BaseModel):
    """
    Schema representing a single music track object.

    Attributes:
        id (UUID4): Unique identifier of the track.
        title (Optional[str]): Title of the track. Optional.
        artist (Optional[str]): Name of the artist or performer. Optional.
        url (HttpUrl): URL pointing to the audio file of the track.
        cover_url (Optional[HttpUrl]): URL to the cover image of the track. Optional.
        duration (int): Duration of the track in seconds.
    """

    id: UUID4
    title: Optional[str] = None
    artist: Optional[str] = None
    url: HttpUrl
    cover_url: Optional[HttpUrl] = None
    duration: int

    class Config:
        from_attributes = True  # Allows loading from ORM or objects with attributes.


class MusicTrackListResponse(BaseModel):
    """
    Schema representing a paginated response for a list of music tracks.

    Attributes:
        total (int): Total number of tracks available.
        offset (int): The current offset in pagination.
        limit (int): The maximum number of items returned in one page.
        tracks (Optional[List[MusicTrackSchema]]): List of music tracks in the current page.
        next_offset (Optional[int]): Offset value to fetch the next page of results. Optional.
    """

    total: int
    offset: int
    limit: int
    tracks: Optional[List[MusicTrackSchema]] = None
    next_offset: Optional[int] = None
