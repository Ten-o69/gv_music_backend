import os

from fastapi import APIRouter, UploadFile, File
from fastapi.requests import Request
from fastapi.responses import (
    JSONResponse,
    StreamingResponse,
    Response
)

from service.music import (
    get_music_list,
    save_music,
)
from ..utils import iter_file


router = APIRouter(prefix="/govno_music", tags=["govno_music"])


@router.get("/list/")
def govno_music_list():
    music_list = get_music_list()

    if len(music_list) == 0 or music_list is None:
        return {
            "num": 0,
            "tracks": None
        }

    data = {
        "num": len(music_list),
        "tracks": music_list,
    }

    return JSONResponse(data)


@router.get("/stream/{index}/")
def govno_music_get_stream(request: Request, index: str):
    music_list = get_music_list()
    range_header = request.headers.get("range")

    if len(music_list) == 0 or music_list is None:
        return Response(status_code=404, content="No music found on the server")

    for music in music_list:
        if music["id"] == index:
            file_size = os.path.getsize(music["path"])

            if range_header:
                # Если запрос с Range-заголовком, обрабатываем его
                range_value = range_header.replace("bytes=", "").split("-")
                start = int(range_value[0]) if range_value[0] else 0
                end = int(range_value[1]) if len(range_value) > 1 and range_value[1] else file_size - 1

                response = StreamingResponse(iter_file(music["path"], start, end + 1),
                                             status_code=206, media_type="audio/mpeg")
                response.headers.update({
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(end - start + 1)
                })

                return response

            return StreamingResponse(iter_file(music["path"], 0, file_size), media_type="audio/mpeg")

    return Response(status_code=404, content="No music found by index")


@router.post("/upload/")
def govno_music_upload(music_file: UploadFile = File(...)):
    music_file_binary = music_file.file.read()

    save_music(music_file_binary)

    return Response(status_code=200, content="OK")
