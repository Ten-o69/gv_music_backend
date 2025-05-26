from pathlib import Path
import io
from typing import Any

from mutagen.id3 import ID3, APIC, TIT2, TPE1
from mutagen.mp3 import MP3, HeaderNotFoundError
from PIL import Image


class MusicTrackMetadata:
    def __init__(
            self,
            path_to_music_track: Path,
            music_track_title: str | None = None,
            music_track_artist: str | None = None,
            music_track_cover_binary: bytes | None = None,
    ):
        try:
            self.audio_obj: MP3 | None = MP3(str(path_to_music_track), ID3=ID3)
            self.audio_duration = int(self.audio_obj.info.length)

        except HeaderNotFoundError:
            self.audio_obj = None
            self.audio_duration = 0

        if music_track_title:
            self.title = music_track_title

        else:
            self.title = self.get_title_from_metadata()

        if music_track_artist:
            self.artist = music_track_artist

        else:
            self.artist = self.get_artist_from_metadata()

        if music_track_cover_binary:
            self.cover_bytes = music_track_cover_binary

        else:
            self.cover_bytes = self.get_mp3_cover_bytes()

    def __new__(cls, *args, **kwargs) -> dict[str, Any]:
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)

        music_track_metadata: dict[str, Any] = {
            "audio_duration": instance.audio_duration,
            "title": instance.title,
            "artist": instance.artist,
            "cover_bytes": instance.cover_bytes,
        }

        return music_track_metadata

    def get_title_from_metadata(self) -> str | None:
        if self.audio_obj and self.audio_obj.tags:
            audio_title = self.audio_obj.tags.get("TIT2", None)
            audio_title = audio_title.text[0] if isinstance(audio_title, TIT2) else audio_title

        else:
            audio_title = None

        return audio_title

    def get_artist_from_metadata(self) -> str | None:
        if self.audio_obj and self.audio_obj.tags:
            audio_artist = self.audio_obj.tags.get("TPE1", None)
            audio_artist = audio_artist.text[0] if isinstance(audio_artist, TPE1) else audio_artist

        else:
            audio_artist = None

        return audio_artist

    def get_mp3_cover_bytes(
            self,
            output_quality: int = 50,
    ) -> bytes | None:
        """
        Extract and compress the embedded album cover from an MP3 file.

        This function attempts to extract the album artwork from the given MP3 file using Mutagen,
        compress it using Pillow, and return the resulting JPEG image as bytes.

        Args:
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
        if not self.audio_obj.tags:
            return None

        for tag in self.audio_obj.tags.values():
            if isinstance(tag, APIC):
                image_data = tag.data  # Extract raw image bytes

                # Open and compress image using Pillow
                image = Image.open(io.BytesIO(image_data))
                output_io = io.BytesIO()
                image.convert("RGB").save(output_io, format="JPEG", quality=output_quality)

                return output_io.getvalue()

        return None  # No cover found
