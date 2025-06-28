"""Test configuration and fixtures for VibeStack backend tests."""

import asyncio
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.schemas.user import UserCreate
from app.services.user_service import UserService

# Set testing environment
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

# Create test database engine
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
)

# Create test session factory
TestingSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_database():
    """Set up test database with tables and create admin user."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Create admin user
    async with TestingSessionLocal() as session:
        user_service = UserService(session)
        try:
            await user_service.create_user(
                UserCreate(
                    email="admin@vibestack.dev",
                    password="Admin1234!",
                    username="admin",
                    first_name="Admin",
                    last_name="User",
                    is_superuser=True,
                )
            )
        except Exception:
            pass
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def async_client(db_session):
    """Provide an async HTTP client for testing."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
