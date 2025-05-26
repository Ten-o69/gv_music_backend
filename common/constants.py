from pathlib import Path
import os

from ten_utils.log import LoggerConfig
from ten_utils.env_loader import EnvLoader


# base
BASE_DIR = Path(__file__).parent.parent

# env
ENV_MODE = os.getenv("ENV", "dev")
ENV_PATH = BASE_DIR / f".env.{ENV_MODE}"

if ENV_MODE == "dev":
    env_loader = EnvLoader(ENV_PATH)

elif ENV_MODE == "prod":
    env_loader = EnvLoader(ENV_PATH, getenv_mode=True)

else:
    raise ValueError(f"The environment variable 'ENV_MODE' is not set or is set incorrectly")


# path/dir
DIR_DATA = env_loader.load("DIR_DATA", Path)
DIR_MUSIC = DIR_DATA / "music"
DIR_MUSIC_COVER = DIR_DATA / "music_cover"
DIR_STATIC = BASE_DIR / "static"

# url
URL_MUSIC = "music_tracks/"
URL_MUSIC_COVER = "music_track_covers/"
URL_MUSIC_STREAM = "api/v1/tracks/"

# database
DATABASE_URL = env_loader.load("DATABASE_URL", str)
DATABASE_LOG: bool = env_loader.load("DATABASE_LOG", bool)

# api
API_ALLOW_HOSTS = env_loader.load("API_ALLOW_HOSTS", tuple)
API_CORS_ALLOW_ORIGINS = env_loader.load("API_CORS_ALLOW_ORIGINS", tuple)
API_CORS_ALLOW_METHODS = env_loader.load("API_CORS_ALLOW_METHODS", tuple)
API_CORS_ALLOW_CREDENTIALS = env_loader.load("API_CORS_ALLOW_CREDENTIALS", bool)

# log
LoggerConfig().set_default_level_log(
    env_loader.load("LOG_LEVEL", int)
)
