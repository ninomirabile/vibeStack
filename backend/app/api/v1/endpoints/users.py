"""User endpoints for the VibeStack API.

Includes CRUD operations, profile, and RBAC/multi-tenant placeholders.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()

# OAuth2 scheme for extracting JWT from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):  # noqa: B008
    """Dependency to get the current user from JWT token."""
    auth_service = AuthService(db)
    user_data = await auth_service.get_current_user(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return user_data


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def read_current_user(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):  # noqa: B008
    """Get the profile of the current authenticated user."""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.to_response(user)


@router.get("/", response_model=List[UserResponse], summary="List users (admin only)")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):  # noqa: B008
    """List all users (admin only)."""
    # RBAC placeholder: only allow superuser or admin
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_service = UserService(db)
    users = await user_service.get_users(skip=skip, limit=limit, active_only=False)
    return [user_service.to_response(u) for u in users]


@router.get(
    "/{user_id}", response_model=UserResponse, summary="Get user by ID (admin only)"
)
async def get_user(
    user_id: int = Path(..., ge=1),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):  # noqa: B008
    """Get a user by ID (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.to_response(user)


@router.patch("/me", response_model=UserResponse, summary="Update current user profile")
async def update_current_user(
    user_update: UserUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):  # noqa: B008
    """Update the profile of the current authenticated user."""
    user_service = UserService(db)
    user = await user_service.update_user(current_user.user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.to_response(user)


@router.delete("/{user_id}", summary="Delete user (admin only)")
async def delete_user(
    user_id: int = Path(..., ge=1),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):  # noqa: B008
    """Delete a user by ID (admin only)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_service = UserService(db)
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


# Placeholder for multi-tenant and RBAC endpoints
# TODO: Implement /users/{tenant_id}/... and role management
