import uuid

from sqlalchemy import Column, Integer, String, Text

from .config import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)


class Track(Base):
    __tablename__ = 'tracks'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(60), nullable=True)
    artist = Column(String(60), nullable=True)
    path = Column(String(255), nullable=False)
    cover_path = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)
