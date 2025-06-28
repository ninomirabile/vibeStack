"""Custom pytest configuration for integration tests."""

import pytest
import os
from typing import List


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests with real database"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if config.getoption("--integration"):
        # When --integration is used, run all tests with integration marker
        # and configure for real database
        os.environ["INTEGRATION_TEST"] = "true"
        os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db")
        
        # Mark all tests as integration tests if not already marked
        for item in items:
            if "integration" not in item.keywords:
                item.add_marker(pytest.mark.integration)
    else:
        # Skip integration tests when --integration is not used
        skip_integration = pytest.mark.skip(reason="Integration tests require --integration flag")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


def pytest_configure(config):
    """Configure pytest for integration tests."""
    if config.getoption("--integration"):
        print("\n🔧 Running integration tests with real database...")
        print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'Not set')}")
        print(f"🔑 Secret Key: {os.getenv('SECRET_KEY', 'Not set')}")
        print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'Not set')}\n") 