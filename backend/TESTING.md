# Testing Guide

## Overview

The VibeStack backend uses pytest for testing with support for both unit tests and integration tests.

## Test Types

### Unit Tests
- **Purpose**: Test individual functions and components in isolation
- **Database**: SQLite in-memory database
- **Speed**: Fast execution
- **Dependencies**: Minimal external dependencies

### Integration Tests
- **Purpose**: Test complete workflows and API endpoints
- **Database**: PostgreSQL (real database)
- **Speed**: Slower execution
- **Dependencies**: Full application stack

## Running Tests

### All Tests
```bash
make backend-test
# or
cd backend && python -m pytest tests/ -v
```

### Unit Tests Only
```bash
make backend-test-unit
# or
cd backend && python -m pytest tests/ -v -m "unit"
```

### Integration Tests Only
```bash
make backend-test-integration
# or
cd backend && python -m pytest tests/ -v --integration -p pytest_integration
```

### Specific Test File
```bash
cd backend && python -m pytest tests/test_auth.py -v
```

## Test Configuration

### Environment Variables
- `TESTING=true`: Enables test mode
- `INTEGRATION_TEST=true`: Enables integration test mode
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key for tests

### Database Setup
- **Unit Tests**: SQLite in-memory database (automatic cleanup)
- **Integration Tests**: PostgreSQL database (manual cleanup required)

### Test Fixtures
- `event_loop`: Async event loop for tests
- `setup_database`: Database setup and teardown
- `db_session`: Database session
- `async_client`: HTTP client for API testing

## Writing Tests

### Unit Test Example
```python
@pytest.mark.asyncio
@pytest.mark.unit
async def test_password_verification():
    """Test password hashing and verification."""
    password = "TestPassword123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True
```

### Integration Test Example
```python
@pytest.mark.asyncio
@pytest.mark.integration
async def test_user_registration(async_client: AsyncClient):
    """Test complete user registration flow."""
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "username": "testuser",
        },
    )
    assert response.status_code == 200
```

## Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow running tests
- `@pytest.mark.asyncio`: Async tests

## CI/CD Integration

The GitHub Actions workflow automatically:
1. Runs unit tests in the lint job
2. Runs integration tests with PostgreSQL in the integration job
3. Uses the `--integration` flag for integration tests

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running for integration tests
- Check `DATABASE_URL` environment variable
- Verify database credentials

### Test Failures
- Run `make backend-test-unit` for quick feedback
- Check test logs for detailed error messages
- Ensure all dependencies are installed

### Performance Issues
- Unit tests should run quickly (< 30 seconds)
- Integration tests may take longer due to database setup
- Use `-x` flag to stop on first failure: `pytest -x` 