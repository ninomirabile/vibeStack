"""Authentication service for JWT token management.

This module contains the AuthService class that handles authentication,
JWT token creation and validation, and user session management.
"""

from typing import Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    is_token_expired,
    verify_token,
)
from app.schemas.auth import Token, TokenData
from app.services.user_service import UserService

logger = structlog.get_logger(__name__)


class AuthService:
    """Service class for authentication-related operations."""

    def __init__(self, db: AsyncSession):
        """Initialize AuthService with a database session."""
        self.db = db
        self.user_service = UserService(db)

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        """Authenticate user and return JWT tokens.

        Args:
        ----
            email: User email
            password: Plain text password

        Returns:
        -------
            Optional[Token]: JWT tokens if authentication successful, None otherwise
        """
        user = await self.user_service.authenticate_user(email, password)
        if not user:
            return None

        # Create tokens
        token_data = {
            "sub": str(user.user_id),
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "role": user.role,
        }

        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        logger.info(
            "User authenticated and tokens created",
            user_id=user.user_id,
            email=user.email,
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=60 * 60,  # 1 hour in seconds
        )

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        """Refresh access token using refresh token.

        Args:
        ----
            refresh_token: Valid refresh token

        Returns:
        -------
            Optional[Token]: New JWT tokens if refresh successful, None otherwise
        """
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            logger.warning("Invalid refresh token provided")
            return None

        # Check if token is expired
        if is_token_expired(refresh_token):
            logger.warning("Refresh token is expired")
            return None

        # Get user from database
        user_id = int(payload.get("sub"))
        user = await self.user_service.get_user_by_id(user_id)

        if not user or not user.is_active:
            logger.warning("User not found or inactive", user_id=user_id)
            return None

        # Create new tokens
        token_data = {
            "sub": str(user.user_id),
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "role": user.role,
        }

        access_token = create_access_token(data=token_data)
        new_refresh_token = create_refresh_token(data=token_data)

        logger.info(
            "Tokens refreshed successfully", user_id=user.user_id, email=user.email
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=60 * 60,  # 1 hour in seconds
        )

    async def get_current_user(self, token: str) -> Optional[TokenData]:
        """Get current user from access token.

        Args:
        ----
            token: JWT access token

        Returns:
        -------
            Optional[TokenData]: User data from token or None if invalid
        """
        # Verify access token
        payload = verify_token(token, token_type="access")
        if not payload:
            logger.warning("Invalid access token provided")
            return None

        # Check if token is expired
        if is_token_expired(token):
            logger.warning("Access token is expired")
            return None

        # Get user from database to ensure they still exist and are active
        user_id = int(payload.get("sub"))
        user = await self.user_service.get_user_by_id(user_id)

        if not user or not user.is_active:
            logger.warning("User not found or inactive", user_id=user_id)
            return None

        return TokenData(
            user_id=user.user_id,
            email=user.email,
            username=user.username,
            is_superuser=user.is_superuser,
            role=user.role,
        )

    async def revoke_token(self, token: str) -> bool:
        """Revoke a token (placeholder for token blacklisting).

        Args:
        ----
            token: Token to revoke

        Returns:
        -------
            bool: True if token was revoked (placeholder implementation)
        """
        # TODO: Implement token blacklisting with Redis or database
        # For now, this is a placeholder that always returns True
        logger.info("Token revocation requested (placeholder implementation)")
        return True

    async def validate_token(self, token: str) -> bool:
        """Validate if a token is still valid.

        Args:
        ----
            token: JWT token to validate

        Returns:
        -------
            bool: True if token is valid, False otherwise
        """
        # Verify token
        payload = verify_token(token)
        if not payload:
            return False

        # Check if token is expired
        if is_token_expired(token):
            return False

        # Get user from database to ensure they still exist and are active
        user_id = int(payload.get("sub"))
        user = await self.user_service.get_user_by_id(user_id)

        if not user or not user.is_active:
            return False

        return True

    def create_tokens_for_user(
        self,
        user_id: int,
        email: str,
        username: str = None,
        is_superuser: bool = False,
        role: str = "user",
    ) -> Token:
        """Create tokens for a specific user (used for testing or admin operations).

        Args:
        ----
            user_id: User ID
            email: User email
            username: User username (optional)
            is_superuser: Whether user is superuser
            role: User role

        Returns:
        -------
            Token: JWT tokens
        """
        token_data = {
            "sub": str(user_id),
            "email": email,
            "username": username,
            "is_superuser": is_superuser,
            "role": role,
        }

        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=60 * 60,  # 1 hour in seconds
        )
