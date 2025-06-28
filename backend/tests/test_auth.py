"""Authentication endpoint tests for VibeStack backend."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(async_client: AsyncClient):
    """Test user registration, login, and token refresh flow."""
    # Register a new user
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "pytestuser@vibestack.dev",
            "password": "Pytest1234!",
            "username": "pytestuser",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "pytestuser@vibestack.dev"

    # Login with the new user
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "pytestuser@vibestack.dev", "password": "Pytest1234!"},
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    # Refresh token
    response = await async_client.post(
        "/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert response.status_code == 200
    refreshed = response.json()
    assert "access_token" in refreshed
    assert "refresh_token" in refreshed
