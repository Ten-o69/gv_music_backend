from uuid import uuid4

from ten_utils.log import Logger
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1

from common.constants import (
    DIR_MUSIC,
)
from .utils import get_mp3_cover_base64
from database import models
from database.config import SessionLocal


logger = Logger(__name__, level=1)


def get_music_list() -> list[dict[str, str | int]] | None:
    with SessionLocal() as session:
        music_list = session.query(models.Music).all()

    music_list_json = []
    music: models.Music

    for music in music_list:
        minutes, seconds = divmod(music.seconds, 60)

        music_list_json.append({
            "id": music.id,
            "name": music.name,
            "author": music.author,
            "path": music.path,
            "cover_base64": f"data:image/jpeg;base64,{music.cover_base64}",
            "time": f"{minutes}:{seconds:02d}",
        })

    return music_list_json


def save_music(file_binary: bytes) -> None:
    path_to_music = DIR_MUSIC / (str(uuid4()) + ".mp3")
    with path_to_music.open("wb") as file:
        file.write(file_binary)

    audio = MP3(str(path_to_music), ID3=ID3)
    audio_duration = int(audio.info.length)
    audio_cover_base64 = get_mp3_cover_base64(str(path_to_music))

    if audio.tags:
        audio_title = audio.tags.get("TIT2", "Unknown Title")
        audio_artist = audio.tags.get("TPE1", "Unknown Artist")

    else:
        audio_title = None
        audio_artist = None


    with SessionLocal() as session:
        music = models.Music(
            name=audio_title.text[0] if isinstance(audio_title, TIT2) else audio_title,
            author=audio_artist.text[0] if isinstance(audio_artist, TPE1) else audio_artist,
            path=str(path_to_music),
            cover_base64=audio_cover_base64,
            seconds=audio_duration,
        )

        session.add(music)
        session.commit()
