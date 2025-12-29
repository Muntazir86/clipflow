"""Analysis API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.config import get_settings
from app.models.analysis import AnalysisResult, AnalysisStatus, ProcessingMode
from app.models.media import MediaFile
from app.models.project import Project
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse,
    AnalysisStartResponse,
    AnalysisStatusResponse,
)

router = APIRouter()
settings = get_settings()


@router.post(
    "/media/{media_id}/analyze",
    response_model=AnalysisStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_analysis(
    media_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
    data: AnalysisCreate = AnalysisCreate(),
):
    """Start audio analysis for a media file."""
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

    # Determine processing mode
    processing_mode = data.processing_mode or "auto"

    if processing_mode == "auto":
        processing_mode = settings.default_processing_mode

    if processing_mode == "whisper":
        if not settings.ai_features_enabled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AI_FEATURES_DISABLED",
                    "message": "AI features are not enabled on this server",
                },
            )
        if not settings.whisper_api_enabled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AI_FEATURES_DISABLED",
                    "message": "Whisper API is not enabled on this server",
                },
            )

    # Create analysis record
    analysis = AnalysisResult(
        media_file_id=media_id,
        processing_mode=ProcessingMode(processing_mode),
        status=AnalysisStatus.PENDING,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Trigger Celery task
    try:
        from app.tasks.analysis_tasks import process_audio_analysis

        process_audio_analysis.delay(
            str(analysis.id),
            {
                "processing_mode": processing_mode,
                "vad_aggressiveness": data.vad_aggressiveness
                or settings.vad_aggressiveness,
                "min_silence_duration_ms": data.min_silence_duration_ms
                or settings.min_silence_duration_ms,
                "min_speech_duration_ms": data.min_speech_duration_ms
                or settings.min_speech_duration_ms,
                "detect_filler_words": data.detect_filler_words
                if data.detect_filler_words is not None
                else settings.detect_filler_words,
                "custom_filler_words": data.custom_filler_words or [],
            },
        )

        # Update status to processing
        analysis.status = AnalysisStatus.PROCESSING
        db.commit()

    except Exception as e:
        # If task submission fails, mark as failed
        analysis.status = AnalysisStatus.FAILED
        analysis.error_message = f"Failed to start processing: {str(e)}"
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "PROCESSING_FAILED",
                "message": "Failed to start analysis task",
            },
        )

    return AnalysisStartResponse(
        analysis_id=analysis.id,
        status=analysis.status,
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get analysis result."""
    analysis = (
        db.query(AnalysisResult)
        .join(MediaFile)
        .join(Project)
        .filter(AnalysisResult.id == analysis_id, Project.user_id == current_user.id)
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Analysis not found",
            },
        )

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}/status", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    analysis_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
):
    """Get lightweight analysis status for polling."""
    analysis = (
        db.query(AnalysisResult)
        .join(MediaFile)
        .join(Project)
        .filter(AnalysisResult.id == analysis_id, Project.user_id == current_user.id)
        .first()
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": "Analysis not found",
            },
        )

    # Calculate progress (simplified)
    progress = None
    if analysis.status == AnalysisStatus.PENDING:
        progress = 0
    elif analysis.status == AnalysisStatus.PROCESSING:
        progress = 50  # Could be more granular with task progress tracking
    elif analysis.status == AnalysisStatus.COMPLETED:
        progress = 100
    elif analysis.status == AnalysisStatus.FAILED:
        progress = None

    return AnalysisStatusResponse(
        status=analysis.status,
        progress_percent=progress,
        error_message=analysis.error_message,
    )
