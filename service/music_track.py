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


logger = Logger(__name__)


def get_music_track_list(
        db: SessionLocal,
        base_url: str,
        offset: int = 0,
        limit: int = 100,
        get_all: bool = False,
) -> tuple[list[dict[str, str | int]], int]:
    """
    Retrieves a paginated list of music tracks from the database and returns it as a list of dictionaries.

    Args:
        db (SessionLocal): The active SQLAlchemy database session.
        base_url (str): The base URL used to generate absolute URLs for audio and cover files.
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Maximum number of items to return. Defaults to 100.
        get_all (bool, optional): If True, ignores pagination and returns all tracks.

    Returns:
        tuple[list[dict[str, str | int]], int]:
            - A list of dictionaries representing music tracks.
            - The total number of tracks in the database.
    """
    if not get_all:
        music_track_list = db.query(Track).offset(offset).limit(limit).all()

    else:
        music_track_list = db.query(Track).all()

    total_music_tracks = db.query(Track).count()
    music_track_list_json = []

    for music_track in music_track_list:
        music_track_cover_path = Path(music_track.cover_path if music_track.cover_path else "")
        music_track_cover_url = (f"{base_url}{URL_MUSIC_COVER}"
                                 f"{music_track_cover_path.stem + music_track_cover_path.suffix}")

        music_track_list_json.append({
            "id": music_track.id,
            "title": music_track.title,
            "artist": music_track.artist,
            "url": f"{base_url}{URL_MUSIC_STREAM}{music_track.id}",
            "cover_url": music_track_cover_url,
            "duration": music_track.duration,
        })

    return music_track_list_json, total_music_tracks


def get_music_track(track_id: str, db: SessionLocal) -> Track | None:
    """
    Retrieves a single music track by its ID.

    Args:
        track_id (str): The UUID of the track.
        db (SessionLocal): The active SQLAlchemy database session.

    Returns:
        Track | None: The Track object if found, otherwise None.
    """
    music_track = db.query(Track).filter(Track.id == track_id).first()

    return music_track


def save_music_track(db: SessionLocal, file_binary: bytes) -> None:
    """
    Saves an uploaded music file into the file system and creates a corresponding Track entry in the database.

    This function:
        - Writes the MP3 file to disk.
        - Extracts metadata such as title, artist, and duration.
        - Saves cover art if available.
        - Stores the track and cover in the database.

    Args:
        db (SessionLocal): The active SQLAlchemy database session.
        file_binary (bytes): Binary content of the uploaded MP3 file.

    Raises:
        HeaderNotFoundError: If the uploaded file is not a valid MP3 file with proper headers.
    """
    path_to_track_music = DIR_MUSIC / (str(uuid4()) + ".mp3")
    path_to_track_music_cover = DIR_MUSIC_COVER / (str(uuid4()) + ".jpg")

    with open(path_to_track_music, "wb") as file:
        file.write(file_binary)

    try:
        audio = MP3(str(path_to_track_music), ID3=ID3)
        audio_duration = int(audio.info.length)
        audio_cover_base64 = get_mp3_cover_bytes(audio_obj=audio)

    except HeaderNotFoundError:
        audio = None
        audio_duration = 0
        audio_cover_base64 = None

    # Save cover art to file system
    if audio_cover_base64:
        with open(path_to_track_music_cover, "wb") as file:
                file.write(audio_cover_base64)

    else:
        path_to_track_music_cover = None

    # Extract metadata
    if audio and audio.tags:
        audio_title = audio.tags.get("TIT2", None)
        audio_artist = audio.tags.get("TPE1", None)

    else:
        audio_title = None
        audio_artist = None

    # Convert to relative paths for database storage
    path_to_track_music = get_relative_path(path_to_track_music)

    if path_to_track_music_cover is not None:
        path_to_track_music_cover = get_relative_path(path_to_track_music_cover)

    # Create Track object
    music = Track(
        title=audio_title.text[0] if isinstance(audio_title, TIT2) else audio_title,
        artist=audio_artist.text[0] if isinstance(audio_artist, TPE1) else audio_artist,
        path=path_to_track_music,
        cover_path=path_to_track_music_cover,
        duration=audio_duration,
    )

    db.add(music)
    db.commit()
