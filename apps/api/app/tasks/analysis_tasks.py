"""Celery tasks for audio analysis processing."""

import shutil
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import UUID

from celery import shared_task
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.analysis import AnalysisResult, AnalysisStatus, ProcessingMode
from app.models.media import MediaFile
from app.services.audio_extractor import get_audio_extractor
from app.services.segment_processor import get_segment_processor
from app.services.storage_service import get_storage_service
from app.services.vad_processor import get_vad_processor
from app.tasks.celery_app import celery_app

settings = get_settings()


def get_db() -> Session:
    """Get database session for tasks."""
    return SessionLocal()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_audio_analysis(self, analysis_id: str, options: Dict[str, Any]):
    """
    Main processing task for audio analysis.

    Args:
        analysis_id: UUID of the analysis record
        options: Processing options including:
            - processing_mode: "vad" or "whisper"
            - vad_aggressiveness: 1-3
            - min_silence_duration_ms: minimum silence duration
            - min_speech_duration_ms: minimum speech duration
            - detect_filler_words: whether to detect filler words
            - custom_filler_words: additional filler words to detect
    """
    db = get_db()
    temp_dir = None
    start_time = time.time()

    try:
        # Get analysis record
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        # Update status
        analysis.status = AnalysisStatus.PROCESSING
        db.commit()

        # Get media file
        media_file = db.query(MediaFile).filter(MediaFile.id == analysis.media_file_id).first()
        if not media_file:
            raise ValueError(f"Media file not found for analysis {analysis_id}")

        # Get storage service
        storage = get_storage_service()

        # Get local file path
        local_path = storage.get_local_path(media_file.stored_filename)
        if not local_path or not local_path.exists():
            raise ValueError("Media file not found on storage")

        # Create temp directory for processing
        temp_dir = Path(tempfile.mkdtemp())

        # Extract audio
        audio_extractor = get_audio_extractor()
        audio_path = audio_extractor.extract_audio_from_file(
            file_path=local_path,
            output_dir=temp_dir,
        )

        # Process based on mode
        processing_mode = options.get("processing_mode", "vad")
        segments = []
        transcription = None
        filler_words_detected = None

        if processing_mode == "whisper" and settings.ai_features_enabled and settings.whisper_api_enabled:
            # Use Whisper processor
            from app.services.whisper_processor import get_whisper_processor

            whisper = get_whisper_processor(
                detect_filler_words=options.get("detect_filler_words", True),
                custom_filler_words=options.get("custom_filler_words"),
            )

            whisper_segments, transcription, filler_words = whisper.process_audio(
                audio_path=audio_path,
                vad_aggressiveness=options.get("vad_aggressiveness", 3),
                min_silence_duration_ms=options.get("min_silence_duration_ms", 300),
                min_speech_duration_ms=options.get("min_speech_duration_ms", 250),
            )

            # Convert to dict format
            segments = [
                {
                    "start_ms": s.start_ms,
                    "end_ms": s.end_ms,
                    "type": s.type,
                    "confidence": s.confidence,
                    "text": s.text,
                    "filler_word": s.filler_word,
                }
                for s in whisper_segments
            ]

            filler_words_detected = [
                {
                    "word": fw.word,
                    "start_ms": fw.start_ms,
                    "end_ms": fw.end_ms,
                    "confidence": fw.confidence,
                }
                for fw in filler_words
            ]

        else:
            # Use VAD processor
            vad = get_vad_processor(
                aggressiveness=options.get("vad_aggressiveness", 3),
                min_silence_duration_ms=options.get("min_silence_duration_ms", 300),
                min_speech_duration_ms=options.get("min_speech_duration_ms", 250),
            )

            vad_segments = vad.process_audio(audio_path)

            # Convert to dict format
            segments = [
                {
                    "start_ms": s.start_ms,
                    "end_ms": s.end_ms,
                    "type": s.type,
                    "confidence": s.confidence,
                }
                for s in vad_segments
            ]

        # Post-process segments
        segment_processor = get_segment_processor(
            min_silence_duration_ms=options.get("min_silence_duration_ms", 300),
            min_speech_duration_ms=options.get("min_speech_duration_ms", 250),
        )

        total_duration_ms = int((media_file.duration_seconds or 0) * 1000)
        processed_segments = segment_processor.process_segments(segments, total_duration_ms)

        # Convert processed segments to dict
        final_segments = [s.to_dict() for s in processed_segments]

        # Calculate processing time
        processing_time_ms = int((time.time() - start_time) * 1000)

        # Update analysis record
        analysis.status = AnalysisStatus.COMPLETED
        analysis.segments = final_segments
        analysis.transcription = transcription
        analysis.filler_words_detected = filler_words_detected
        analysis.processing_time_ms = processing_time_ms
        analysis.completed_at = datetime.now(timezone.utc)
        db.commit()

    except Exception as e:
        # Handle failure
        db.rollback()

        try:
            analysis = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = str(e)[:1000]
                db.commit()
        except Exception:
            pass

        # Retry if retries remaining
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e)

        raise

    finally:
        # Cleanup temp directory
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

        db.close()


@celery_app.task
def cleanup_expired_files():
    """
    Periodic task to cleanup expired files.

    - Delete uploaded files older than 30 days
    - Delete orphaned analysis results
    - Clear temporary processing files
    """
    db = get_db()

    try:
        # Get cutoff date (30 days ago)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

        # Find old media files
        old_media_files = (
            db.query(MediaFile)
            .filter(MediaFile.created_at < cutoff_date)
            .all()
        )

        storage = get_storage_service()
        deleted_count = 0

        for media_file in old_media_files:
            # Delete from storage
            storage.delete_file(media_file.file_path)

            # Delete from database (cascades to analysis results)
            db.delete(media_file)
            deleted_count += 1

        db.commit()

        # Cleanup temp directories
        temp_base = Path(tempfile.gettempdir())
        for temp_dir in temp_base.glob("tmp*"):
            if temp_dir.is_dir():
                try:
                    # Check if directory is old (more than 1 day)
                    dir_age = datetime.now() - datetime.fromtimestamp(temp_dir.stat().st_mtime)
                    if dir_age > timedelta(days=1):
                        shutil.rmtree(temp_dir, ignore_errors=True)
                except Exception:
                    pass

        return {"deleted_files": deleted_count}

    except Exception as e:
        db.rollback()
        raise

    finally:
        db.close()
