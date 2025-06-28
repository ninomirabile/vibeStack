# VibeStack Fullstack Project Makefile

.PHONY: help install start stop test lint clean seed docs

# Default target
help:
	@echo "VibeStack Fullstack Project"
	@echo "=========================="
	@echo ""
	@echo "Available commands:"
	@echo "  install     - Install all dependencies (backend + frontend)"
	@echo "  start       - Start the full application (backend + frontend)"
	@echo "  stop        - Stop all services"
	@echo "  test        - Run all tests"
	@echo "  lint        - Run linting for all code"
	@echo "  clean       - Clean all build artifacts"
	@echo "  seed        - Seed the database with initial data"
	@echo "  docs        - Generate documentation"
	@echo ""
	@echo "Backend commands:"
	@echo "  backend-install  - Install Python dependencies"
	@echo "  backend-start    - Start backend services"
	@echo "  backend-test     - Run backend tests"
	@echo "  backend-lint     - Run backend linting"
	@echo "  backend-seed     - Seed backend database"
	@echo ""
	@echo "Frontend commands:"
	@echo "  frontend-install - Install Flutter dependencies"
	@echo "  frontend-setup-android - Set up Android build environment (requires Java 17)"
	@echo "  frontend-start   - Start Flutter development server"
	@echo "  frontend-test    - Run Flutter tests"
	@echo "  frontend-lint    - Run Flutter linting"
	@echo "  frontend-build   - Build Flutter for all platforms"
	@echo "  frontend-build-web - Build Flutter for web"
	@echo "  frontend-build-android - Build Flutter for Android (requires Java 17)"

# Install all dependencies
install: backend-install frontend-install

# Start the full application
start: backend-start
	@echo "Backend started. Starting frontend..."
	@echo "Frontend will be available at: http://localhost:3000"
	@echo "Backend API will be available at: http://localhost:8000"
	@echo "Adminer will be available at: http://localhost:8080"

# Stop all services
stop:
	@echo "Stopping all services..."
	cd backend && docker-compose down
	@echo "All services stopped."

# Run all tests
test: backend-test frontend-test

# Run all linting
lint: backend-lint frontend-lint

# Clean all build artifacts
clean: backend-clean frontend-clean

# Seed database
seed: backend-seed

# Generate documentation
docs:
	@echo "Generating documentation..."
	@echo "Backend API docs: http://localhost:8000/docs"
	@echo "Frontend docs: See frontend/README.md"

# Backend commands
backend-install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

backend-start:
	@echo "Starting backend services..."
	cd backend && docker-compose up -d --build
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Backend services started!"

backend-test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v

backend-lint:
	@echo "Running backend linting..."
	cd backend && ruff check . && black --check .

backend-seed:
	@echo "Seeding backend database..."
	cd backend && python scripts/seed_data.py

backend-clean:
	@echo "Cleaning backend artifacts..."
	cd backend && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -name "*.pyc" -delete 2>/dev/null || true
	cd backend && rm -rf .pytest_cache/ 2>/dev/null || true
	cd backend && rm -rf coverage.xml 2>/dev/null || true

# Frontend commands
frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && flutter pub get

frontend-setup-android:
	@echo "Setting up Android build environment..."
	cd frontend && ./scripts/setup-android.sh

frontend-start:
	@echo "Starting Flutter development server..."
	cd frontend && flutter run -d chrome --web-port 3000

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && flutter test

frontend-lint:
	@echo "Running frontend linting..."
	cd frontend && flutter analyze

frontend-build:
	@echo "Building Flutter for all platforms..."
	cd frontend && flutter build web
	cd frontend && flutter build apk --release
	@echo "Builds completed!"

frontend-build-web:
	@echo "Building Flutter for web..."
	cd frontend && flutter build web
	@echo "Web build completed!"

frontend-build-android:
	@echo "Building Flutter for Android..."
	cd frontend && flutter build apk --release
	@echo "Android build completed!"

# Development helpers
dev-backend:
	@echo "Starting backend in development mode..."
	cd backend && docker-compose up --build

dev-frontend:
	@echo "Starting frontend in development mode..."
	cd frontend && flutter run -d chrome --web-port 3000 --hot

# Database commands
db-reset:
	@echo "Resetting database..."
	cd backend && docker-compose down -v
	cd backend && docker-compose up -d db
	@sleep 5
	cd backend && python scripts/seed_data.py

# Docker commands
docker-build:
	@echo "Building all Docker images..."
	cd backend && docker-compose build

docker-clean:
	@echo "Cleaning Docker resources..."
	docker system prune -f
	docker volume prune -f

# CI/CD helpers
ci-backend:
	@echo "Running backend CI checks..."
	cd backend && pip install -r requirements.txt
	cd backend && ruff check . && black --check .
	cd backend && python -m pytest tests/ -v

ci-frontend:
	@echo "Running frontend CI checks..."
	cd frontend && flutter pub get
	cd frontend && flutter analyze
	cd frontend && flutter test
	cd frontend && ./scripts/setup-android.sh

# Production helpers
prod-build:
	@echo "Building for production..."
	cd backend && docker-compose -f docker-compose.prod.yml build
	cd frontend && flutter build web --release

prod-deploy:
	@echo "Deploying to production..."
	@echo "This is a placeholder for production deployment"
	@echo "Configure your deployment strategy in CI/CD"

# Health checks
health-check:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/health || echo "Backend not responding"
	@curl -f http://localhost:8080 || echo "Adminer not responding"

# Logs
logs:
	@echo "Showing all service logs..."
	cd backend && docker-compose logs -f

logs-backend:
	@echo "Showing backend logs..."
	cd backend && docker-compose logs -f api

logs-db:
	@echo "Showing database logs..."
	cd backend && docker-compose logs -f db 