"""Tests for project endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestListProjects:
    """Tests for listing projects."""

    def test_list_projects_empty(self, client: TestClient, auth_headers):
        """Test listing projects when none exist."""
        response = client.get("/api/v1/projects", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["projects"] == []
        assert data["pagination"]["total"] == 0

    def test_list_projects_with_data(self, client: TestClient, auth_headers, test_project):
        """Test listing projects with existing data."""
        response = client.get("/api/v1/projects", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["projects"]) == 1
        assert data["projects"][0]["name"] == "Test Project"

    def test_list_projects_pagination(self, client: TestClient, auth_headers):
        """Test project list pagination."""
        response = client.get(
            "/api/v1/projects",
            headers=auth_headers,
            params={"page": 1, "limit": 10},
        )
        assert response.status_code == 200
        data = response.json()
        assert "pagination" in data
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 10

    def test_list_projects_unauthorized(self, client: TestClient):
        """Test listing projects without auth."""
        response = client.get("/api/v1/projects")
        assert response.status_code == 403


class TestCreateProject:
    """Tests for creating projects."""

    def test_create_project_success(self, client: TestClient, auth_headers):
        """Test successful project creation."""
        response = client.post(
            "/api/v1/projects",
            headers=auth_headers,
            json={
                "name": "New Project",
                "description": "A new project description",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Project"
        assert data["description"] == "A new project description"
        assert data["status"] == "created"

    def test_create_project_minimal(self, client: TestClient, auth_headers):
        """Test project creation with minimal data."""
        response = client.post(
            "/api/v1/projects",
            headers=auth_headers,
            json={"name": "Minimal Project"},
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Minimal Project"

    def test_create_project_empty_name(self, client: TestClient, auth_headers):
        """Test project creation with empty name."""
        response = client.post(
            "/api/v1/projects",
            headers=auth_headers,
            json={"name": ""},
        )
        assert response.status_code == 422


class TestGetProject:
    """Tests for getting a single project."""

    def test_get_project_success(self, client: TestClient, auth_headers, test_project):
        """Test getting a project by ID."""
        response = client.get(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_project.id)
        assert data["name"] == test_project.name

    def test_get_project_not_found(self, client: TestClient, auth_headers):
        """Test getting a nonexistent project."""
        from uuid import uuid4

        response = client.get(
            f"/api/v1/projects/{uuid4()}",
            headers=auth_headers,
        )
        assert response.status_code == 404


class TestUpdateProject:
    """Tests for updating projects."""

    def test_update_project_success(self, client: TestClient, auth_headers, test_project):
        """Test updating a project."""
        response = client.patch(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers,
            json={"name": "Updated Project Name"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Project Name"

    def test_update_project_not_found(self, client: TestClient, auth_headers):
        """Test updating a nonexistent project."""
        from uuid import uuid4

        response = client.patch(
            f"/api/v1/projects/{uuid4()}",
            headers=auth_headers,
            json={"name": "New Name"},
        )
        assert response.status_code == 404


class TestDeleteProject:
    """Tests for deleting projects."""

    def test_delete_project_success(self, client: TestClient, auth_headers, test_project):
        """Test deleting a project."""
        response = client.delete(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200

        # Verify deletion
        get_response = client.get(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers,
        )
        assert get_response.status_code == 404

    def test_delete_project_not_found(self, client: TestClient, auth_headers):
        """Test deleting a nonexistent project."""
        from uuid import uuid4

        response = client.delete(
            f"/api/v1/projects/{uuid4()}",
            headers=auth_headers,
        )
        assert response.status_code == 404
