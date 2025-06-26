# 🧱 VibeStack Starter – A Modular Fullstack Seed Project

> ⚙️ A ready-to-code starter based on a modular, scalable, and secure architecture — designed for vibecoding productivity with AI tools like Cursor or GitHub Copilot. This project is a complete, functional fullstack application with minimal business logic, ready for rapid prototyping or production-grade development.

## 🎯 Project Status

✅ **COMPLETED** - Full fullstack application with:
- **Backend**: FastAPI with JWT auth, user management, PostgreSQL/SQLite
- **Frontend**: Flutter with Material 3, BLoC state management, cross-platform
- **DevOps**: Docker, CI/CD, tests, linting
- **Documentation**: Comprehensive READMEs and setup guides

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- Python 3.11+
- Flutter SDK 3.22.2+
- Node.js (for CI/CD pipelines, optional)

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd vibeStack
make install
```

### 2. Start the Application
```bash
# Start everything
make start

# Or start individually
make backend-start
make frontend-start
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database Admin**: http://localhost:8080

### 4. Default Credentials
- **Admin**: `admin@vibestack.dev` / `Admin1234!`
- **Test User**: `test@vibestack.dev` / `Test1234!`

## 🧱 Stack Overview

### 🖥 Frontend (Flutter)
- **Framework**: Flutter 3.22.2+ (Web, Mobile, Desktop)
- **State Management**: BLoC pattern with `flutter_bloc`
- **UI**: Material 3 design with dynamic theming
- **Navigation**: `go_router` with adaptive layouts
- **HTTP Client**: `dio` with interceptors
- **Local Storage**: `shared_preferences`
- **Code Generation**: `freezed`, `json_serializable`

### 🔧 Backend (FastAPI)
- **Framework**: FastAPI (async, Python 3.11+)
- **Authentication**: JWT with access/refresh tokens
- **Database**: PostgreSQL (prod), SQLite (dev)
- **ORM**: SQLAlchemy async with Pydantic
- **Security**: bcrypt password hashing
- **Testing**: pytest with async support
- **Linting**: ruff, black

### 📦 DevOps & Tooling
- **Docker**: Multi-stage builds, compose for dev/prod
- **CI/CD**: GitHub Actions with lint, test, build
- **Database**: PostgreSQL with Adminer GUI
- **Environment**: `.env` templates and secrets management
- **Automation**: Comprehensive Makefile

## 🗂️ Project Structure

```
vibeStack/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routers
│   │   │   ├── core/           # Config, DB, security
│   │   │   ├── models/         # SQLAlchemy models
│   │   │   ├── schemas/        # Pydantic schemas
│   │   │   └── services/       # Business logic
│   │   ├── scripts/            # DB init/seed
│   │   ├── tests/              # pytest tests
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── requirements.txt
│   ├── frontend/               # Flutter frontend
│   │   ├── lib/
│   │   │   ├── core/           # App-wide utilities
│   │   │   ├── features/       # Feature modules
│   │   │   └── main.dart
│   │   ├── assets/             # Images, fonts
│   │   ├── test/               # Widget tests
│   │   └── pubspec.yaml
│   ├── .github/workflows/      # CI/CD pipelines
│   ├── Makefile               # Automation
│   └── README.md
```

## 🔐 Security & Features

### Authentication
- JWT tokens with configurable expiry
- Secure password storage (bcrypt)
- Token refresh mechanism
- Role-based access control (RBAC ready)

### API Endpoints
- `GET /health` - Health check
- `POST /auth/login` - JWT authentication
- `POST /auth/refresh` - Token refresh
- `POST /auth/register` - User registration
- `GET /users/me` - User profile
- `GET /users` - List users (admin)
- `PATCH /users/me` - Update profile
- `DELETE /users/{id}` - Delete user (admin)

### Frontend Features
- Responsive Material 3 design
- Adaptive navigation (sidebar/bottom nav)
- Dark/light theme support
- Form validation
- Error handling
- Loading states
- Mock mode for development

## 🛠️ Development

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run with Docker
docker-compose up --build

# Run locally
uvicorn app.main:app --reload

# Run tests
python -m pytest tests/ -v

# Run linting
ruff check . && black --check .
```

### Frontend Development
```bash
cd frontend
# Install dependencies
flutter pub get

# Run on web
flutter run -d chrome

# Run on mobile
flutter run -d android
flutter run -d ios

# Run tests
flutter test

# Analyze code
flutter analyze

# Generate code
flutter packages pub run build_runner build
```

### Database Management
```bash
# Reset database
make db-reset

# Seed data
make seed

# View logs
make logs-db
```

## 🧪 Testing

### Backend Tests
- Unit tests for services
- Integration tests for API endpoints
- Database tests with fixtures
- Authentication tests

### Frontend Tests
- Widget tests for UI components
- BLoC tests for state management
- Integration tests for user flows

### Running Tests
```bash
# All tests
make test

# Backend only
make backend-test

# Frontend only
make frontend-test
```

## 🚀 Deployment

### Production Build
```bash
# Build production images
make prod-build

# Deploy (configure your strategy)
make prod-deploy
```

### Docker Production
```bash
# Backend production
cd backend
docker-compose -f docker-compose.prod.yml up -d

# Frontend production
cd frontend
flutter build web --release
# Deploy build/web/ to your web server
```

## 📱 Platform Support

### Frontend
- ✅ **Web**: Chrome, Firefox, Safari, Edge
- ✅ **Android**: API 21+ (Android 5.0+)
- ✅ **iOS**: iOS 11.0+
- ✅ **Windows**: Windows 10+
- ✅ **macOS**: macOS 10.14+
- ✅ **Linux**: Ubuntu 18.04+

### Backend
- ✅ **Linux**: Ubuntu, CentOS, Alpine
- ✅ **Windows**: Windows 10+ (WSL2)
- ✅ **macOS**: macOS 10.14+
- ✅ **Docker**: All platforms

## 🔧 Configuration

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/vibestack
SECRET_KEY=your-secret-key
ENVIRONMENT=development

# Frontend (app_config.dart)
static const String baseUrl = 'http://localhost:8000';
static const bool enableMockMode = false;
```

### Database Setup
- **Development**: SQLite (automatic)
- **Production**: PostgreSQL (configured)
- **Testing**: In-memory SQLite

## 📚 Documentation

- [Backend README](backend/README.md) - Backend architecture and setup
- [Frontend README](frontend/README.md) - Frontend development guide
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Makefile Help](Makefile) - Available commands

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

_This seed project is designed for immediate use or further extension. All modules include internal comments and follow clean code principles for AI-assisted collaboration._