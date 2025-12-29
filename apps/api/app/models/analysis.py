"""Analysis result database model."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.media import MediaFile


class ProcessingMode(str, enum.Enum):
    """Processing mode enumeration."""

    VAD = "vad"
    WHISPER = "whisper"


class AnalysisStatus(str, enum.Enum):
    """Analysis status enumeration."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisResult(Base):
    """Analysis result model for storing audio analysis data."""

    __tablename__ = "analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    media_file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("media_files.id", ondelete="CASCADE"),
        nullable=False,
    )
    processing_mode: Mapped[ProcessingMode] = mapped_column(
        Enum(ProcessingMode), nullable=False
    )
    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus), default=AnalysisStatus.PENDING
    )
    segments: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    transcription: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    filler_words_detected: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    media_file: Mapped["MediaFile"] = relationship(
        "MediaFile", back_populates="analysis_results"
    )

    def __repr__(self) -> str:
        return f"<AnalysisResult {self.id} - {self.status}>"
