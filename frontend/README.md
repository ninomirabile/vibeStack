# 📱 VibeStack Frontend

A modern Flutter application with Material 3 design, BLoC state management, and cross-platform support (Web, Mobile, Desktop).

## 🚀 Features
- **Flutter 3.22.2+** (Web, Mobile, Desktop)
- **Material 3** design system with dynamic theming
- **BLoC pattern** for state management
- **JWT Authentication** with token refresh
- **Responsive UI** with adaptive navigation
- **I18n ready** (English + Italian)
- **Mock mode** for development without backend
- **Clean Architecture** with feature-based organization

## 🗂️ Structure
```
frontend/
  lib/
    core/              # App-wide utilities
      config/          # App configuration
      services/        # API, storage services
      theme/           # Material 3 theming
      routing/         # Navigation setup
      widgets/         # Shared widgets
    features/          # Feature modules
      auth/            # Authentication
        domain/        # Models, repositories
        presentation/  # BLoC, pages, widgets
      user/            # User management
      home/            # Home screen
    main.dart          # App entry point
  assets/              # Images, fonts, icons
  test/                # Widget tests
  pubspec.yaml         # Dependencies
```

## ⚡ Quickstart

### 1. Prerequisites
- Flutter SDK 3.22.2+
- Dart 3.0.0+
- IDE (VS Code, Android Studio)

### 2. Setup & Run
```bash
cd frontend
flutter pub get
flutter run -d chrome  # Web
# or
flutter run -d android # Android
flutter run -d ios     # iOS
flutter run -d windows # Windows
flutter run -d macos   # macOS
```

### 3. Development
```bash
# Run tests
flutter test

# Analyze code
flutter analyze

# Generate code (freezed, json_serializable)
flutter packages pub run build_runner build

# Watch for changes
flutter packages pub run build_runner watch
```

## 🎨 UI Components

### Material 3 Design
- Dynamic color schemes (light/dark)
- Adaptive navigation (sidebar/bottom nav)
- Responsive layouts
- Custom theming with Google Fonts

### Navigation
- **Desktop**: Sidebar navigation
- **Mobile**: Bottom navigation bar
- **Web**: Responsive layout with drawer

### Screens
- **Login**: Email/password authentication
- **Home**: Dashboard with user info
- **Profile**: User profile management
- **Settings**: App preferences

## 🔧 Configuration

### Mock Mode
Enable mock mode for development without backend:
```dart
// In app_config.dart
static const bool enableMockMode = true;
```

### API Endpoints
Configure backend URL in `lib/core/config/app_config.dart`:
```dart
static const String baseUrl = 'http://localhost:8000';
```

## 🧪 Testing
- **Widget tests** for UI components
- **BLoC tests** for state management
- **Integration tests** for user flows

## 📱 Platform Support
- ✅ **Web**: Chrome, Firefox, Safari, Edge
- ✅ **Android**: API 21+ (Android 5.0+)
- ✅ **iOS**: iOS 11.0+
- ✅ **Windows**: Windows 10+
- ✅ **macOS**: macOS 10.14+
- ✅ **Linux**: Ubuntu 18.04+

## 🛠️ Development

### Code Generation
The app uses code generation for:
- **Freezed**: Immutable data classes
- **JSON Serializable**: JSON parsing
- **Build Runner**: Code generation

Run after dependency changes:
```bash
flutter packages pub run build_runner build --delete-conflicting-outputs
```

### State Management
- **BLoC pattern** for complex state
- **Repository pattern** for data access
- **Dependency injection** with RepositoryProvider

### Architecture
- **Clean Architecture** principles
- **Feature-based** organization
- **Separation of concerns**
- **Testable** design

## 📝 Notes
- Backend must be running for full functionality
- Mock mode available for frontend-only development
- See main README for full-stack setup

---
_Designed for AI-assisted, clean, and scalable development._ 