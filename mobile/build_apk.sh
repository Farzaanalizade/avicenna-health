#!/bin/bash
# APK Builder - Linux/Mac Version
# Use this on a Linux/Mac machine to build APK without pub.dev issues

set -e

echo "======================================="
echo "  Avicenna Health - APK Builder"
echo "======================================="
echo ""

# Change to mobile directory
cd "$(dirname "$0")/mobile"

echo "[1/5] Setting environment variables..."
export FLUTTER_SKIP_UPDATE_CHECK=true
export FLUTTER_NO_ANALYTICS=true
export PUB_HOSTED_URL="https://pub.dev"
export FLUTTER_STORAGE_BASE_URL="https://storage.googleapis.com/flutter_infra_release/releases/stable"

echo "[2/5] Checking Flutter installation..."
flutter --version

echo ""
echo "[3/5] Cleaning previous builds..."
flutter clean

echo ""
echo "[4/5] Getting dependencies..."
flutter pub get || flutter pub get --offline

echo ""
echo "[5/5] Building APK (Release mode)..."
flutter build apk --release

echo ""
echo "======================================="
echo "✓ APK built successfully!"
echo ""
APK_PATH="build/app/outputs/flutter-apk/app-release.apk"
if [ -f "$APK_PATH" ]; then
    echo "Location: $(pwd)/$APK_PATH"
    echo ""
    echo "Install on device:"
    echo "  adb install -r $APK_PATH"
else
    echo "✗ APK not found!"
    exit 1
fi
echo "======================================="
