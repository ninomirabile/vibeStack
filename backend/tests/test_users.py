"""User management endpoint tests for VibeStack backend."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_user_profile_and_update(async_client: AsyncClient):
    """Test user profile retrieval and update functionality."""
    # Register and login
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "profileuser@vibestack.dev",
            "password": "Profile1234!",
            "username": "profileuser",
        },
    )
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "profileuser@vibestack.dev", "password": "Profile1234!"},
    )
    tokens = login.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # Get profile
    resp = await async_client.get("/api/v1/users/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "profileuser@vibestack.dev"

    # Update profile
    resp = await async_client.patch(
        "/api/v1/users/me", json={"first_name": "Profile"}, headers=headers
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["first_name"] == "Profile"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_admin_list_and_delete(async_client: AsyncClient):
    """Test admin user listing and deletion functionality."""
    # Login as admin
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@vibestack.dev", "password": "Admin1234!"},
    )
    tokens = login.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # List users
    resp = await async_client.get("/api/v1/users/", headers=headers)
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)

    # Delete test user (if exists)
    for user in users:
        if user["email"] == "pytestuser@vibestack.dev":
            resp = await async_client.delete(
                f"/api/v1/users/{user['id']}", headers=headers
            )
            assert resp.status_code == 200
