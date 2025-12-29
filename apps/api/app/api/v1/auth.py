"""Authentication API endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.deps import CurrentUser, DbSession
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    UserUpdate,
)
from app.services.auth_service import AuthService

router = APIRouter()
security = HTTPBearer(auto_error=False)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: DbSession):
    """Register a new user."""
    auth_service = AuthService(db)

    # Check if email already exists
    existing_user = auth_service.get_user_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "VALIDATION_ERROR",
                "message": "Email already registered",
                "details": {"email": "This email is already in use"},
            },
        )

    # Create user
    user = auth_service.create_user(data)

    # Create tokens
    access_token, refresh_token = auth_service.create_tokens(user)

    return TokenResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, response: Response, db: DbSession):
    """Login with email and password."""
    auth_service = AuthService(db)

    # Authenticate user
    user = auth_service.authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid email or password",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "FORBIDDEN",
                "message": "User account is deactivated",
            },
        )

    # Update last login
    auth_service.update_last_login(user)

    # Create tokens
    access_token, refresh_token = auth_service.create_tokens(user)

    # Set refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,  # 7 days
    )

    return TokenResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    db: DbSession,
    data: Optional[RefreshTokenRequest] = None,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(db)

    # Get refresh token from body or header
    token = None
    if data and data.refresh_token:
        token = data.refresh_token
    elif credentials:
        token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Refresh token is required",
            },
        )

    # Refresh tokens
    result = auth_service.refresh_tokens(token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid or expired refresh token",
            },
        )

    access_token, new_refresh_token, user = result

    # Set new refresh token as HTTP-only cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )

    return TokenResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    response: Response,
    current_user: CurrentUser,
    db: DbSession,
    data: Optional[RefreshTokenRequest] = None,
):
    """Logout and revoke refresh token."""
    auth_service = AuthService(db)

    # Revoke refresh token if provided
    if data and data.refresh_token:
        auth_service.revoke_refresh_token(data.refresh_token)

    # Clear cookie
    response.delete_cookie(key="refresh_token")

    return MessageResponse(message="Logged out successfully")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(data: ForgotPasswordRequest, db: DbSession):
    """Request password reset email."""
    # Always return success to prevent email enumeration
    # In production, send reset email if user exists
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(data.email)

    if user:
        # TODO: Generate reset token and send email
        pass

    return MessageResponse(
        message="If an account exists with this email, a password reset link has been sent"
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(data: ResetPasswordRequest, db: DbSession):
    """Reset password using reset token."""
    # TODO: Implement token verification and password reset
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail={
            "code": "NOT_IMPLEMENTED",
            "message": "Password reset is not yet implemented",
        },
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """Get current authenticated user information."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    """Update current user profile."""
    auth_service = AuthService(db)
    updated_user = auth_service.update_user(current_user, data)
    return UserResponse.model_validate(updated_user)
