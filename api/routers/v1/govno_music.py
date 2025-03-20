import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query,
)
from fastapi.requests import Request
from fastapi.responses import (
    JSONResponse,
    StreamingResponse,
    Response
)
from sqlalchemy.orm import Session

from service.music import (
    get_music_list,
    save_music,
)
from ..utils import iter_file
from database import get_db
from schemas.music import TrackListResponse


router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("/", response_model=TrackListResponse)
def govno_music_list(
        request: Request,
        skip: int = Query(0, alias="offset"),
        limit: int = Query(100, alias="limit"),
        db: Session = Depends(get_db),
):
    track_list, total_tracks, _ = get_music_list(
        db=db,
        offset=skip,
        limit=limit,
        base_url=str(request.base_url)
    )

    if total_tracks == 0 or not track_list:
        return {
            "total": total_tracks,
            "offset": skip,
            "limit": limit,
            "tracks": None,
            "next_offset": skip + limit if skip + limit < total_tracks else None,
        }

    data = {
        "total": total_tracks,
        "offset": skip,
        "limit": limit,
        "tracks": track_list,
        "next_offset": skip + limit if skip + limit < total_tracks else None,
    }

    return JSONResponse(data)


@router.get("/{track_id}/")
def govno_music_get_stream(
        request: Request,
        track_id: str,
        db: Session = Depends(get_db),
):
    track_list, total_tracks, path_to_tracks = get_music_list(
        db=db,
        get_all=True,
        base_url=str(request.base_url)
    )
    range_header = request.headers.get("range")

    if total_tracks == 0 or not track_list:
        return Response(status_code=404, content="No music found on the server")

    for num, music in enumerate(track_list):
        if music["id"] == track_id:
            file_size = os.path.getsize(path_to_tracks[num])

            if range_header:
                # Если запрос с Range-заголовком, обрабатывает его
                range_value = range_header.replace("bytes=", "").split("-")
                start = int(range_value[0]) if range_value[0] else 0
                end = int(range_value[1]) if len(range_value) > 1 and range_value[1] else file_size - 1

                response = StreamingResponse(iter_file(path_to_tracks[num], start, end + 1),
                                             status_code=206, media_type="audio/mpeg")
                response.headers.update({
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(end - start + 1)
                })

                return response

            return StreamingResponse(iter_file(path_to_tracks[num], 0, file_size),
                                     media_type="audio/mpeg")

    return Response(status_code=404, content="No music found by index")


@router.post("/")
def govno_music_upload(
        music_file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    music_file_binary = music_file.file.read()

    save_music(db=db, file_binary=music_file_binary)

    return Response(status_code=200, content="OK")
