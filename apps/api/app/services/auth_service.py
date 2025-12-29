"""Authentication service for user management and token handling."""

from datetime import datetime, timezone
from typing import Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import RegisterRequest, UserUpdate
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
    verify_token,
)

settings = get_settings()


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.db.query(User).filter(User.email == email.lower()).first()

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, data: RegisterRequest) -> User:
        """Create a new user."""
        user = User(
            email=data.email.lower(),
            password_hash=hash_password(data.password),
            full_name=data.full_name,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def update_last_login(self, user: User) -> None:
        """Update user's last login timestamp."""
        user.last_login = datetime.now(timezone.utc)
        self.db.commit()

    def update_user(self, user: User, data: UserUpdate) -> User:
        """Update user profile."""
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.settings is not None:
            user.settings = data.settings
        self.db.commit()
        self.db.refresh(user)
        return user

    def create_tokens(self, user: User) -> Tuple[str, str]:
        """Create access and refresh tokens for user."""
        access_token = create_access_token(subject=str(user.id))
        refresh_token, expires_at = create_refresh_token(subject=str(user.id))

        # Store refresh token hash
        token_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )
        self.db.add(token_record)
        self.db.commit()

        return access_token, refresh_token

    def refresh_tokens(self, refresh_token: str) -> Optional[Tuple[str, str, User]]:
        """Refresh tokens using a valid refresh token."""
        # Verify token
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        # Find and validate stored token
        token_hash = hash_token(refresh_token)
        stored_token = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )

        if not stored_token:
            return None

        # Get user
        user = self.get_user_by_id(UUID(user_id))
        if not user or not user.is_active:
            return None

        # Revoke old token (rotation)
        stored_token.revoked = True
        stored_token.revoked_at = datetime.now(timezone.utc)

        # Create new tokens
        access_token, new_refresh_token = self.create_tokens(user)

        return access_token, new_refresh_token, user

    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """Revoke a refresh token."""
        token_hash = hash_token(refresh_token)
        stored_token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.token_hash == token_hash)
            .first()
        )

        if stored_token:
            stored_token.revoked = True
            stored_token.revoked_at = datetime.now(timezone.utc)
            self.db.commit()
            return True
        return False

    def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """Revoke all refresh tokens for a user."""
        result = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
            )
            .update(
                {
                    RefreshToken.revoked: True,
                    RefreshToken.revoked_at: datetime.now(timezone.utc),
                }
            )
        )
        self.db.commit()
        return result

    def change_password(self, user: User, new_password: str) -> None:
        """Change user password and revoke all tokens."""
        user.password_hash = hash_password(new_password)
        self.db.commit()
        # Revoke all refresh tokens on password change
        self.revoke_all_user_tokens(user.id)

    def cleanup_expired_tokens(self) -> int:
        """Delete expired refresh tokens."""
        result = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.expires_at < datetime.now(timezone.utc))
            .delete()
        )
        self.db.commit()
        return result
