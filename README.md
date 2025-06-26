# 🧱 VibeStack Starter – A Modular Fullstack Seed Project

> ⚙️ A ready-to-code starter based on a modular, scalable, and secure architecture — designed for vibecoding productivity with AI tools like Cursor or GitHub Copilot. This project should be generated as a complete, functional fullstack application with minimal business logic, ready for rapid prototyping or production-grade development.

## 🎯 Output Expected

The output should be a fully structured monorepo with clear separation between `backend/` and `frontend/` folders. It must include:
- Docker-ready setup
- Properly typed code (Dart and Python)
- Basic CI/CD
- Tests
- Example seed data
- `.env` config templates
- Local development instructions
- Folder-specific `README.md` files (for both frontend and backend)

## 🚀 Purpose

Create a complete, modular fullstack seed project with a Flutter frontend (Web, Mobile, Desktop) and a FastAPI backend. The project should:
- Be **enterprise-ready** with clean architecture and typed code.
- Include **minimal but functional** implementations of authentication, user management, and healthcheck endpoints.
- Be **AI-tool-friendly** (optimized for Cursor) with clear module boundaries and readable, annotated code.
- Minimize API calls by including all necessary implementation details in this single prompt.
- Support **Dockerized environments** and include **basic CI/CD** setup via GitHub Actions.
- Include tests, encryption-ready setup, and secure token handling.

## 🧱 Stack Overview

### 🖥 Frontend

- **Framework**: Flutter (single codebase for Web, Mobile, Desktop)
- **State Management**: BLoC pattern (using `flutter_bloc`)
- **UI**: Minimal, clean UI with customizable Material 3 theming
- **Features**:
  - Login screen (email/password) with JWT authentication
  - User profile screen (basic display of user data)
  - Navigation with sidebar (desktop) and bottom navigation bar (mobile)
  - Mock API mode toggle (for development without backend)
- **i18n**: Preconfigured for English with i18n scaffolding for additional languages
- **API Integration**: HTTP client using `dio`
- **Tests**: `flutter_test` with widget tests for login and profile views
- **Linting/Formatting**: `dart format`, `flutter analyze`
- **Documentation**: Include a `frontend/README.md` with setup, structure, and mock mode info

### 🔧 Backend

- **Framework**: FastAPI (Python 3.11+)
- **Structure**: Modular architecture with routers, services, and async models
- **Auth**: JWT-based authentication using OAuth2 password flow
- **ORM**: SQLAlchemy (async) with Pydantic models
- **Database**: PostgreSQL for production; SQLite for development
- **Security**:
  - JWT with customizable expiry
  - Encrypted secrets using `.env`
  - SQLCipher-ready (optional instructions in `README.md`)
- **Endpoints**:
  - `/health` – Healthcheck
  - `/auth/login` – JWT generation
  - `/auth/refresh` – Token refresh
  - `/users` – User CRUD (create, read, update, delete)
  - `/users/me` – Authenticated user profile
- **Seed Data**: Include initial admin and test user creation logic
- **Logging**: Basic logging setup using Python’s `logging` module
- **Tests**: `pytest` with unit tests for auth and users
- **Linting/Formatting**: `ruff` and `black`
- **Documentation**: Include a `backend/README.md` with architecture and setup info

### 📦 DevOps & Tooling

- **Docker Compose**:
  - Services: FastAPI backend, PostgreSQL DB, Adminer (DB GUI)
  - Volume mapping for local development
- **Environment**:
  - `.env.example` templates
  - Secrets and config loaded via environment variables
- **CI/CD**:
  - GitHub Actions workflows:
    - Lint
    - Test
    - Build (Docker)
- **Automation**:
  - Basic `Makefile` or shell scripts (`start.sh`, `test.sh`, `seed.sh`) for common tasks

## 🔐 Security & Scalability

- **Authentication**:
  - JWT tokens with configurable lifetimes (1h access / 7d refresh)
  - Secure password storage (hashing with `bcrypt`)
- **Secrets Management**:
  - `.env` files + support for Docker secrets (optional)
- **Separation of Concerns**:
  - Keep business logic in services, API logic in routers
  - Minimal coupling between infrastructure and logic
- **Scalability**:
  - Placeholder hooks for multi-tenant support
  - Placeholder comments for RBAC implementation (role-based access control)

## 🧰 Included Modules

- ✅ **Auth**: Login, refresh, registration
- ✅ **Users**: CRUD with RBAC placeholder
- ✅ **Healthcheck**: Basic liveness endpoint
- 🟡 **Multi-Tenant**: Hookable structure, but not implemented
- 🟡 **RBAC**: Scaffolded, but no roles logic enforced

## 🏁 Getting Started

### Requirements
- Docker + Docker Compose
- Python 3.11+
- Flutter SDK 3.22.2+
- Node.js (for CI/CD pipelines, optional)

### Launch Backend
```bash
cd backend
cp .env.example .env
docker-compose up --build
```

### Launch Frontend
```bash
cd frontend
flutter pub get
flutter run -d chrome # or android, ios, windows, macos
```

---

_This seed project is designed for immediate use or further extension. All modules should include internal comments and follow clean code principles for AI-assisted collaboration._