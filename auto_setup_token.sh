#!/bin/bash

# Automated Dart Pub Token Setup for Flutter (Bash Version)
# This can be run via Git Bash or WSL

set -e

EMAIL="saal2070@gmail.com"
APP_PASSWORD="atuipwbibtoofsja"
PUB_DEV_URL="https://pub.dev"

echo "=========================================="
echo "🚀 Dart Pub Token Auto-Setup (Bash)"
echo "=========================================="
echo

# Step 1: Navigate to project
echo "📁 Navigating to project..."
cd d:/AvicennaAI/mobile || exit 1
echo "✅ Located at: $(pwd)"
echo

# Step 2: Set environment
export FLUTTER_SKIP_UPDATE_CHECK=true
export FLUTTER_NO_ANALYTICS=true
echo "✅ Environment set"
echo

# Step 3: Add token via echo
echo "🔑 Adding pub.dev token..."
(
  echo "$EMAIL"
  sleep 0.5
  echo "$APP_PASSWORD"
) | dart pub token add "$PUB_DEV_URL" 2>&1 || true

echo "✅ Token addition attempted"
echo

# Step 4: Verify
echo "🔍 Verifying credentials..."
if [ -f "$HOME/.pub-cache/credentials.json" ]; then
    echo "✅ Credentials file exists"
else
    echo "⚠️  Credentials file not yet created"
fi
echo

# Step 5: Clean and test
echo "🧹 Cleaning cache..."
flutter clean 2>/dev/null || true
dart pub cache clean 2>/dev/null || true
echo "✅ Cache cleaned"
echo

# Step 6: Run pub get
echo "📦 Running flutter pub get..."
flutter pub get 2>&1 | head -20

echo
echo "=========================================="
echo "✨ Done!"
echo "=========================================="
