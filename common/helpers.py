from pathlib import Path

from .constants import (
    BASE_DIR,
)


def get_relative_path(path: Path) -> str:
    """
    Функция для получения относительного пути
    в универсальном формате
    :param path: Путь который нужно преобразовать.
    :return: Возвращает строку с преобразованным путём
    """

    return path.relative_to(BASE_DIR).as_posix()
