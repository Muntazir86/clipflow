"""Media upload and management API endpoints."""

import os
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import StreamingResponse

from app.api.deps import CurrentUser, DbSession
from app.config import get_settings
from app.models.media import MediaFile
from app.models.project import Project
from app.schemas.analysis import WaveformResponse
from app.schemas.media import (
    MediaFileResponse,
    PresignedUploadRequest,
    PresignedUploadResponse,
    UploadConfirmResponse,
    ProcessVideoOptions,
)
from app.services.storage_service import get_storage_service
from app.services.waveform_generator import get_waveform_generator
from app.utils.ffmpeg_utils import get_media_duration
from app.utils.file_utils import (
    generate_stored_filename,
    get_mime_type,
    sanitize_filename,
    validate_file_extension,
    validate_file_size,
    validate_magic_bytes,
)

router = APIRouter()
settings = get_settings()


@router.post(
    "/projects/{project_id}/upload",
    response_model=MediaFileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_media(
    project_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
):
    """Upload a media file to a project."""
    # Verify project ownership
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

    # Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Filename is required",
            },
        )

    original_filename = sanitize_filename(file.filename)

    # Validate extension
    if not validate_file_extension(original_filename):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={
                "code": "UNSUPPORTED_FORMAT",
                "message": f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions_list)}",
            },
        )

    # Read file content
    content = await file.read()
    file_size = len(content)

    # Validate file size
    is_valid, error = validate_file_size(file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "code": "FILE_TOO_LARGE",
                "message": error,
            },
        )

    # Validate magic bytes
    detected_mime = validate_magic_bytes(content[:32])
    if detected_mime is None:
        # Fall back to extension-based mime type
        detected_mime = get_mime_type(original_filename)

    # Generate stored filename
    stored_filename = generate_stored_filename(original_filename)

    # Save file
    storage = get_storage_service()
    import io

    file_path = storage.save_file(io.BytesIO(content), stored_filename)

    # Get media duration
    duration = None
    local_path = storage.get_local_path(stored_filename)
    if local_path:
        duration = get_media_duration(local_path)

    # Create database record
    media_file = MediaFile(
        project_id=project_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=detected_mime or "application/octet-stream",
        duration_seconds=duration,
    )
    db.add(media_file)
    db.commit()
    db.refresh(media_file)

    return MediaFileResponse.model_validate(media_file)


@router.post("/upload/presigned", response_model=PresignedUploadResponse)
async def get_presigned_upload_url(
    data: PresignedUploadRequest,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get a presigned URL for direct S3 upload."""
    # Validate extension
    if not validate_file_extension(data.filename):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={
                "code": "UNSUPPORTED_FORMAT",
                "message": f"File type not allowed. Allowed types: {', '.join(settings.allowed_extensions_list)}",
            },
        )

    # Validate file size
    is_valid, error = validate_file_size(data.file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "code": "FILE_TOO_LARGE",
                "message": error,
            },
        )

    # Generate stored filename
    stored_filename = generate_stored_filename(data.filename)

    # Get presigned URL
    storage = get_storage_service()
    upload_url = storage.get_presigned_upload_url(stored_filename, data.content_type)

    if not upload_url:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={
                "code": "NOT_IMPLEMENTED",
                "message": "Presigned uploads are only available with S3 storage",
            },
        )

    # Create pending media file record
    import uuid

    file_id = uuid.uuid4()

    # Store pending upload info (in production, use Redis or database)
    # For now, we'll handle this in the confirm endpoint

    return PresignedUploadResponse(
        upload_url=upload_url,
        file_id=file_id,
    )


@router.post("/upload/confirm/{file_id}", response_model=UploadConfirmResponse)
async def confirm_upload(
    file_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Confirm that a presigned URL upload has completed."""
    # TODO: Implement presigned upload confirmation
    # This requires storing pending upload metadata
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "code": "NOT_IMPLEMENTED",
            "message": "Presigned upload confirmation not yet implemented",
        },
    )


@router.get("/{media_id}/stream")
async def stream_media(
    media_id: UUID,
    request: Request,
    db: DbSession,
    token: str | None = None,
):
    """Stream a media file with range request support."""
    from jose import JWTError, jwt
    from app.config import get_settings
    from app.models.user import User
    
    settings = get_settings()
    
    # Authenticate via query token (for video elements that can't set headers)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Token required"},
        )
    
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = payload.get("sub")
        token_type = payload.get("type")
        
        if not user_id or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "UNAUTHORIZED", "message": "Invalid token"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "Invalid token"},
        )
    
    # Get media file with project ownership check
    media_file = (
        db.query(MediaFile)
        .join(Project)
        .filter(MediaFile.id == media_id, Project.user_id == user_id)
        .first()
    )

    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Media file not found",
            },
        )

    # Get local file path
    storage = get_storage_service()
    local_path = storage.get_local_path(media_file.stored_filename)

    if not local_path or not local_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Media file not found on storage",
            },
        )

    file_size = local_path.stat().st_size
    content_type = media_file.mime_type or "video/mp4"

    # Handle range requests for video seeking
    range_header = request.headers.get("range")
    
    if range_header:
        # Parse range header
        range_match = range_header.replace("bytes=", "").split("-")
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        
        if start >= file_size:
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Range not satisfiable",
            )
        
        end = min(end, file_size - 1)
        content_length = end - start + 1

        def iter_file():
            with open(local_path, "rb") as f:
                f.seek(start)
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(8192, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        return StreamingResponse(
            iter_file(),
            status_code=206,
            media_type=content_type,
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
            },
        )
    else:
        # Full file response
        def iter_full_file():
            with open(local_path, "rb") as f:
                while chunk := f.read(8192):
                    yield chunk

        return StreamingResponse(
            iter_full_file(),
            media_type=content_type,
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
            },
        )


@router.get("/{media_id}/waveform", response_model=WaveformResponse)
async def get_waveform(
    media_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get waveform data for a media file."""
    # Get media file with project ownership check
    media_file = (
        db.query(MediaFile)
        .join(Project)
        .filter(MediaFile.id == media_id, Project.user_id == current_user.id)
        .first()
    )

    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Media file not found",
            },
        )

    # Get local file path
    storage = get_storage_service()
    local_path = storage.get_local_path(media_file.stored_filename)

    if not local_path or not local_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Media file not found on storage",
            },
        )

    # Generate waveform
    try:
        waveform_gen = get_waveform_generator()
        peaks, duration, sample_rate = waveform_gen.generate_from_file(local_path)

        return WaveformResponse(
            peaks=peaks,
            duration=duration,
            sample_rate=sample_rate,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "PROCESSING_FAILED",
                "message": f"Failed to generate waveform: {str(e)}",
            },
        )


@router.post("/{media_id}/process-video", response_model=MediaFileResponse)
async def process_video(
    media_id: UUID,
    options: ProcessVideoOptions,
    current_user: CurrentUser,
    db: DbSession,
):
    """
    Process a video by removing silence and/or filler words based on options.
    
    Uses the analysis results to identify segments to remove based on processing options,
    keeping only the desired portions of the video.
    """
    from app.models.analysis import AnalysisResult, AnalysisStatus
    from app.utils.ffmpeg_utils import cut_segments_from_video, FFmpegError
    import uuid as uuid_module
    
    # Get media file and verify ownership
    media_file = db.query(MediaFile).filter(MediaFile.id == media_id).first()
    
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "NOT_FOUND", "message": "Media file not found"},
        )
    
    # Verify project ownership
    project = (
        db.query(Project)
        .filter(Project.id == media_file.project_id, Project.user_id == current_user.id)
        .first()
    )
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Access denied"},
        )
    
    # Get the latest completed analysis for this media file
    analysis = (
        db.query(AnalysisResult)
        .filter(
            AnalysisResult.media_file_id == media_id,
            AnalysisResult.status == AnalysisStatus.COMPLETED,
        )
        .order_by(AnalysisResult.completed_at.desc())
        .first()
    )
    
    if not analysis or not analysis.segments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "NO_ANALYSIS",
                "message": "No completed analysis found. Please analyze the video first.",
            },
        )
    
    # Get the source file path
    storage = get_storage_service()
    source_path = storage.get_local_path(media_file.stored_filename)
    
    if not source_path or not source_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "FILE_NOT_FOUND", "message": "Source video file not found"},
        )
    
    # Validate options - at least one processing option must be enabled
    if not options.silence_removal and not options.filler_word_filter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_OPTIONS",
                "message": "At least one processing option must be enabled (silence_removal or filler_word_filter).",
            },
        )
    
    # Calculate segments to remove based on options
    # Segments in analysis have: type, start_ms, end_ms, filler_word (optional)
    segments_to_remove = []
    
    if options.silence_removal:
        silence_segments = [
            (seg["start_ms"] / 1000, seg["end_ms"] / 1000)
            for seg in analysis.segments
            if seg.get("type") == "silence"
        ]
        segments_to_remove.extend(silence_segments)
    
    if options.filler_word_filter:
        filler_segments = [
            (seg["start_ms"] / 1000, seg["end_ms"] / 1000)
            for seg in analysis.segments
            if seg.get("type") == "filler"
        ]
        segments_to_remove.extend(filler_segments)
    
    if not segments_to_remove:
        processing_types = []
        if options.silence_removal:
            processing_types.append("silence")
        if options.filler_word_filter:
            processing_types.append("filler words")
        processing_types_str = " or ".join(processing_types)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "NO_SEGMENTS",
                "message": f"No {processing_types_str} segments found to remove.",
            },
        )
    
    # Sort segments to remove by start time
    segments_to_remove.sort(key=lambda x: x[0])
    
    # Calculate segments to keep (the gaps between segments to remove)
    duration = media_file.duration_seconds or 0
    segments_to_keep = []
    current_pos = 0.0
    
    for segment_start, segment_end in segments_to_remove:
        if current_pos < segment_start:
            # Keep the segment before this removal segment
            segments_to_keep.append((current_pos, segment_start))
        current_pos = segment_end
    
    # Add final segment if there's content after last removal segment
    if current_pos < duration:
        segments_to_keep.append((current_pos, duration))
    
    if not segments_to_keep:
        processing_types = []
        if options.silence_removal:
            processing_types.append("silence")
        if options.filler_word_filter:
            processing_types.append("filler words")
        processing_types_str = " and ".join(processing_types)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "NO_CONTENT",
                "message": f"No content would remain after removing {processing_types_str}.",
            },
        )
    
    # Generate output filename based on processing options
    original_name = media_file.original_filename
    name_parts = original_name.rsplit(".", 1)
    
    # Build suffix based on processing options
    suffix_parts = []
    if options.silence_removal:
        suffix_parts.append("silence")
    if options.filler_word_filter:
        suffix_parts.append("filler")
    suffix = "_".join(suffix_parts)
    
    if len(name_parts) == 2:
        output_original_name = f"{name_parts[0]}_processed_{suffix}.{name_parts[1]}"
    else:
        output_original_name = f"{original_name}_processed_{suffix}"
    
    output_stored_name = f"processed/{uuid_module.uuid4()}_{output_original_name}"
    output_path = Path(settings.upload_dir) / output_stored_name
    
    # Ensure the processed directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Process the video
    try:
        cut_segments_from_video(source_path, output_path, segments_to_keep)
    except FFmpegError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "PROCESSING_FAILED",
                "message": f"Failed to process video: {str(e)}",
            },
        )
    
    # Get the new file size and duration
    new_file_size = output_path.stat().st_size
    new_duration = get_media_duration(output_path)
    
    # Create new media file record for the processed video
    new_media_file = MediaFile(
        project_id=media_file.project_id,
        original_filename=output_original_name,
        stored_filename=output_stored_name,
        file_path=str(output_path),
        file_size=new_file_size,
        mime_type=media_file.mime_type,
        duration_seconds=new_duration,
    )
    db.add(new_media_file)
    db.commit()
    db.refresh(new_media_file)
    
    return MediaFileResponse.model_validate(new_media_file)
