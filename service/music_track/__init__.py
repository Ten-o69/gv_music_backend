from uuid import uuid4
from pathlib import Path
import mimetypes

from ten_utils.log import Logger

from common.constants import (
    DIR_MUSIC,
    DIR_MUSIC_COVER,
    URL_MUSIC_STREAM,
    URL_MUSIC_COVER,
)
from common.helpers import get_relative_path
from database.models import Track
from database.config import SessionLocal
from .metadata import MusicTrackMetadata


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
        if music_track.cover_path:
            music_track_cover_path = Path(music_track.cover_path)
            music_track_cover_url = f"{base_url + URL_MUSIC_COVER + music_track_cover_path.name}"

        else:
            music_track_cover_url = None

        mime_type, _ = mimetypes.guess_type(music_track.path)

        music_track_list_json.append({
            "id": music_track.id,
            "title": music_track.title,
            "artist": music_track.artist,
            "url": f"{base_url}{URL_MUSIC_STREAM}{music_track.id}",
            "cover_url": music_track_cover_url,
            "duration": music_track.duration,
            "mime_type": mime_type,
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


def save_music_track(
        db: SessionLocal,
        music_track_binary: bytes,
        music_track_title: str | None = None,
        music_track_artist: str | None = None,
        music_track_cover_binary: bytes | None = None,
):
    path_to_track_music = DIR_MUSIC / (str(uuid4()) + ".mp3")
    path_to_track_music_cover = DIR_MUSIC_COVER / (str(uuid4()) + ".jpg")

    with open(path_to_track_music, "wb") as file:
        file.write(music_track_binary)

    music_track_metadata = MusicTrackMetadata(
        path_to_music_track=path_to_track_music,
        music_track_title=music_track_title,
        music_track_artist=music_track_artist,
        music_track_cover_binary=music_track_cover_binary,
    )

    if music_track_metadata["cover_bytes"]:
        with open(path_to_track_music_cover, "wb") as file:
            file.write(music_track_metadata["cover_bytes"])

    else:
        path_to_track_music_cover = None

    # Convert to relative paths for database storage
    path_to_track_music = get_relative_path(path_to_track_music)

    if path_to_track_music_cover is not None:
        path_to_track_music_cover = get_relative_path(path_to_track_music_cover)

    # Create Track object
    music = Track(
        title=music_track_metadata["title"],
        artist=music_track_metadata["artist"],
        path=path_to_track_music,
        cover_path=path_to_track_music_cover,
        duration=music_track_metadata["audio_duration"],
    )

    db.add(music)
    db.commit()
