from pathlib import Path
import os

from dotenv import load_dotenv


env_mode = os.getenv("ENV", "dev")
load_dotenv(f".env.{env_mode}")


# path/dir
BASE_DIR = Path(__file__).parent.parent
DIR_STATIC = BASE_DIR / "static"
DIR_MUSIC = DIR_STATIC / "music"
DIR_MUSIC_COVER = DIR_STATIC / "music_cover"

# url
URL_MUSIC = "static/music/"
URL_MUSIC_STREAM = "api/v1/tracks/"
URL_MUSIC_COVER = "static/music_cover/"


# database
DATABASE_URL = os.getenv("DATABASE_URL")
