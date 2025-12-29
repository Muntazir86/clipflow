"""Configuration API endpoints."""

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import get_settings

router = APIRouter()
settings = get_settings()


class FeaturesResponse(BaseModel):
    """Schema for features configuration response."""

    # ai_features_enabled: bool
    # whisper_available: bool
    filler_detection_available: bool
    max_file_size_mb: int
    allowed_extensions: List[str]
    default_processing_mode: str


@router.get("/features", response_model=FeaturesResponse)
async def get_features():
    """Get available features and configuration (public endpoint)."""
    return FeaturesResponse(
        # ai_features_enabled=settings.ai_features_enabled,
        # whisper_available=settings.ai_features_enabled and settings.whisper_api_enabled,
        filler_detection_available=settings.ai_features_enabled
        and settings.whisper_api_enabled
        and settings.detect_filler_words,
        max_file_size_mb=settings.max_file_size_mb,
        allowed_extensions=settings.allowed_extensions_list,
        default_processing_mode=settings.default_processing_mode,
    )
