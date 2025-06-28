#!/bin/bash

# Setup script for Android development
# This script ensures local.properties is properly configured

set -e

echo "Setting up Android build environment..."

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "Error: Java 17 or higher is required for Android builds. Current version: $JAVA_VERSION"
    echo "Please install Java 17 or set JAVA_HOME to point to Java 17 installation."
    exit 1
fi
echo "Java version check passed: $(java -version 2>&1 | head -n 1)"

# Get Flutter SDK path
FLUTTER_SDK=$(flutter --version --machine | grep -o '"flutterRoot":"[^"]*"' | cut -d'"' -f4)

if [ -z "$FLUTTER_SDK" ]; then
    echo "Error: Could not find Flutter SDK path"
    exit 1
fi

# Get Android SDK path (try common locations)
ANDROID_SDK=""
if [ -n "$ANDROID_HOME" ]; then
    ANDROID_SDK="$ANDROID_HOME"
elif [ -d "$HOME/Android/Sdk" ]; then
    ANDROID_SDK="$HOME/Android/Sdk"
elif [ -d "/usr/local/android-sdk" ]; then
    ANDROID_SDK="/usr/local/android-sdk"
else
    echo "Warning: Could not find Android SDK. Please set ANDROID_HOME environment variable."
    ANDROID_SDK="$HOME/Android/Sdk"  # Default fallback
fi

# Get version from pubspec.yaml
VERSION_LINE=$(grep "version:" pubspec.yaml)
VERSION_NAME=$(echo "$VERSION_LINE" | sed 's/version: //' | sed 's/+.*//')
VERSION_CODE=$(echo "$VERSION_LINE" | sed 's/.*+//')

echo "Flutter SDK: $FLUTTER_SDK"
echo "Android SDK: $ANDROID_SDK"
echo "Version Name: $VERSION_NAME"
echo "Version Code: $VERSION_CODE"

# Create local.properties
cat > android/local.properties << EOF
flutter.sdk=$FLUTTER_SDK
sdk.dir=$ANDROID_SDK
flutterVersionCode=$VERSION_CODE
flutterVersionName=$VERSION_NAME
EOF

echo "Android build environment setup complete!"
echo "local.properties has been updated." 