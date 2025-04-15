import uuid

from sqlalchemy import Column, Integer, String, Text

from .config import Base


class User(Base):
    """
    SQLAlchemy ORM model for the `users` table.

    Represents an application user, storing authentication information.

    Fields:
        id (str): UUID of the user (primary key).
        username (str): Unique username for authentication.
        password_hash (str): Hashed password for secure storage.
    """

    __tablename__ = 'users'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="UUID (v4) used as the primary key."
    )
    username = Column(
        String(20),
        nullable=False,
        unique=True,
        doc="Unique username of the user, max length 20 characters."
    )
    password_hash = Column(
        String(64),
        nullable=False,
        doc="SHA-256 hashed password, stored securely (64 characters)."
    )


class Track(Base):
    """
    SQLAlchemy ORM model for the `tracks` table.

    Represents a music track with its metadata, including file path and duration.

    Fields:
        id (str): UUID of the track (primary key).
        title (str, optional): Title of the music track.
        artist (str, optional): Artist or band name.
        path (str): Relative path to the audio file on the server.
        cover_path (str, optional): Path to the cover image file (if available).
        duration (int): Duration of the track in seconds.
    """

    __tablename__ = 'tracks'

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="UUID (v4) used as the primary key for the track."
    )
    title = Column(
        String(60),
        nullable=True,
        doc="Title of the track. Optional. Max length 60 characters."
    )
    artist = Column(
        String(60),
        nullable=True,
        doc="Name of the artist or band. Optional. Max length 60 characters."
    )
    path = Column(
        String(255),
        nullable=False,
        doc="Relative file path to the audio file on the server."
    )
    cover_path = Column(
        Text,
        nullable=True,
        doc="Optional relative path to the cover image file (usually .jpg)."
    )
    duration = Column(
        Integer,
        nullable=False,
        doc="Track duration in seconds."
    )
