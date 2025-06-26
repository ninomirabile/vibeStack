# 🧱 VibeStack Backend

A modular, scalable FastAPI backend with JWT authentication, user management, and production-ready architecture.

## 🚀 Features
- **FastAPI** (async, Python 3.11+)
- **JWT Auth** (access/refresh, OAuth2 password flow)
- **User CRUD** (with RBAC/multi-tenant placeholders)
- **PostgreSQL** (prod), **SQLite** (dev/test)
- **Docker-ready** (compose for dev/prod)
- **Seed data** (admin/test user)
- **Logging** (structlog)
- **Tests** (pytest)
- **Linting** (ruff, black)

## 🗂️ Structure
```
backend/
  app/
    api/           # FastAPI routers (v1, endpoints)
    core/          # Config, DB, security, logging
    models/        # SQLAlchemy models
    schemas/       # Pydantic schemas
    services/      # Business logic
  scripts/         # DB init/seed scripts
  Dockerfile
  docker-compose.yml
  requirements.txt
  ...
```

## ⚡ Quickstart
### 1. Prerequisites
- Docker + Docker Compose
- Python 3.11+ (for local dev)

### 2. Setup & Run (Dev)
```bash
cd backend
cp env.example .env
# (edit .env as needed)
docker-compose up --build
```
- API: http://localhost:8000
- Adminer: http://localhost:8080

### 3. Seed Data
```bash
make seed
```
Creates admin (`admin@vibestack.dev` / `Admin1234!`) and test user.

### 4. Run Tests & Lint
```bash
make test
make lint
```

## 🛡️ Security
- Passwords hashed with bcrypt
- JWT tokens (configurable expiry)
- Secrets via `.env` (never commit real secrets)
- RBAC/multi-tenant: ready for extension

## 🧩 Extending
- Add new models/services in `app/models` and `app/services`
- Add endpoints in `app/api/v1/endpoints`
- Use dependency injection for business logic

## 📝 Notes
- For production, use `docker-compose.prod.yml` and set strong secrets.
- See main README for full-stack info.

---
_Designed for AI-assisted, clean, and scalable development._ 