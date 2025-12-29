"""Audio extraction service for processing video/audio files."""

import tempfile
from pathlib import Path
from typing import Optional, Tuple

from app.services.storage_service import StorageService, get_storage_service
from app.utils.ffmpeg_utils import (
    FFmpegError,
    extract_audio,
    generate_waveform_data,
    get_media_duration,
    get_media_info,
    validate_media_file,
)


class AudioExtractor:
    """Service for extracting and processing audio from media files."""

    def __init__(self, storage_service: Optional[StorageService] = None):
        self.storage = storage_service or get_storage_service()

    def extract_audio_from_file(
        self,
        file_path: Path,
        output_dir: Optional[Path] = None,
        sample_rate: int = 16000,
        channels: int = 1,
    ) -> Path:
        """
        Extract audio from a video/audio file.

        Args:
            file_path: Path to the input media file
            output_dir: Directory for output file (uses temp if not provided)
            sample_rate: Output sample rate (default 16kHz for VAD)
            channels: Number of audio channels (default mono)

        Returns:
            Path to the extracted audio WAV file
        """
        if output_dir:
            output_path = output_dir / f"{file_path.stem}_audio.wav"
        else:
            output_path = None

        return extract_audio(
            input_path=file_path,
            output_path=output_path,
            sample_rate=sample_rate,
            channels=channels,
        )

    def get_duration(self, file_path: Path) -> Optional[float]:
        """Get media duration in seconds."""
        return get_media_duration(file_path)

    def get_info(self, file_path: Path) -> Optional[dict]:
        """Get detailed media information."""
        return get_media_info(file_path)

    def validate_file(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """Validate that a file is a valid media file with audio."""
        return validate_media_file(file_path)

    def generate_waveform(
        self,
        file_path: Path,
        num_samples: int = 1000,
    ) -> Tuple[list, float, int]:
        """
        Generate waveform visualization data.

        Args:
            file_path: Path to audio file
            num_samples: Number of peak samples to generate

        Returns:
            Tuple of (peaks list, duration, sample_rate)
        """
        return generate_waveform_data(file_path, num_samples)

    def process_uploaded_file(
        self,
        stored_path: str,
        temp_dir: Optional[Path] = None,
    ) -> Tuple[Path, float]:
        """
        Process an uploaded file for analysis.

        Args:
            stored_path: Path to the stored file
            temp_dir: Temporary directory for processing

        Returns:
            Tuple of (audio_path, duration)
        """
        file_path = Path(stored_path)

        # Validate file
        is_valid, error = self.validate_file(file_path)
        if not is_valid:
            raise FFmpegError(error or "Invalid media file")

        # Get duration
        duration = self.get_duration(file_path)
        if duration is None:
            raise FFmpegError("Could not determine media duration")

        # Extract audio
        if temp_dir is None:
            temp_dir = Path(tempfile.mkdtemp())

        audio_path = self.extract_audio_from_file(
            file_path=file_path,
            output_dir=temp_dir,
        )

        return audio_path, duration


def get_audio_extractor() -> AudioExtractor:
    """Get audio extractor instance."""
    return AudioExtractor()
