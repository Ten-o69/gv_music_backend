from pathlib import Path

from .constants import (
    BASE_DIR,
)


def get_relative_path(path: Path) -> str:
    return path.relative_to(BASE_DIR).as_posix()
