from pathlib import Path


def iter_file(file_path: Path | str, start: int, end: int, chunk_size: int = 1024):
    """Читаем файл частями для стриминга"""
    with open(file_path, "rb") as f:
        f.seek(start)
        while start < end:
            chunk = f.read(min(chunk_size, end - start))
            if not chunk:
                break
            start += len(chunk)
            yield chunk

