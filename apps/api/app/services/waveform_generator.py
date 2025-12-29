"""Waveform generation service for audio visualization."""

from pathlib import Path
from typing import List, Tuple

from app.services.audio_extractor import get_audio_extractor
from app.utils.ffmpeg_utils import generate_waveform_data


class WaveformGenerator:
    """Service for generating waveform visualization data."""

    def __init__(self, num_samples: int = 1000):
        """
        Initialize waveform generator.

        Args:
            num_samples: Number of peak samples to generate
        """
        self.num_samples = num_samples
        self.audio_extractor = get_audio_extractor()

    def generate_from_file(self, file_path: Path) -> Tuple[List[float], float, int]:
        """
        Generate waveform data from a media file.

        Args:
            file_path: Path to media file

        Returns:
            Tuple of (peaks, duration, sample_rate)
        """
        return generate_waveform_data(file_path, self.num_samples)

    def generate_from_audio(self, audio_path: Path) -> Tuple[List[float], float, int]:
        """
        Generate waveform data from an audio file.

        Args:
            audio_path: Path to audio file (WAV preferred)

        Returns:
            Tuple of (peaks, duration, sample_rate)
        """
        return generate_waveform_data(audio_path, self.num_samples)

    def normalize_peaks(self, peaks: List[float]) -> List[float]:
        """
        Normalize peaks to 0-1 range.

        Args:
            peaks: List of peak values

        Returns:
            Normalized peak values
        """
        if not peaks:
            return []

        max_peak = max(peaks)
        if max_peak == 0:
            return peaks

        return [p / max_peak for p in peaks]


def get_waveform_generator(num_samples: int = 1000) -> WaveformGenerator:
    """Get waveform generator instance."""
    return WaveformGenerator(num_samples=num_samples)
