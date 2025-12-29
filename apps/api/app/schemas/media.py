"""Media file schemas."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

class ProcessVideoOptions(BaseModel):
    """Schema for video processing options."""

    silence_removal: bool = False
    filler_word_filter: bool = False


class MediaFileResponse(BaseModel):
    """Schema for media file response."""

    id: UUID
    project_id: UUID
    original_filename: str
    stored_filename: str
    file_size: int
    mime_type: str
    duration_seconds: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PresignedUploadRequest(BaseModel):
    """Schema for presigned URL upload request."""

    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str
    file_size: int = Field(..., gt=0)


class PresignedUploadResponse(BaseModel):
    """Schema for presigned URL upload response."""

    upload_url: str
    file_id: UUID


class UploadConfirmResponse(BaseModel):
    """Schema for upload confirmation response."""

    media_file: MediaFileResponse
