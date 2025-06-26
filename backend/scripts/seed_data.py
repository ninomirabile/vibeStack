"""
Seed data script for VibeStack backend.

Creates an initial admin and test user if they do not exist.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate
import os

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@vibestack.dev")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin1234!")
TEST_EMAIL = os.getenv("TEST_EMAIL", "test@vibestack.dev")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "Test1234!")

async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        # Create admin user
        try:
            await user_service.create_user(UserCreate(
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD,
                username="admin",
                first_name="Admin",
                last_name="User"
            ))
            print(f"Admin user created: {ADMIN_EMAIL}")
        except Exception as e:
            print(f"Admin user: {e}")
        # Create test user
        try:
            await user_service.create_user(UserCreate(
                email=TEST_EMAIL,
                password=TEST_PASSWORD,
                username="testuser",
                first_name="Test",
                last_name="User"
            ))
            print(f"Test user created: {TEST_EMAIL}")
        except Exception as e:
            print(f"Test user: {e}")

if __name__ == "__main__":
    asyncio.run(seed()) 