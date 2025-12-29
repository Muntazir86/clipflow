"""File handling utilities."""

import mimetypes
import os
import secrets
from pathlib import Path
from typing import Optional, Tuple

from app.config import get_settings

settings = get_settings()

# Magic bytes for common video/audio formats
MAGIC_BYTES = {
    b"\x00\x00\x00\x18ftypmp42": "video/mp4",
    b"\x00\x00\x00\x1cftypmp42": "video/mp4",
    b"\x00\x00\x00\x20ftypmp42": "video/mp4",
    b"\x00\x00\x00\x18ftypisom": "video/mp4",
    b"\x00\x00\x00\x1cftypisom": "video/mp4",
    b"\x00\x00\x00\x20ftypisom": "video/mp4",
    b"\x00\x00\x00\x18ftypM4V": "video/mp4",
    b"\x00\x00\x00\x1cftypM4V": "video/mp4",
    b"\x1aE\xdf\xa3": "video/webm",
    b"\x00\x00\x00\x14ftypqt": "video/quicktime",
    b"\x00\x00\x00\x08moov": "video/quicktime",
    b"RIFF": "video/avi",
    b"ID3": "audio/mpeg",
    b"\xff\xfb": "audio/mpeg",
    b"\xff\xfa": "audio/mpeg",
    b"RIFF....WAVE": "audio/wav",
    b"\x00\x00\x00\x18ftypM4A": "audio/m4a",
    b"\x00\x00\x00\x20ftypM4A": "audio/m4a",
}


def validate_file_extension(filename: str) -> bool:
    """Validate file extension against allowed extensions."""
    ext = Path(filename).suffix.lower().lstrip(".")
    return ext in settings.allowed_extensions_list


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename."""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def validate_magic_bytes(file_content: bytes) -> Optional[str]:
    """Validate file magic bytes and return detected MIME type."""
    # Check for MP4/MOV (ftyp box)
    if len(file_content) >= 12:
        # MP4/MOV files have ftyp at offset 4
        if file_content[4:8] == b"ftyp":
            brand = file_content[8:12]
            if brand in (b"isom", b"mp42", b"mp41", b"M4V ", b"M4A ", b"qt  "):
                if brand == b"M4A ":
                    return "audio/m4a"
                return "video/mp4"
            if brand == b"qt  ":
                return "video/quicktime"

    # Check for WebM/MKV
    if file_content[:4] == b"\x1aE\xdf\xa3":
        return "video/webm"

    # Check for AVI
    if file_content[:4] == b"RIFF" and file_content[8:12] == b"AVI ":
        return "video/avi"

    # Check for WAV
    if file_content[:4] == b"RIFF" and file_content[8:12] == b"WAVE":
        return "audio/wav"

    # Check for MP3
    if file_content[:3] == b"ID3" or file_content[:2] in (b"\xff\xfb", b"\xff\xfa"):
        return "audio/mpeg"

    return None


def generate_stored_filename(original_filename: str) -> str:
    """Generate a random filename for storage while preserving extension."""
    ext = Path(original_filename).suffix.lower()
    random_name = secrets.token_hex(16)
    return f"{random_name}{ext}"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and other issues."""
    # Remove path components
    filename = Path(filename).name
    # Remove null bytes and other dangerous characters
    dangerous_chars = ["\x00", "/", "\\", "..", ":", "*", "?", '"', "<", ">", "|"]
    for char in dangerous_chars:
        filename = filename.replace(char, "_")
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[: 255 - len(ext)] + ext
    return filename


def get_file_path(stored_filename: str) -> Path:
    """Get the full file path for a stored file."""
    return Path(settings.upload_dir) / stored_filename


def ensure_upload_dir() -> Path:
    """Ensure upload directory exists and return path."""
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size


def delete_file(file_path: Path) -> bool:
    """Delete a file if it exists."""
    try:
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def validate_file_size(file_size: int) -> Tuple[bool, Optional[str]]:
    """Validate file size against maximum allowed."""
    if file_size > settings.max_file_size_bytes:
        return False, f"File size exceeds maximum allowed ({settings.max_file_size_mb}MB)"
    return True, None
