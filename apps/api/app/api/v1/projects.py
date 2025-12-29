"""Project API endpoints."""

import logging
import math
import uuid as uuid_lib
from io import BytesIO
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.api.deps import CurrentUser, DbSession
from app.services.storage_service import get_storage_service
from app.models.media import MediaFile
from app.models.project import Project, ProjectStatus
from app.schemas.auth import MessageResponse
from app.schemas.project import (
    PaginationMeta,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
    ProjectWithMediaResponse,
)

router = APIRouter()

storage_service = get_storage_service()
logger = logging.getLogger(__name__)


def _get_thumbnail_url(project: Project) -> Optional[str]:
    """Get the thumbnail URL for a project."""
    if not project.thumbnail_path:
        return None
    # For local storage, return a relative URL that the frontend can use
    # For S3, this would be a presigned URL
    return f"/api/v1/projects/{project.id}/thumbnail"


def _project_to_response(project: Project) -> ProjectResponse:
    """Convert a Project model to ProjectResponse with thumbnail URL."""
    from app.schemas.project import ProcessingOptions
    
    processing_opts = None
    if project.processing_options:
        processing_opts = ProcessingOptions(**project.processing_options)
    
    return ProjectResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        status=project.status,
        thumbnail_url=_get_thumbnail_url(project),
        processing_options=processing_opts,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def _project_with_media_to_response(project: Project) -> ProjectWithMediaResponse:
    """Convert a Project model to ProjectWithMediaResponse with thumbnail URL."""
    from app.schemas.project import MediaFileWithAnalysisResponse, ProcessingOptions
    
    processing_opts = None
    if project.processing_options:
        processing_opts = ProcessingOptions(**project.processing_options)
    
    return ProjectWithMediaResponse(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        description=project.description,
        status=project.status,
        thumbnail_url=_get_thumbnail_url(project),
        processing_options=processing_opts,
        created_at=project.created_at,
        updated_at=project.updated_at,
        media_files=[MediaFileWithAnalysisResponse.model_validate(mf) for mf in project.media_files],
    )


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    current_user: CurrentUser,
    db: DbSession,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[ProjectStatus] = None,
):
    """List all projects for the current user."""
    query = db.query(Project).filter(Project.user_id == current_user.id)

    if status:
        query = query.filter(Project.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    offset = (page - 1) * limit
    projects = (
        query.order_by(Project.created_at.desc()).offset(offset).limit(limit).all()
    )

    total_pages = math.ceil(total / limit) if total > 0 else 1

    return ProjectListResponse(
        projects=[_project_to_response(p) for p in projects],
        pagination=PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Create a new project."""
    processing_options = None
    if data.processing_options:
        processing_options = data.processing_options.model_dump()
    
    project = Project(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        processing_options=processing_options,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return _project_to_response(project)


@router.get("/{project_id}", response_model=ProjectWithMediaResponse)
async def get_project(
    project_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get a project with its media files and analysis results."""
    project = (
        db.query(Project)
        .options(
            joinedload(Project.media_files).joinedload(MediaFile.analysis_results)
        )
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Project not found",
            },
        )

    return _project_with_media_to_response(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update a project."""
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Project not found",
            },
        )

    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description
    if data.status is not None:
        project.status = data.status

    db.commit()
    db.refresh(project)

    return _project_to_response(project)


@router.delete("/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Delete a project and all associated files."""
    project = (
        db.query(Project)
        .options(joinedload(Project.media_files))
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Project not found",
            },
        )

    # Delete thumbnail file if exists
    if project.thumbnail_path:
        try:
            storage_service.delete_file(project.thumbnail_path)
        except Exception as e:
            # Log error but don't fail the deletion
            logger.warning(f"Failed to delete thumbnail {project.thumbnail_path}: {e}")

    # Delete all media files
    for media_file in project.media_files:
        try:
            storage_service.delete_file(media_file.file_path)
        except Exception as e:
            # Log error but don't fail the deletion
            logger.warning(f"Failed to delete media file {media_file.file_path}: {e}")

    # Delete the project (this will cascade delete media_files and analysis_results due to relationships)
    db.delete(project)
    db.commit()

    return MessageResponse(message="Project deleted successfully")


@router.post("/{project_id}/thumbnail", response_model=ProjectResponse)
async def upload_thumbnail(
    project_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    """Upload a thumbnail image for a project."""
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Project not found",
            },
        )

    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_FILE_TYPE",
                "message": "File must be an image",
            },
        )

    # Delete old thumbnail if exists
    if project.thumbnail_path:
        storage_service.delete_file(project.thumbnail_path)

    # Generate unique filename
    ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
    filename = f"thumbnails/{project_id}_{uuid_lib.uuid4().hex[:8]}.{ext}"

    # Save file
    contents = await file.read()
    storage_service.save_file(BytesIO(contents), filename)

    # Update project
    project.thumbnail_path = filename
    db.commit()
    db.refresh(project)

    return _project_to_response(project)


@router.get("/{project_id}/thumbnail")
async def get_thumbnail(
    project_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get the thumbnail image for a project."""
    from fastapi.responses import Response

    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == current_user.id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Project not found",
            },
        )

    if not project.thumbnail_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Thumbnail not found",
            },
        )

    contents = storage_service.get_file(project.thumbnail_path)
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Thumbnail file not found",
            },
        )

    # Determine content type from extension
    ext = project.thumbnail_path.split(".")[-1].lower()
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }.get(ext, "image/jpeg")

    return Response(content=contents, media_type=content_type)
