"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "ClipFlow API"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "your-secret-key-here-change-in-production"
    api_version: str = "v1"

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/videocut"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT Configuration
    jwt_secret_key: str = "your-jwt-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # File Storage
    storage_type: str = "local"  # local | s3
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 500
    allowed_extensions: str = "mp4,webm,mov,avi,mkv,mp3,wav,m4a"

    # S3 Configuration
    s3_bucket_name: Optional[str] = None
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_region: Optional[str] = None
    s3_endpoint_url: Optional[str] = None

    # AI Features Toggle
    ai_features_enabled: bool = False
    whisper_api_enabled: bool = False
    openai_api_key: Optional[str] = None

    # Processing Configuration
    default_processing_mode: str = "vad"  # vad | whisper
    vad_aggressiveness: int = 3  # 1-3
    min_silence_duration_ms: int = 300
    min_speech_duration_ms: int = 250
    silence_threshold_db: int = -40

    # Filler Words Configuration
    detect_filler_words: bool = True
    filler_words: str = "um,uh,like,you know,basically,actually,literally,so,well,I mean"
    filler_word_padding_ms: int = 100

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 3600  # seconds

    # CORS Configuration
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        """Return allowed extensions as a list."""
        return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]

    @property
    def filler_words_list(self) -> List[str]:
        """Return filler words as a list."""
        return [word.strip().lower() for word in self.filler_words.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        """Return max file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024

    @field_validator("vad_aggressiveness")
    @classmethod
    def validate_vad_aggressiveness(cls, v: int) -> int:
        if v < 1 or v > 3:
            raise ValueError("vad_aggressiveness must be between 1 and 3")
        return v

@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
