from pathlib import Path

from .constants import (
    DIR_DATA,
)


def get_relative_path(path: Path) -> str:
    """
    Converts an absolute path to a relative path based on the base data directory (DIR_DATA).

    This function ensures that the returned path is in a consistent, POSIX-compliant format
    (i.e., using forward slashes `/`), making it suitable for storage or transport across systems.

    Args:
        path (Path): The absolute path to convert.

    Returns:
        str: A relative POSIX-style path string, relative to DIR_DATA.

    Raises:
        ValueError: If the provided path is not a sub-path of DIR_DATA.
    """
    return path.relative_to(DIR_DATA).as_posix()
