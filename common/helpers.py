from pathlib import Path

from .constants import (
    DIR_DATA,
)


def get_relative_path(path: Path) -> str:
    """
    Функция для получения относительного пути
    в универсальном формате
    :param path: Путь который нужно преобразовать.
    :return: Возвращает строку с преобразованным путём
    """

    return path.relative_to(DIR_DATA).as_posix()
