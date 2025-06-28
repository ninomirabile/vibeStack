"""Seed data script for VibeStack backend.

Creates an initial admin and test user if they do not exist.
"""

import asyncio
import os

import structlog

from app.core.database import AsyncSessionLocal, init_db
from app.schemas.user import UserCreate
from app.services.user_service import UserService

logger = structlog.get_logger(__name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@vibestack.dev")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin1234!")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@vibestack.dev")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "Test1234!")


async def seed():
    """Seed the database with initial admin and test users if they do not exist."""
    await init_db()
    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        # Create admin user
        try:
            await user_service.create_user(
                UserCreate(
                    email=ADMIN_EMAIL,
                    password=ADMIN_PASSWORD,
                    username="admin",
                    first_name="Admin",
                    last_name="User",
                )
            )
            logger.info("Admin user created", email=ADMIN_EMAIL)
        except Exception as e:
            logger.info("Admin user exists or error", error=str(e))
        # Create test user
        try:
            await user_service.create_user(
                UserCreate(
                    email=TEST_EMAIL,
                    password=TEST_PASSWORD,
                    username="testuser",
                    first_name="Test",
                    last_name="User",
                )
            )
            logger.info("Test user created", email=TEST_EMAIL)
        except Exception as e:
            logger.info("Test user exists or error", error=str(e))


if __name__ == "__main__":
    asyncio.run(seed())
