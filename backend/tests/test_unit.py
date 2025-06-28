"""Unit tests for VibeStack backend services."""

import pytest
from passlib.context import CryptContext

from app.core.security import create_access_token, verify_password
from app.schemas.user import UserCreate


@pytest.mark.asyncio
@pytest.mark.unit
async def test_password_verification():
    """Test password hashing and verification."""
    password = "TestPassword123!"

    # Test password verification with incorrect hash
    assert verify_password(
        password, "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.i8i2"
    ) is False

    # Test with correct hash
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash(password)
    assert verify_password(password, hashed) is True


@pytest.mark.asyncio
@pytest.mark.unit
async def test_token_creation():
    """Test JWT token creation."""
    user_id = 1
    email = "test@example.com"

    token = create_access_token(data={"sub": email, "user_id": user_id})
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_user_schema_validation():
    """Test user schema validation."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
    }

    user = UserCreate(**user_data)
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"

    with pytest.raises(ValueError):
        UserCreate(
            email="invalid-email",
            password="TestPassword123!",
            username="testuser",
        )
