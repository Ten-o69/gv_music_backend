from pathlib import Path
from typing import Generator, Any

def iter_file(
        file: bytes | Path | str,
        start: int,
        end: int,
        chunk_size: int = 1024
) -> Generator[bytes, Any, None]:
    """
    Функция читает файл частями для стриминга
    :param file: Путь до файла или байты файла
    :param start: Откуда начать читать файл по байтам
    :param end: Где закончить читать файл
    :param chunk_size: Размер чанка который
        мы будем считывать за раз.
    :return: Возвращает генератор или None
    """
    with open(file, "rb") as f:
        f.seek(start)

        while start < end:
            chunk = f.read(min(chunk_size, end - start))
            if not chunk:
                break

            start += len(chunk)
            yield chunk

