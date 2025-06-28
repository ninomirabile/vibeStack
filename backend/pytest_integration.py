"""Custom pytest configuration for integration tests."""

import logging
import os

import pytest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests with real database",
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if config.getoption("--integration"):
        os.environ["INTEGRATION_TEST"] = "true"
        os.environ["DATABASE_URL"] = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
        )

        for item in items:
            if "integration" not in item.keywords:
                item.add_marker(pytest.mark.integration)
    else:
        skip_integration = pytest.mark.skip(
            reason="Integration tests require --integration flag"
        )
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


def pytest_configure(config):
    """Configure pytest for integration tests."""
    if config.getoption("--integration"):
        logger.info("🔧 Running integration tests with real database...")
        logger.info("📊 Database URL: %s", os.getenv("DATABASE_URL", "Not set"))
        logger.info("🔑 Secret Key: %s", os.getenv("SECRET_KEY", "Not set"))
        logger.info("🌍 Environment: %s", os.getenv("ENVIRONMENT", "Not set"))
