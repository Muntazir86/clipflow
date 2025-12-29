"""Voice Activity Detection (VAD) processor using Silero VAD."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional

import torch

from app.config import get_settings

settings = get_settings()


@dataclass
class Segment:
    """Represents a detected audio segment."""

    start_ms: int
    end_ms: int
    type: Literal["speech", "silence"]
    confidence: float


class VADProcessor:
    """Voice Activity Detection processor using Silero VAD."""

    def __init__(
        self,
        aggressiveness: int = 3,
        min_silence_duration_ms: int = 300,
        min_speech_duration_ms: int = 250,
    ):
        """
        Initialize VAD processor.

        Args:
            aggressiveness: VAD aggressiveness level (1-3, higher = more aggressive)
            min_silence_duration_ms: Minimum silence duration to detect
            min_speech_duration_ms: Minimum speech duration to detect
        """
        self.aggressiveness = max(1, min(3, aggressiveness))
        self.min_silence_duration_ms = min_silence_duration_ms
        self.min_speech_duration_ms = min_speech_duration_ms

        # Silero VAD thresholds based on aggressiveness
        self.thresholds = {
            1: 0.3,  # Less aggressive, more speech detected
            2: 0.5,  # Balanced
            3: 0.7,  # More aggressive, less speech detected
        }

        self._model = None
        self._utils = None

    def _load_model(self):
        """Lazy load Silero VAD model."""
        if self._model is None:
            model, utils = torch.hub.load(
                repo_or_dir="snakers4/silero-vad",
                model="silero_vad",
                force_reload=False,
                onnx=False,
            )
            self._model = model
            self._utils = utils

    def process_audio(
        self,
        audio_path: Path,
        sample_rate: int = 16000,
    ) -> List[Segment]:
        """
        Process audio file and detect speech/silence segments.

        Args:
            audio_path: Path to WAV audio file (16kHz mono recommended)
            sample_rate: Sample rate of the audio file

        Returns:
            List of detected segments
        """
        self._load_model()

        # Get utility functions
        (get_speech_timestamps, _, read_audio, *_) = self._utils

        # Read audio
        wav = read_audio(str(audio_path), sampling_rate=sample_rate)

        # Get speech timestamps
        speech_timestamps = get_speech_timestamps(
            wav,
            self._model,
            sampling_rate=sample_rate,
            threshold=self.thresholds[self.aggressiveness],
            min_silence_duration_ms=self.min_silence_duration_ms,
            min_speech_duration_ms=self.min_speech_duration_ms,
            return_seconds=False,
        )

        # Convert to segments
        segments = self._create_segments(
            speech_timestamps,
            total_samples=len(wav),
            sample_rate=sample_rate,
        )

        return segments

    def _create_segments(
        self,
        speech_timestamps: List[dict],
        total_samples: int,
        sample_rate: int,
    ) -> List[Segment]:
        """
        Create segment list from speech timestamps.

        Args:
            speech_timestamps: List of speech timestamp dicts from Silero
            total_samples: Total number of audio samples
            sample_rate: Audio sample rate

        Returns:
            List of Segment objects including both speech and silence
        """
        segments = []
        current_pos = 0

        for ts in speech_timestamps:
            start_sample = ts["start"]
            end_sample = ts["end"]

            # Add silence segment before speech if there's a gap
            if start_sample > current_pos:
                silence_start_ms = int(current_pos * 1000 / sample_rate)
                silence_end_ms = int(start_sample * 1000 / sample_rate)

                # Only add if meets minimum duration
                if (silence_end_ms - silence_start_ms) >= self.min_silence_duration_ms:
                    segments.append(
                        Segment(
                            start_ms=silence_start_ms,
                            end_ms=silence_end_ms,
                            type="silence",
                            confidence=0.9,
                        )
                    )

            # Add speech segment
            speech_start_ms = int(start_sample * 1000 / sample_rate)
            speech_end_ms = int(end_sample * 1000 / sample_rate)

            segments.append(
                Segment(
                    start_ms=speech_start_ms,
                    end_ms=speech_end_ms,
                    type="speech",
                    confidence=0.95,
                )
            )

            current_pos = end_sample

        # Add final silence segment if there's remaining audio
        if current_pos < total_samples:
            silence_start_ms = int(current_pos * 1000 / sample_rate)
            silence_end_ms = int(total_samples * 1000 / sample_rate)

            if (silence_end_ms - silence_start_ms) >= self.min_silence_duration_ms:
                segments.append(
                    Segment(
                        start_ms=silence_start_ms,
                        end_ms=silence_end_ms,
                        type="silence",
                        confidence=0.9,
                    )
                )

        return segments


def get_vad_processor(
    aggressiveness: Optional[int] = None,
    min_silence_duration_ms: Optional[int] = None,
    min_speech_duration_ms: Optional[int] = None,
) -> VADProcessor:
    """Get VAD processor instance with configuration."""
    return VADProcessor(
        aggressiveness=aggressiveness or settings.vad_aggressiveness,
        min_silence_duration_ms=min_silence_duration_ms or settings.min_silence_duration_ms,
        min_speech_duration_ms=min_speech_duration_ms or settings.min_speech_duration_ms,
    )
