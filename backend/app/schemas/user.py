"""
Pydantic schemas for user-related operations.

This module defines Pydantic models for user creation, updates,
and responses with proper validation and serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    email: EmailStr
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if v is not None:
            if len(v) < 3:
                raise ValueError('Username must be at least 3 characters long')
            if len(v) > 50:
                raise ValueError('Username must be at most 50 characters long')
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v
    
    @validator('first_name', 'last_name')
    def validate_name(cls, v):
        """Validate name fields."""
        if v is not None and len(v) > 100:
            raise ValueError('Name must be at most 100 characters long')
        return v
    
    @validator('bio')
    def validate_bio(cls, v):
        """Validate bio field."""
        if v is not None and len(v) > 1000:
            raise ValueError('Bio must be at most 1000 characters long')
        return v


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if v is not None:
            if len(v) < 3:
                raise ValueError('Username must be at least 3 characters long')
            if len(v) > 50:
                raise ValueError('Username must be at most 50 characters long')
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v
    
    @validator('first_name', 'last_name')
    def validate_name(cls, v):
        """Validate name fields."""
        if v is not None and len(v) > 100:
            raise ValueError('Name must be at most 100 characters long')
        return v
    
    @validator('bio')
    def validate_bio(cls, v):
        """Validate bio field."""
        if v is not None and len(v) > 1000:
            raise ValueError('Bio must be at most 1000 characters long')
        return v


class UserInDB(UserBase):
    """Schema for user data in database (includes internal fields)."""
    
    id: int
    hashed_password: str
    is_active: bool
    is_verified: bool
    is_superuser: bool
    role: str
    tenant_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    """Schema for user response (excludes sensitive fields)."""
    
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    role: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.username:
            return self.username
        else:
            return self.email
    
    @property
    def display_name(self) -> str:
        """Get the user's display name."""
        return self.username or self.email
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "display_name": "johndoe",
                "bio": "Software developer passionate about clean code",
                "avatar_url": "https://example.com/avatar.jpg",
                "is_active": True,
                "is_verified": True,
                "is_superuser": False,
                "role": "user",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "last_login_at": "2023-01-01T12:00:00Z"
            }
        } 