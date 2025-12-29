"""Pytest configuration and fixtures."""

import os
from typing import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import Settings, get_settings
from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.utils.security import create_access_token, hash_password


def get_test_settings() -> Settings:
    """Get test settings."""
    return Settings(
        database_url="sqlite:///:memory:",
        secret_key="test-secret-key",
        jwt_secret_key="test-jwt-secret",
        upload_dir="./test_uploads",
        ai_features_enabled=False,
        whisper_api_enabled=False,
    )


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Test settings fixture."""
    return get_test_settings()


@pytest.fixture(scope="function")
def db_engine():
    """Create test database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session: Session, test_settings: Settings) -> Generator[TestClient, None, None]:
    """Create test client with database override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    def override_get_settings():
        return test_settings

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_get_settings

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash=hash_password("TestPassword123"),
        full_name="Test User",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Create authentication headers for test user."""
    access_token = create_access_token(subject=str(test_user.id))
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_project(db_session: Session, test_user: User):
    """Create a test project."""
    from app.models.project import Project, ProjectStatus

    project = Project(
        id=uuid4(),
        user_id=test_user.id,
        name="Test Project",
        description="A test project",
        status=ProjectStatus.CREATED,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project
