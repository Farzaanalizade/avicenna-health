# 🚀 Codemagic Build & Deployment Guide

**تاریخ**: ۱۷ دسامبر ۲۰۲۵  
**هدف**: Build APK و IPA برای اپ Avicenna Health  
**مرحله**: Ready for Production Build

---

## ✅ Pre-Build Checklist

### Mobile App Verification
- [x] All routes configured
- [x] Camera service fixed (selfie/rear)
- [x] Navigation working
- [x] API service integrated
- [x] Offline mode supported
- [x] No console errors

### Configuration Updates Needed
- [ ] `app_config.dart` - Backend URL updated
- [ ] `AndroidManifest.xml` - Camera permissions
- [ ] `Info.plist` - Camera/Privacy permissions
- [ ] `pubspec.yaml` - Dependencies resolved
- [ ] `.env.example` - Environment variables documented

### Code Quality
- [ ] Code formatted (dart format)
- [ ] No lint warnings
- [ ] Error handling complete
- [ ] No hardcoded values
- [ ] Comments for complex logic

---

## 🔧 Codemagic Configuration

### Step 1: Create codemagic.yaml

**File**: `codemagic.yaml`

```yaml
# Codemagic Build Configuration for Avicenna Health
# Last Updated: December 17, 2025

workflows:
  android-build:
    name: 📱 Android Build - APK Release
    triggering:
      events:
        - push
        - pull_request
      branch:
        patterns:
          - pattern: main
            include: true
          - pattern: develop
            include: true
    environment:
      flutter: stable
      xcode: latest
      cocoapods: default
      groups:
        - avicenna_secrets
    cache:
      cache_paths:
        - ~/.gradle/caches/**/*
        - ~/.gradle/wrapper/**/*
        - $HOME/.pub-cache/**/*
    scripts:
      - name: Set up Flutter
        script: |
          flutter pub get
          flutter pub global activate intl_utils
          
      - name: Format Code
        script: dart format lib/ --line-length 100
        
      - name: Analyze Code
        script: flutter analyze --no-fatal-infos
        
      - name: Run Tests
        script: flutter test --coverage
        
      - name: Build APK (Debug)
        script: |
          flutter build apk --debug \
            --target-platform android-arm64 \
            --split-per-abi
          
      - name: Build APK (Release)
        script: |
          flutter build apk --release \
            --target-platform android-arm64 \
            --build-number=$BUILD_NUMBER
    artifacts:
      - build/app/outputs/**/*.apk
      - build/app/outputs/**/*.aab
      - coverage/**
    publishing:
      email:
        recipients:
          - $DEVELOPER_EMAIL
        notify:
          success: true
          failure: true
      slack:
        channel: '#builds'
        notify_on_build_status: always
        message_template: |
          Android Build {{ status }} for Avicenna Health
          Commit: {{ commit.message }}

  ios-build:
    name: 🍎 iOS Build - IPA Release
    triggering:
      events:
        - push
      branch:
        patterns:
          - pattern: main
            include: true
    environment:
      flutter: stable
      xcode: latest
      cocoapods: default
      groups:
        - avicenna_secrets
        - ios_credentials
    cache:
      cache_paths:
        - ~/.pub-cache/**/*
        - Pods/**/*
    scripts:
      - name: Set up Flutter
        script: |
          flutter pub get
          
      - name: Build iOS
        script: |
          flutter build ios --release \
            --build-number=$BUILD_NUMBER \
            --build-name=1.0.0
            
      - name: Archive & Export IPA
        script: |
          cd ios
          xcodebuild -workspace Runner.xcworkspace \
            -scheme Runner \
            -configuration Release \
            -derivedDataPath build \
            -archivePath build/Runner.xcarchive \
            archive
          
          xcodebuild -exportArchive \
            -archivePath build/Runner.xcarchive \
            -exportPath build/ipa \
            -exportOptionsPlist ExportOptions.plist
    artifacts:
      - build/ipa/**/*.ipa
    publishing:
      email:
        recipients:
          - $DEVELOPER_EMAIL
        notify:
          success: true
          failure: true

  web-build:
    name: 🌐 Web Build
    triggering:
      events:
        - push
      branch:
        patterns:
          - pattern: main
            include: true
    environment:
      flutter: stable
    scripts:
      - name: Build Web
        script: flutter build web --release
    artifacts:
      - build/web/**/*
    publishing:
      email:
        recipients:
          - $DEVELOPER_EMAIL
```

---

## 📋 Environment Variables Setup

### Codemagic Environment Variables

**Name**: `avicenna_secrets`

```
# Backend Configuration
BACKEND_URL=https://api.avicennahealth.com
API_TIMEOUT=30000

# AI Services
GEMINI_API_KEY=your_gemini_api_key
CLAUDE_API_KEY=your_claude_api_key

# Developer Info
DEVELOPER_EMAIL=your_email@example.com
DEVELOPER_NAME=Your Name

# Build Info
BUILD_TYPE=release
TARGET_SDK=34
MIN_SDK=24
```

---

## 🏗️ Android Build Configuration

### AndroidManifest.xml Updates

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.avicenna.health">

    <!-- Required Permissions -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <!-- Bluetooth & Sensors -->
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission android:name="android.permission.BODY_SENSORS" />

    <!-- Feature Requirements -->
    <uses-feature
        android:name="android.hardware.camera"
        android:required="true" />
    <uses-feature
        android:name="android.hardware.camera.front"
        android:required="false" />
    <uses-feature
        android:name="android.hardware.camera.autofocus"
        android:required="false" />

    <application
        android:label="Avicenna Health"
        android:icon="@mipmap/ic_launcher"
        android:theme="@style/LaunchTheme">

        <activity
            android:name=".MainActivity"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize"
            android:exported="true">
            
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
```

---

## 🍎 iOS Build Configuration

### Info.plist Updates

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Privacy Permissions -->
    <key>NSCameraUsageDescription</key>
    <string>We need camera access for health analysis (tongue, eyes, face, skin)</string>
    
    <key>NSPhotoLibraryUsageDescription</key>
    <string>We need to access your photos for health image analysis</string>
    
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>Location helps personalize health recommendations</string>
    
    <key>NSHealthShareUsageDescription</key>
    <string>We need access to your health data for better analysis</string>
    
    <key>NSHealthUpdateUsageDescription</key>
    <string>We can help manage your health data</string>
    
    <key>NSBluetoothPeripheralUsageDescription</key>
    <string>Connect to health wearables</string>
    
    <key>NSMicrophoneUsageDescription</key>
    <string>Microphone access for audio analysis</string>

    <!-- App Configuration -->
    <key>CFBundleName</key>
    <string>Avicenna Health</string>
    
    <key>CFBundleDisplayName</key>
    <string>Avicenna Health</string>
    
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>

    <!-- Supported Orientations -->
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationPortraitUpsideDown</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>

    <!-- Minimum iOS Version -->
    <key>MinimumOSVersion</key>
    <string>12.0</string>

    <!-- Network Security -->
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <key>NSAllowsArbitraryLoadsForMedia</key>
    <false/>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
</plist>
```

---

## 🔒 Signing & Distribution

### Android Signing

**File**: `android/key.properties`

```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=avicenna_key
storeFile=avicenna_keystore.jks
```

**File**: `android/app/build.gradle`

```gradle
android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'),
                          'proguard-rules.pro'
        }
    }
}
```

---

## 🎯 Build Commands

### Local Build (Testing)

```bash
# Install dependencies
flutter pub get

# Format code
dart format lib/ --line-length 100

# Run static analysis
flutter analyze

# Run tests
flutter test

# Build APK (Debug)
flutter build apk --debug

# Build APK (Release)
flutter build apk --release

# Build App Bundle (For Play Store)
flutter build appbundle --release

# Build iOS
flutter build ios --release
```

### Codemagic Build (Automated)

1. Push to GitHub repository
2. Codemagic automatically:
   - Runs tests
   - Analyzes code
   - Builds APK/IPA
   - Sends notification
   - Archives artifacts

---

## 📦 Release Checklist

### Pre-Release
- [ ] Version updated in pubspec.yaml
- [ ] Changelog updated
- [ ] All tests passing
- [ ] No lint warnings
- [ ] App icon updated
- [ ] App name correct
- [ ] Privacy policy ready
- [ ] Terms of service ready

### Android Release
- [ ] APK signed with release key
- [ ] Version code incremented
- [ ] Minimum SDK: 24 (Android 7.0)
- [ ] Target SDK: 34 (Android 14)
- [ ] All permissions justified
- [ ] Screenshots prepared (5+)
- [ ] Description written
- [ ] Contact info provided

### iOS Release
- [ ] IPA built and tested
- [ ] Xcode version compatible
- [ ] Provisioning profiles updated
- [ ] Certificates valid
- [ ] Privacy policy URL provided
- [ ] Screenshots prepared (5+)
- [ ] Description written

---

## 🚀 Release Steps

### Play Store Release

1. **Prepare APK/AAB**:
   ```bash
   flutter build appbundle --release
   # Creates: build/app/outputs/bundle/release/app-release.aab
   ```

2. **Upload to Google Play Console**:
   - Go to Google Play Console
   - Select Avicenna Health app
   - Click Release → Production
   - Upload app bundle
   - Add release notes
   - Review and publish

### App Store Release

1. **Prepare IPA**:
   ```bash
   flutter build ios --release
   # Use Xcode to export IPA
   ```

2. **Upload to App Store Connect**:
   - Use Transporter app
   - Or use Xcode organizer
   - Add TestFlight testers
   - Get reviews approval
   - Release to App Store

---

## 📊 Post-Release Monitoring

### Analytics
- Download statistics
- User reviews/ratings
- Crash reports
- Performance metrics
- User engagement

### Support
- Review app store comments
- Monitor GitHub issues
- Fix bugs immediately
- Release hotfixes as needed
- Collect user feedback

---

## 🔄 Update Process

### For Bug Fixes
1. Fix bug on develop branch
2. Increment patch version (1.0.1)
3. Create release PR
4. Merge to main
5. Codemagic auto-builds
6. Upload new build to stores

### For Feature Releases
1. Develop on feature branch
2. Increment minor version (1.1.0)
3. Update changelog
4. Create release PR
5. Merge to main
6. Tag release (v1.1.0)
7. Codemagic auto-builds
8. Upload to stores

---

## 🎓 Troubleshooting

### Build Fails

**Check**:
1. Dart version compatibility
2. Flutter dependencies
3. Java version for Android
4. Xcode version for iOS
5. Provisioning profiles (iOS)

**Solution**:
```bash
flutter clean
flutter pub get
flutter pub upgrade
flutter doctor -v
```

### Upload Fails

**Check**:
1. App signing correct
2. Version code incremented
3. All permissions declared
4. Screenshots uploaded (5+)
5. Description complete

**Solution**:
- Review Codemagic logs
- Check Play Store console
- Verify signing configuration
- Rerun build

---

## 📱 App Store Links

**Once Released**:
- [Google Play Store](https://play.google.com/store/apps/details?id=com.avicenna.health)
- [Apple App Store](https://apps.apple.com/app/avicenna-health/...)

---

**Status**: Ready for Codemagic Build  
**Next Step**: Connect GitHub to Codemagic + Configure build  
**Timeline**: First build in 24 hours, updates in 2-3 hours
