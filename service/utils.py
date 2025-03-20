import base64
import io

from mutagen.mp3 import MP3
from mutagen.id3 import APIC, ID3
from PIL import Image


def get_mp3_cover_bytes(file_path: str, output_quality: int = 50) -> bytes | None:
    """Возвращает сжатую обложку в формате base64"""

    audio = MP3(file_path, ID3=ID3)

    if not audio.tags:
        return None

    for tag in audio.tags.values():
        if isinstance(tag, APIC):
            image_data = tag.data  # Получаем оригинальный байтовый формат изображения

            # Открываем изображение через Pillow
            image = Image.open(io.BytesIO(image_data))

            # Сжимаем изображение и конвертируем в JPEG
            output_io = io.BytesIO()
            image.convert("RGB").save(output_io, format="JPEG", quality=output_quality)

            # Кодируем в base64
            return output_io.getvalue()

    return None  # Если обложки нет
