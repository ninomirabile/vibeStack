"""Pydantic schemas for authentication operations.

This module defines Pydantic models for login, token management,
and authentication-related requests and responses.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

    class Config:
        """Pydantic config for Token schema."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        }


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None
    is_superuser: bool = False
    role: str = "user"


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr
    password: str

    class Config:
        """Pydantic config for LoginRequest schema."""

        json_schema_extra = {
            "example": {"email": "user@example.com", "password": "SecurePassword123!"}
        }


class RefreshRequest(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str

    class Config:
        """Pydantic config for RefreshRequest schema."""

        json_schema_extra = {
            "example": {"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
        }


class PasswordChangeRequest(BaseModel):
    """Schema for password change request."""

    current_password: str
    new_password: str

    class Config:
        """Pydantic config for PasswordChangeRequest schema."""

        json_schema_extra = {
            "example": {
                "current_password": "OldPassword123!",
                "new_password": "NewSecurePassword456!",
            }
        }


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""

    email: EmailStr

    class Config:
        """Pydantic config for PasswordResetRequest schema."""

        json_schema_extra = {"example": {"email": "user@example.com"}}


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""

    token: str
    new_password: str

    class Config:
        """Pydantic config for PasswordResetConfirm schema."""

        json_schema_extra = {
            "example": {
                "token": "reset-token-here",
                "new_password": "NewSecurePassword456!",
            }
        }
