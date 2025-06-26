"""
User service for business logic and database operations.

This module contains the UserService class that handles all user-related
business logic, database operations, and validation.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import structlog

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash, verify_password

logger = structlog.get_logger(__name__)


class UserService:
    """Service class for user-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            User: Created user instance
            
        Raises:
            ValueError: If email or username already exists
        """
        # Check if email already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Check if username already exists (if provided)
        if user_data.username:
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user:
                raise ValueError("Username already taken")
        
        # Create user instance
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            bio=user_data.bio,
            avatar_url=user_data.avatar_url,
            hashed_password=hashed_password,
        )
        
        # Save to database
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info("User created successfully", user_id=user.id, email=user.email)
        return user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Optional[User]: User instance or None if not found
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User instance or None if not found
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            Optional[User]: User instance or None if not found
        """
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[User]:
        """
        Get list of users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: If True, only return active users
            
        Returns:
            List[User]: List of user instances
        """
        query = select(User)
        
        if active_only:
            query = query.where(User.is_active == True)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        
        return result.scalars().all()
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id: User ID to update
            user_data: User update data
            
        Returns:
            Optional[User]: Updated user instance or None if not found
        """
        # Get existing user
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Check for email conflicts
        if user_data.email and user_data.email != user.email:
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("Email already registered")
        
        # Check for username conflicts
        if user_data.username and user_data.username != user.username:
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user:
                raise ValueError("Username already taken")
        
        # Update user fields
        update_data = user_data.dict(exclude_unset=True)
        
        if update_data:
            await self.db.execute(
                update(User)
                .where(User.id == user_id)
                .values(**update_data)
            )
            await self.db.commit()
            
            # Refresh user instance
            await self.db.refresh(user)
            
            logger.info("User updated successfully", user_id=user_id)
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user (soft delete by setting is_active to False).
        
        Args:
            user_id: User ID to delete
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Soft delete by setting is_active to False
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )
        await self.db.commit()
        
        logger.info("User deleted successfully", user_id=user_id)
        return True
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Optional[User]: Authenticated user or None if invalid credentials
        """
        user = await self.get_user_by_email(email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        # Update last login
        user.update_last_login()
        await self.db.commit()
        
        logger.info("User authenticated successfully", user_id=user.id, email=user.email)
        return user
    
    async def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password was changed, False if invalid current password
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            return False
        
        # Hash and update new password
        hashed_password = get_password_hash(new_password)
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(hashed_password=hashed_password)
        )
        await self.db.commit()
        
        logger.info("Password changed successfully", user_id=user_id)
        return True
    
    async def verify_user(self, user_id: int) -> bool:
        """
        Mark user as verified.
        
        Args:
            user_id: User ID to verify
            
        Returns:
            bool: True if user was verified, False if not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_verified=True)
        )
        await self.db.commit()
        
        logger.info("User verified successfully", user_id=user_id)
        return True
    
    def to_response(self, user: User) -> UserResponse:
        """
        Convert User model to UserResponse schema.
        
        Args:
            user: User model instance
            
        Returns:
            UserResponse: User response schema
        """
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
        ) 