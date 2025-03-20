from uuid import uuid4
from pathlib import Path

from ten_utils.log import Logger
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, TIT2, TPE1

from common.constants import (
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    URL_MUSIC,
    URL_MUSIC_COVER,
)
from .utils import get_mp3_cover_bytes
from database.models import Music
from database.config import SessionLocal


logger = Logger(__name__, level=1)


def get_music_list(
        db: SessionLocal,
        base_url: str,
        offset: int = 0,
        limit: int = 100,
        get_all: bool = False,
) -> tuple[list[dict[str, str | int]], int, list[str]]:
    if not get_all:
        music_list = db.query(Music).offset(offset).limit(limit).all()

    else:
        music_list = db.query(Music).all()

    total_tracks = db.query(Music).count()

    music_list_json = []
    path_music_list = []
    music: Music

    for music in music_list:
        minutes, seconds = divmod(music.seconds, 60)
        path_music_list.append(music.path)

        music_list_json.append({
            "id": music.id,
            "title": music.name,
            "artist": music.author,
            "url": f"{base_url}{URL_MUSIC}{Path(music.path).name}",
            "cover_url": f"{base_url}{URL_MUSIC_COVER}{Path(music.cover_path if music.cover_path else "").name}",
            "duration": f"{minutes}:{seconds:02d}",
        })

    return music_list_json, total_tracks, path_music_list


def save_music(db: SessionLocal, file_binary: bytes) -> None:
    path_to_music = DIR_MUSIC / (str(uuid4()) + ".mp3")
    path_to_music_cover = DIR_MUSIC_COVER / (str(uuid4()) + ".jpg")

    with path_to_music.open("wb") as file:
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
        audio_title = None
        audio_artist = None

    music = Music(
        name=audio_title.text[0] if isinstance(audio_title, TIT2) else audio_title,
        author=audio_artist.text[0] if isinstance(audio_artist, TPE1) else audio_artist,
        path=str(path_to_music),
        cover_path=str(path_to_music_cover),
        seconds=audio_duration,
    )

    db.add(music)
    db.commit()
