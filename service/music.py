from uuid import uuid4
from pathlib import Path

from ten_utils.log import Logger
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, TIT2, TPE1

from common.constants import (
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    URL_MUSIC_STREAM,
    URL_MUSIC_COVER,
)
from common.helpers import get_relative_path
from .utils import get_mp3_cover_bytes
from database.models import Track
from database.config import SessionLocal


logger = Logger(__name__, level=1)


def get_music_track_list(
        db: SessionLocal,
        base_url: str,
        offset: int = 0,
        limit: int = 100,
        get_all: bool = False,
) -> tuple[list[dict[str, str | int]], int]:
    if not get_all:
        music_list = db.query(Track).offset(offset).limit(limit).all()

    else:
        music_list = db.query(Track).all()

    total_tracks = db.query(Track).count()
    music_list_json = []
    music: Track

    for music in music_list:
        minutes, seconds = divmod(music.duration, 60)

        cover_path = Path(music.cover_path if music.cover_path else "")
        cover_url = f"{base_url}{URL_MUSIC_COVER}{cover_path.stem + cover_path.suffix}"

        music_list_json.append({
            "id": music.id,
            "title": music.title,
            "artist": music.artist,
            "url": f"{base_url}{URL_MUSIC_STREAM}{music.id}",
            "cover_url": cover_url,
            "duration": f"{minutes}:{seconds:02d}",
        })

    return music_list_json, total_tracks


def get_music_track(track_id: str, db: SessionLocal) -> Track | None:
    track = db.query(Track).filter(Track.id == track_id).first()

    return track


def save_music_track(db: SessionLocal, file_binary: bytes) -> None:
    path_to_music = DIR_MUSIC / (str(uuid4()) + ".mp3")
    path_to_music_cover = DIR_MUSIC_COVER / (str(uuid4()) + ".jpg")

    with open(path_to_music, "wb") as file:
        file.write(file_binary)

    try:
        audio = MP3(str(path_to_music), ID3=ID3)
        audio_duration = int(audio.info.length)
        audio_cover_base64 = get_mp3_cover_bytes(str(path_to_music))

    except HeaderNotFoundError:
        audio = None
        audio_duration = 0
        audio_cover_base64 = None

    # Сохранение обложки в static
    with open(path_to_music_cover, "wb") as file:
        if audio_cover_base64:
            file.write(audio_cover_base64)

    if audio and audio.tags:
        audio_title = audio.tags.get("TIT2", "Unknown Title")
        audio_artist = audio.tags.get("TPE1", "Unknown Artist")

    else:
        audio_title = "Unknown Title"
        audio_artist = "Unknown Artist"

    # Получение относительных путей
    path_to_music = get_relative_path(path_to_music)
    path_to_music_cover = get_relative_path(path_to_music_cover)

    music = Track(
        title=audio_title.text[0] if isinstance(audio_title, TIT2) else audio_title,
        artist=audio_artist.text[0] if isinstance(audio_artist, TPE1) else audio_artist,
        path=path_to_music,
        cover_path=path_to_music_cover,
        duration=audio_duration,
    )

    db.add(music)
    db.commit()
