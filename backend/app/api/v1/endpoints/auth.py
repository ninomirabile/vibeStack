"""Authentication endpoints for the VibeStack API.

Includes login, token refresh, and registration endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/login", response_model=Token, summary="Login and get JWT tokens")
async def login(
    login_data: LoginRequest, db: AsyncSession = Depends(get_db)
):  # noqa: B008
    """Authenticate user and return JWT tokens."""
    auth_service = AuthService(db)
    token = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return token


@router.post("/refresh", response_model=Token, summary="Refresh JWT tokens")
async def refresh_token(
    refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db)
):  # noqa: B008
    """Refresh JWT tokens using a valid refresh token."""
    auth_service = AuthService(db)
    token = await auth_service.refresh_tokens(refresh_data.refresh_token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    return token


@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
):  # noqa: B008
    """Register a new user account."""
    user_service = UserService(db)
    try:
        user = await user_service.create_user(user_data)
        return user_service.to_response(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
