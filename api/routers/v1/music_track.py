"""
Tracks API router for handling music track operations.

This module provides endpoints to:
- Retrieve a paginated list of music tracks.
- Stream an individual music track.
- Upload a new music file to the server.

Routes:
    - GET /tracks/
    - GET /tracks/{track_id}/
    - POST /tracks/
"""

import os
from typing import Optional

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query,
    Request,
    Form,
)
from fastapi.responses import (
    JSONResponse,
    StreamingResponse,
    Response
)
from sqlalchemy.orm import Session

from service.music_track  import (
    get_music_track_list,
    save_music_track,
    get_music_track,
)
from ..utils import iter_file
from database import get_db
from schemas.music_track import MusicTrackListResponse
from common.constants import DIR_DATA

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("", response_model=MusicTrackListResponse)
def get_music_tracks_list(
    request: Request,
    skip: int = Query(0, alias="offset"),
    limit: int = Query(100, alias="limit"),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Retrieve a paginated list of music tracks.

    Args:
        request (Request): FastAPI request object to extract base URL.
        skip (int): Number of items to skip for pagination (alias: offset).
        limit (int): Maximum number of items to return (alias: limit).
        db (Session): SQLAlchemy database session dependency.

    Returns:
        JSONResponse: List of music tracks along with pagination metadata.
    """
    track_list, total_tracks = get_music_track_list(
        db=db,
        base_url=str(request.base_url),
        offset=skip,
        limit=limit
    )

    if total_tracks == 0 or not track_list:
        return JSONResponse({
            "total": total_tracks,
            "offset": skip,
            "limit": limit,
            "tracks": None,
            "next_offset": skip + limit if skip + limit < total_tracks else None,
        })

    return JSONResponse({
        "total": total_tracks,
        "offset": skip,
        "limit": limit,
        "tracks": track_list,
        "next_offset": skip + limit if skip + limit < total_tracks else None,
    })


@router.get("/{track_id}/")
def music_track_get_stream(
    request: Request,
    track_id: str,
    db: Session = Depends(get_db),
) -> Response:
    """
    Stream a specific track by its ID, with support for HTTP Range requests.

    Args:
        request (Request): FastAPI request object (used to extract headers and base URL).
        track_id (str): ID of the track to stream.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        StreamingResponse or Response: Audio stream of the track, or 404 if not found.
    """
    track = get_music_track(
        track_id=track_id,
        db=db,
    )
    range_header = request.headers.get("range")

    if track is None:
        return Response(status_code=404, content="Not found music track")

    path_to_track = DIR_DATA / track.path
    file_size = os.path.getsize(path_to_track)

    if range_header:
        # Handle partial content (HTTP 206)
        range_value = range_header.replace("bytes=", "").split("-")
        start = int(range_value[0]) if range_value[0] else 0
        end = int(range_value[1]) if len(range_value) > 1 and range_value[1] else file_size - 1

        response = StreamingResponse(
            iter_file(path_to_track, start, end + 1),
            status_code=206,
            media_type="audio/mpeg"
        )
        response.headers.update({
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(end - start + 1)
        })
        return response

    # Return full file if no range requested
    return StreamingResponse(
        iter_file(path_to_track, 0, file_size),
        media_type="audio/mpeg"
    )


@router.post("/")
def music_track_upload(
        db: Session = Depends(get_db),
        music_track_file: UploadFile = File(...),
        music_track_cover_file: Optional[UploadFile] = File(None),
        music_track_title: Optional[str] = Form(None),
        music_track_artist: Optional[str] = Form(None),
) -> Response:
    """
    Upload a new music file to the server.

    Args:
        music_track_file (UploadFile): The music file to upload.
        music_track_title (Optional[str]): The name of the new music track.
        music_track_artist (Optional[str]): The author of the new music track.
        music_track_cover_file (Optional[UploadFile]): The cover of the new music track.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        Response: HTTP 200 OK on success.
    """
    save_music_track(
        db=db,
        music_track_binary=music_track_file.file.read(),
        music_track_cover_binary=music_track_cover_file.file.read() if music_track_cover_file else None,
        music_track_title=music_track_title,
        music_track_artist=music_track_artist,
    )

    return Response(status_code=200, content="OK")
