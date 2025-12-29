"""Project schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.project import ProjectStatus


class ProcessingOptions(BaseModel):
    """Schema for processing options."""

    silence_removal: bool = True
    filler_word_filter: bool = False


class ProjectCreate(BaseModel):
    """Schema for creating a project."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    processing_options: Optional[ProcessingOptions] = None


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[ProjectStatus] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""

    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    thumbnail_url: Optional[str] = None
    processing_options: Optional[ProcessingOptions] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MediaFileBasicResponse(BaseModel):
    """Basic media file response for nested inclusion."""

    id: UUID
    original_filename: str
    file_size: int
    mime_type: str
    duration_seconds: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisBasicResponse(BaseModel):
    """Basic analysis response for nested inclusion."""

    id: UUID
    processing_mode: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class MediaFileWithAnalysisResponse(BaseModel):
    """Media file response with analysis results."""

    id: UUID
    original_filename: str
    file_size: int
    mime_type: str
    duration_seconds: Optional[float] = None
    created_at: datetime
    analysis_results: List[AnalysisBasicResponse] = []

    model_config = {"from_attributes": True}


class ProjectWithMediaResponse(BaseModel):
    """Schema for project response with media files and analysis."""

    id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    thumbnail_url: Optional[str] = None
    processing_options: Optional[ProcessingOptions] = None
    created_at: datetime
    updated_at: datetime
    media_files: List[MediaFileWithAnalysisResponse] = []

    model_config = {"from_attributes": True}


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int
    limit: int
    total: int
    total_pages: int


class ProjectListResponse(BaseModel):
    """Schema for paginated project list response."""

    projects: List[ProjectResponse]
    pagination: PaginationMeta
