"""Tests for analysis endpoints."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


class TestStartAnalysis:
    """Tests for starting analysis."""

    def test_start_analysis_media_not_found(self, client: TestClient, auth_headers):
        """Test starting analysis for nonexistent media."""
        response = client.post(
            f"/api/v1/analysis/media/{uuid4()}/analyze",
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_start_analysis_whisper_disabled(
        self, client: TestClient, auth_headers, test_project, db_session
    ):
        """Test starting whisper analysis when AI is disabled."""
        # Create a media file
        from app.models.media import MediaFile

        media = MediaFile(
            id=uuid4(),
            project_id=test_project.id,
            original_filename="test.mp4",
            stored_filename="test_stored.mp4",
            file_path="/tmp/test.mp4",
            file_size=1000,
            mime_type="video/mp4",
        )
        db_session.add(media)
        db_session.commit()

        response = client.post(
            f"/api/v1/analysis/media/{media.id}/analyze",
            headers=auth_headers,
            json={"processing_mode": "whisper"},
        )
        assert response.status_code == 403
        assert "AI_FEATURES_DISABLED" in response.json()["detail"]["code"]


class TestGetAnalysis:
    """Tests for getting analysis results."""

    def test_get_analysis_not_found(self, client: TestClient, auth_headers):
        """Test getting nonexistent analysis."""
        response = client.get(
            f"/api/v1/analysis/{uuid4()}",
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestGetAnalysisStatus:
    """Tests for getting analysis status."""

    def test_get_status_not_found(self, client: TestClient, auth_headers):
        """Test getting status for nonexistent analysis."""
        response = client.get(
            f"/api/v1/analysis/{uuid4()}/status",
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestConfigEndpoint:
    """Tests for configuration endpoint."""

    def test_get_features(self, client: TestClient):
        """Test getting features configuration (public endpoint)."""
        response = client.get("/api/v1/config/features")
        assert response.status_code == 200
        data = response.json()
        assert "ai_features_enabled" in data
        assert "whisper_available" in data
        assert "max_file_size_mb" in data
        assert "allowed_extensions" in data
        assert "default_processing_mode" in data
