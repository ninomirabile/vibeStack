# Android Setup Guide

## Prerequisites

### Java 17 or higher
Android SDK requires Java 17 or higher. You can check your Java version with:
```bash
java -version
```

If you need to install Java 17:
- **Ubuntu/Debian**: `sudo apt install openjdk-17-jdk`
- **macOS**: `brew install openjdk@17`
- **Windows**: Download from [Oracle](https://www.oracle.com/java/technologies/downloads/#java17) or [Adoptium](https://adoptium.net/)

### Android SDK
Make sure you have Android SDK installed and `ANDROID_HOME` environment variable set.

## Setup

### Automatic Setup
Run the setup script:
```bash
cd frontend
./scripts/setup-android.sh
```

### Manual Setup
1. Create `android/local.properties` with:
```properties
flutter.sdk=<path-to-flutter-sdk>
sdk.dir=<path-to-android-sdk>
flutterVersionCode=1
flutterVersionName=1.0.0
```

2. Update version numbers from `pubspec.yaml`

## Building

### Local Development
```bash
# Setup environment
make frontend-setup-android

# Build Android APK
make frontend-build-android

# Or build web
make frontend-build-web
```

### CI/CD
The GitHub Actions workflow automatically:
1. Sets up Java 17
2. Configures Android SDK
3. Sets up local.properties
4. Builds the APK

## Troubleshooting

### Java Version Issues
- Ensure Java 17+ is installed
- Set `JAVA_HOME` environment variable
- Restart your terminal after installation

### Android SDK Issues
- Install Android Studio or command-line tools
- Set `ANDROID_HOME` environment variable
- Accept Android SDK licenses: `sdkmanager --licenses`

### Build Issues
- Clean build: `flutter clean`
- Get dependencies: `flutter pub get`
- Check Flutter doctor: `flutter doctor`

## Version Management

The build system automatically extracts version information from `pubspec.yaml`:
- `version: 1.0.0+1` → `versionName=1.0.0`, `versionCode=1`
- Update the version in `pubspec.yaml` to change both values 