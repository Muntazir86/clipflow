"""FFmpeg utilities for audio/video processing."""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from app.config import get_settings

settings = get_settings()


class FFmpegError(Exception):
    """Exception raised for FFmpeg errors."""

    pass


def get_media_duration(file_path: Path) -> Optional[float]:
    """Get media duration in seconds using FFprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            str(file_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return None

        data = json.loads(result.stdout)
        duration = data.get("format", {}).get("duration")
        return float(duration) if duration else None

    except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError):
        return None


def get_media_info(file_path: Path) -> Optional[dict]:
    """Get detailed media information using FFprobe."""
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(file_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return None

        return json.loads(result.stdout)

    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def extract_audio(
    input_path: Path,
    output_path: Optional[Path] = None,
    sample_rate: int = 16000,
    channels: int = 1,
) -> Path:
    """
    Extract audio from video file and convert to WAV format.

    Args:
        input_path: Path to input video/audio file
        output_path: Optional output path (creates temp file if not provided)
        sample_rate: Output sample rate (default 16kHz for VAD)
        channels: Number of audio channels (default mono)

    Returns:
        Path to extracted audio file
    """
    if output_path is None:
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / "audio.wav"

    cmd = [
        "ffmpeg",
        "-i",
        str(input_path),
        "-vn",  # No video
        "-acodec",
        "pcm_s16le",  # 16-bit PCM
        "-ar",
        str(sample_rate),  # Sample rate
        "-ac",
        str(channels),  # Channels
        "-y",  # Overwrite output
        str(output_path),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        if result.returncode != 0:
            raise FFmpegError(f"FFmpeg audio extraction failed: {result.stderr}")

        return output_path

    except subprocess.TimeoutExpired:
        raise FFmpegError("FFmpeg audio extraction timed out")


def generate_waveform_data(
    audio_path: Path,
    num_samples: int = 1000,
) -> Tuple[list, float, int]:
    """
    Generate waveform peak data for visualization.

    Args:
        audio_path: Path to audio file
        num_samples: Number of peak samples to generate

    Returns:
        Tuple of (peaks list, duration, sample_rate)
    """
    try:
        # Get audio info
        info = get_media_info(audio_path)
        if not info:
            raise FFmpegError("Could not get audio info")

        duration = float(info.get("format", {}).get("duration", 0))
        audio_stream = next(
            (s for s in info.get("streams", []) if s.get("codec_type") == "audio"),
            None,
        )
        sample_rate = int(audio_stream.get("sample_rate", 44100)) if audio_stream else 44100

        # Use FFmpeg to extract raw audio samples
        cmd = [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-f",
            "s16le",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "8000",  # Lower sample rate for waveform
            "-ac",
            "1",
            "-",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=120,
        )

        if result.returncode != 0:
            raise FFmpegError("Failed to extract audio for waveform")

        # Process raw audio data to get peaks
        import struct

        audio_data = result.stdout
        samples = struct.unpack(f"<{len(audio_data) // 2}h", audio_data)

        # Calculate peaks
        samples_per_peak = max(1, len(samples) // num_samples)
        peaks = []

        for i in range(0, len(samples), samples_per_peak):
            chunk = samples[i : i + samples_per_peak]
            if chunk:
                peak = max(abs(min(chunk)), abs(max(chunk))) / 32768.0
                peaks.append(round(peak, 4))

        # Ensure we have exactly num_samples peaks
        if len(peaks) > num_samples:
            peaks = peaks[:num_samples]

        return peaks, duration, sample_rate

    except subprocess.TimeoutExpired:
        raise FFmpegError("Waveform generation timed out")


def cut_segments_from_video(
    input_path: Path,
    output_path: Path,
    segments_to_keep: list[Tuple[float, float]],
) -> Path:
    """
    Cut video to keep only specified segments, removing everything else.
    
    Args:
        input_path: Path to input video file
        output_path: Path for output video file
        segments_to_keep: List of (start_seconds, end_seconds) tuples to keep
        
    Returns:
        Path to output video file
    """
    if not segments_to_keep:
        raise FFmpegError("No segments to keep")
    
    # Sort segments by start time
    segments_to_keep = sorted(segments_to_keep, key=lambda x: x[0])
    
    # Create a complex filter to concat segments
    # First, we need to create filter inputs for each segment
    filter_parts = []
    concat_inputs = []
    
    for i, (start, end) in enumerate(segments_to_keep):
        # Trim video and audio for each segment
        filter_parts.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}]"
        )
        filter_parts.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]"
        )
        concat_inputs.append(f"[v{i}][a{i}]")
    
    # Concat all segments
    n_segments = len(segments_to_keep)
    filter_complex = ";".join(filter_parts)
    filter_complex += f";{''.join(concat_inputs)}concat=n={n_segments}:v=1:a=1[outv][outa]"
    
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-y",
        str(output_path),
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout for longer videos
        )
        
        if result.returncode != 0:
            raise FFmpegError(f"FFmpeg cut failed: {result.stderr}")
        
        return output_path
        
    except subprocess.TimeoutExpired:
        raise FFmpegError("FFmpeg cut operation timed out")


def validate_media_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate that a file is a valid media file using FFprobe.

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        info = get_media_info(file_path)
        if not info:
            return False, "Could not read media file"

        streams = info.get("streams", [])
        has_audio = any(s.get("codec_type") == "audio" for s in streams)

        if not has_audio:
            return False, "Media file has no audio track"

        return True, None

    except Exception as e:
        return False, str(e)
