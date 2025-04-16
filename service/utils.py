import io

from mutagen.mp3 import MP3
from mutagen.id3 import APIC
from PIL import Image


def get_mp3_cover_bytes(
    audio_obj: MP3,
    output_quality: int = 50,
) -> bytes | None:
    """
    Extract and compress the embedded album cover from an MP3 file.

    This function attempts to extract the album artwork from the given MP3 file using Mutagen,
    compress it using Pillow, and return the resulting JPEG image as bytes.

    Args:
        audio_obj (MP3): The Mutagen MP3 object with potential embedded ID3 tags.
        output_quality (int): The quality of the output JPEG image (1–100).
            Lower values mean more compression. Defaults to 50.

    Returns:
        bytes | None: A bytes object containing the JPEG image data if a cover is found,
        otherwise `None`.

    Example:
        ```python
        from mutagen.mp3 import MP3
        from utils import get_mp3_cover_bytes

        mp3 = MP3("song.mp3")
        cover_bytes = get_mp3_cover_bytes(mp3)
        if cover_bytes:
            with open("cover.jpg", "wb") as f:
                f.write(cover_bytes)
        ```
    """
    if not audio_obj.tags:
        return None

    for tag in audio_obj.tags.values():
        if isinstance(tag, APIC):
            image_data = tag.data  # Extract raw image bytes

            # Open and compress image using Pillow
            image = Image.open(io.BytesIO(image_data))
            output_io = io.BytesIO()
            image.convert("RGB").save(output_io, format="JPEG", quality=output_quality)

            return output_io.getvalue()

    return None  # No cover found
