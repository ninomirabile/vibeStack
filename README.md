# 🧱 VibeStack Starter – A Modular Fullstack Seed Project

> ⚙️ A ready-to-code starter based on a modular, scalable, and secure architecture — designed for vibecoding productivity with AI tools like Cursor or GitHub Copilot.

## 🚀 Purpose

This seed project provides a complete starting point for building modern fullstack applications with a **clean, enterprise-ready architecture**. It’s minimal in business logic, yet powerful in structure — perfect for vibecoding sessions, rapid prototyping, or as a base for real-world projects.

**Inspired by production-grade architectures** used in real backend+frontend platforms (like DARMA), this repo showcases a solid stack without domain-specific logic.

## 🧱 Stack Overview

### 🖥 Frontend

- **Flutter** (Web, Mobile, Desktop – single codebase)
- **BLoC** pattern for state management
- **Clean UI layer** with customizable theming
- **i18n-ready** for future internationalization

### 🔧 Backend

- **FastAPI** – high-performance Python backend
- **Modular structure**: routers, services, models
- **Auth-ready**: JWT with OAuth2 flows
- **ORM**: SQLAlchemy with Pydantic models
- **Database**: PostgreSQL (or SQLite for dev/testing)
- **Optional encryption**: SQLCipher integration ready

### 📦 DevOps & Tooling

- **Docker Compose**: backend + db environment
- **CI/CD**: ready for GitHub Actions or Bitbucket Pipelines
- **Preconfigured Linting & Formatting**
- **Tests**: placeholders for unit, integration, and e2e
- **Cursor & Copilot-friendly**: clear folder structure and typed code

## 🔐 Security & Scalability

Even if it’s a seed project, the foundation is solid:

- JWT token auth, encrypted secrets
- Secure Docker configurations
- Clear separation between core logic and infrastructure
- Ready for multi-tenant adaptation

## 🧰 Included Modules

- ✅ Auth (Login / JWT)
- ✅ Users (CRUD example)
- ✅ Healthcheck endpoint
- 🟡 Placeholder for multi-tenant logic
- 🟡 Placeholder for role-based access control

## 🏁 Getting Started

### Requirements

- Docker / Docker Compose
- Python 3.11+
- Flutter SDK (if you want to run the frontend)

### Launch Backend

```bash
cd backend
cp .env.example .env
docker-compose up --build
```

API available at: `http://localhost:8000/docs`

### Launch Frontend

```bash
cd frontend
flutter run -d chrome
```

(Or target mobile/emulator depending on your dev setup)

## 📂 Project Structure

```bash
├── backend/
│   ├── app/
│   │   ├── api/            # Routers (FastAPI)
│   │   ├── core/           # Config & Security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── services/       # Business logic
│   │   ├── tests/          # Test cases
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/
│   ├── lib/
│   │   ├── blocs/
│   │   ├── views/
│   │   ├── services/
│   └── pubspec.yaml
```

## 🤖 Using with Cursor or Copilot

This repo is designed to enhance AI-assisted development:

- All modules are typed and isolated
- Clear component boundaries for incremental implementation
- Easy to prompt: “generate user CRUD using existing model”

## 💡 What's Next?

> This repo is the foundation — no business logic, no assumptions. You bring the problem. Let AI help you build the solution.

---

## 📄 License

MIT License – use it, break it, learn from it.

---

## 👋 Contributing

This is meant as a clean starting point — feel free to fork, clone, or adapt for your own project. PRs welcome if you want to extend the demo modules.
