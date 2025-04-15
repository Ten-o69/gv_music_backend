from pathlib import Path
from typing import Generator, Any


def iter_file(
    file: bytes | Path | str,
    start: int,
    end: int,
    chunk_size: int = 1024
) -> Generator[bytes, Any, None]:
    """
    Stream a file in chunks within a specified byte range.

    This function is used to efficiently stream part of a file,
    typically for media files where HTTP range requests are supported.

    Args:
        file (bytes | Path | str): The path to the file, or a file-like object.
        start (int): The byte position to start reading from.
        end (int): The byte position to stop reading at (non-inclusive).
        chunk_size (int, optional): The number of bytes to read at a time.
            Defaults to 1024.

    Yields:
        bytes: A chunk of the file within the given byte range.

    Raises:
        OSError: If the file path is invalid or unreadable.

    Example:
        for chunk in iter_file("track.mp3", start=0, end=5000):
            process(chunk)
    """
    with open(file, "rb") as f:
        f.seek(start)

        while start < end:
            chunk = f.read(min(chunk_size, end - start))
            if not chunk:
                break

            start += len(chunk)
            yield chunk
