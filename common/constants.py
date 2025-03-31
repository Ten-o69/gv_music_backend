from pathlib import Path
import os

from dotenv import load_dotenv
from ten_utils.log import Logger


# base
env_mode = os.getenv("ENV", "dev")
logger = Logger(__name__, level=3)
load_dotenv(f".env.{env_mode}")


# path/dir
BASE_DIR = Path(__file__).parent.parent
DIR_DATA = os.getenv("DIR_DATA", None)
if DIR_DATA:
    DIR_DATA = Path(DIR_DATA)

else:
    logger.critical("DIR_DATA environment variable is not set")

DIR_MUSIC = DIR_DATA / "music"
DIR_MUSIC_COVER = DIR_DATA / "music_cover"
DIR_STATIC = BASE_DIR / "static"

# url
URL_MUSIC = "static/music/"
URL_MUSIC_STREAM = "api/v1/tracks/"
URL_MUSIC_COVER = "static/music_cover/"

# database
DATABASE_URL = os.getenv("DATABASE_URL", None)

# api
ALLOW_HOSTS = os.getenv("ALLOW_HOSTS", None)
if ALLOW_HOSTS:
    ALLOW_HOSTS = ALLOW_HOSTS.split(",")

elif not ALLOW_HOSTS:
    logger.critical("ALLOW_HOSTS environment variable is not set")
