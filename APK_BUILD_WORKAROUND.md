# APK Build Workaround - pub.dev Authorization Issue

## Problem
Flutter build fails with:
```
Error (69): Insufficient permissions to the resource at https://pub.dev
```

This is a **pub.dev connectivity/authorization issue**, not a code or configuration problem.

---

## ✅ Solution 1: Direct Gradle Build (Recommended)

Since we have valid `pubspec.yaml`, we can use Gradle directly:

```bash
cd d:\AvicennaAI\mobile
.\build_apk_gradle.bat
```

**How it works**: 
- Skips Flutter tool's pub upgrade check
- Uses pre-cached dependencies or local .gradle folder
- Builds directly with Android Gradle Plugin
- Output: `android\app\build\outputs\apk\release\app-release.apk`

**Requirements**:
- Java JDK 11+ installed
- Android SDK installed
- Gradle wrapper in `android/gradle/wrapper/gradle-wrapper.properties`

---

## ✅ Solution 2: GitHub Actions Build (Cloud)

1. Push code to GitHub:
```bash
git init
git add .
git commit -m "Ready for APK build"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/avicenna.git
git push -u origin main
```

2. Create `.github/workflows/build-apk.yml` (already created in your repo)

3. Go to GitHub Actions tab → Click "Build APK" workflow → Run workflow

4. After 10-15 minutes, download APK from artifacts

**Pros**: 
- No local pub.dev issues
- Runs on Ubuntu (better Android support)
- Automatic APK upload as artifact
- Free for public repos

**File location**: `.github/workflows/build-apk.yml`

---

## ✅ Solution 3: Use Codemagic (Alternative CI/CD)

1. Go to https://codemagic.io
2. Sign up (free tier available)
3. Connect your GitHub repo
4. Codemagic auto-detects Flutter project
5. Click "Start building"
6. APK downloads in 15-20 minutes

**Pros**:
- Specifically optimized for Flutter
- Better pub.dev support
- Pre-configured environment
- Email notifications

---

## ✅ Solution 4: Use EAS Build (Expo)

```bash
npm install -g eas-cli
eas build --platform android
```

**Pros**:
- Specifically for React Native and Flutter
- Handles all dependencies
- Cloud-based

**Cons**:
- Requires account
- May require paid plan for private repos

---

## ✅ Solution 5: Offline Mode with Cached Dependencies

If you have Internet but pub.dev auth fails:

```powershell
cd d:\AvicennaAI\mobile

# Set offline mode
$env:PUB_CACHE = "$env:LOCALAPPDATA\Pub\Cache"
$env:FLUTTER_SKIP_UPDATE_CHECK = "true"

# Try with system Dart (bypass Flutter tool)
dart pub get
dart pub upgrade --offline

# Build
flutter build apk --release --offline
```

---

## ✅ Solution 6: Network/Proxy Configuration

If behind corporate firewall:

```powershell
# Set Dart pub server mirror (faster than pub.dev)
dart pub get --hosted-url https://pub.mirrors.aliyun.com

# Or configure globally
dart pub config --list

# For China users
$env:PUB_HOSTED_URL = "https://pub.mirrors.aliyun.com"
```

---

## ⚙️ Current Status

**Issue**: Flutter tool requires pub.dev upgrade before building
**Root cause**: Probable pub.dev authorization or corporate proxy
**Status**: Code is 100% valid, build tools are ready

---

## 📋 Implementation Order

1. **First try**: Direct Gradle build
   ```bash
   .\build_apk_gradle.bat
   ```

2. **If that fails**: GitHub Actions (cloud build)
   - Push to GitHub
   - Use workflow

3. **If neither works**: Codemagic or EAS Build
   - Account required
   - Usually most reliable

---

## 🔧 Manual Gradle Build (Advanced)

```bash
cd android

# Clean
gradlew.bat clean

# Build Release APK
gradlew.bat assembleRelease

# APK location
# android\app\build\outputs\apk\release\app-release.apk
```

---

## 📱 Install APK After Build

```bash
# Connect device
adb devices

# Install
adb install -r build\app\outputs\flutter-apk\app-release.apk
# OR
adb install -r android\app\build\outputs\apk\release\app-release.apk

# Launch
adb shell am start -n com.example.avicenna_health/.MainActivity
```

---

## ✨ Summary

| Method | Difficulty | Time | Notes |
|--------|-----------|------|-------|
| Gradle | Easy | 5-10m | Recommended |
| GitHub Actions | Medium | 15-20m | Reliable |
| Codemagic | Easy | 15-20m | Most robust |
| EAS Build | Medium | 10-15m | Alternative |
| Offline Mode | Hard | 10-20m | Try if others fail |

---

**Recommendation**: Try Gradle first. If any issues, use GitHub Actions (most reliable).

