"""Analysis schemas."""

from datetime import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.analysis import AnalysisStatus, ProcessingMode


class AnalysisCreate(BaseModel):
    """Schema for creating an analysis request."""

    processing_mode: Optional[Literal["vad", "whisper", "auto"]] = "auto"
    vad_aggressiveness: Optional[int] = Field(None, ge=1, le=3)
    min_silence_duration_ms: Optional[int] = Field(None, ge=100, le=5000)
    min_speech_duration_ms: Optional[int] = Field(None, ge=100, le=5000)
    detect_filler_words: Optional[bool] = None
    custom_filler_words: Optional[List[str]] = None


class SegmentResponse(BaseModel):
    """Schema for a single segment in analysis results."""

    start_ms: int
    end_ms: int
    type: Literal["speech", "silence", "filler"]
    confidence: float
    text: Optional[str] = None
    filler_word: Optional[str] = None


class FillerWordDetection(BaseModel):
    """Schema for detected filler word."""

    word: str
    start_ms: int
    end_ms: int
    confidence: float


class AnalysisResponse(BaseModel):
    """Schema for full analysis response."""

    id: UUID
    media_file_id: UUID
    processing_mode: ProcessingMode
    status: AnalysisStatus
    segments: Optional[List[SegmentResponse]] = None
    transcription: Optional[str] = None
    filler_words_detected: Optional[List[FillerWordDetection]] = None
    processing_time_ms: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AnalysisStatusResponse(BaseModel):
    """Schema for lightweight analysis status check."""

    status: AnalysisStatus
    progress_percent: Optional[int] = None
    error_message: Optional[str] = None


class AnalysisStartResponse(BaseModel):
    """Schema for analysis start response."""

    analysis_id: UUID
    status: AnalysisStatus = AnalysisStatus.PROCESSING


class WaveformResponse(BaseModel):
    """Schema for waveform data response."""

    peaks: List[float]
    duration: float
    sample_rate: int
