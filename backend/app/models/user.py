"""User model for authentication and user management.

This module defines the User SQLAlchemy model with proper relationships,
validation, and methods for user management.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """User model for authentication and user management.

    This model represents users in the system with support for:
    - Basic authentication (email/password)
    - Role-based access control (RBAC) placeholder
    - Multi-tenant support placeholder
    - Audit fields (created_at, updated_at)
    """

    __tablename__ = "users"

    # Primary key
    user_id = Column(Integer, primary_key=True, index=True)

    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # User profile fields
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), unique=True, index=True, nullable=True)

    # Status and permissions
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Role-based access control (placeholder for future implementation)
    role = Column(String(50), default="user", nullable=False)

    # Multi-tenant support (placeholder for future implementation)
    tenant_id = Column(String(100), nullable=True, index=True)

    # Additional profile information
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)

    # Audit fields
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        """Return string representation of the User model."""
        return f"<User(user_id={self.user_id}, email='{self.email}', username='{self.username}')>"

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
        """Get the user's display name (username or email)."""
        return self.username or self.email

    def to_dict(self) -> dict:
        """Convert user to dictionary representation."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_superuser": self.is_superuser,
            "role": self.role,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat()
            if self.last_login_at
            else None,
        }

    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login_at = datetime.utcnow()

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission (placeholder for RBAC).

        Args:
        ----
            permission: Permission to check

        Returns:
        -------
            bool: True if user has permission, False otherwise
        """
        # TODO: Implement proper RBAC logic
        if self.is_superuser:
            return True

        # Placeholder logic - replace with actual RBAC implementation
        if permission == "read" and self.is_active:
            return True

        return False

    def is_tenant_member(self, tenant_id: str) -> bool:
        """Check if user is a member of a specific tenant (placeholder for multi-tenancy).

        Args:
        ----
            tenant_id: Tenant ID to check

        Returns:
        -------
            bool: True if user is member of tenant, False otherwise
        """
        # TODO: Implement proper multi-tenant logic
        if self.is_superuser:
            return True

        return self.tenant_id == tenant_id
