"""
Authentication endpoints for the VibeStack API.

Includes login, token refresh, and registration endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token, summary="Login and get JWT tokens")
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    token = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return token

@router.post("/refresh", response_model=Token, summary="Refresh JWT tokens")
async def refresh_token(
    refresh_data: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    token = await auth_service.refresh_tokens(refresh_data.refresh_token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    return token

# Minimal registration endpoint (optional, can be expanded)
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

@router.post("/register", response_model=UserResponse, summary="Register a new user")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    try:
        user = await user_service.create_user(user_data)
        return user_service.to_response(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 