# Android Configuration Guide

## Build Configuration

### build.gradle (Project Level)
Location: `android/build.gradle`

```gradle
buildscript {
    repositories {
        google()
        mavenCentral()
    }

    dependencies {
        classpath 'com.android.tools.build:gradle:7.3.0'
        classpath 'com.google.gms:google-services:4.3.15'
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
```

### build.gradle (App Level)
Location: `android/app/build.gradle`

```gradle
apply plugin: 'com.android.application'
apply plugin: 'kotlin-android'
apply from: "$flutterRoot/packages/flutter_tools/gradle/flutter.gradle"
apply plugin: 'com.google.gms.google-services'

android {
    compileSdkVersion 33

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }

    kotlinOptions {
        jvmTarget = '1.8'
    }

    sourceSets {
        main.java.srcDirs += 'src/main/kotlin'
    }

    defaultConfig {
        applicationId "com.avicenna.health"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
        
        multiDexEnabled true
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}

flutter {
    source '../..'
}

dependencies {
    implementation 'com.android.support:multidex:1.0.3'
    implementation 'com.google.firebase:firebase-core:21.1.1'
    implementation 'com.google.firebase:firebase-auth:21.1.0'
}
```

### AndroidManifest.xml
Location: `android/app/src/main/AndroidManifest.xml`

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.avicenna.health">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />

    <!-- Application -->
    <application
        android:label="Avicenna Health"
        android:icon="@mipmap/ic_launcher"
        android:debuggable="false">

        <!-- Main Activity -->
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Notification Channel (Firebase Messaging) -->
        <service
            android:name="com.google.firebase.messaging.FirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>
    </application>
</manifest>
```

## Signing Configuration

### Create Keystore
```bash
keytool -genkey -v -keystore ~/avicenna-release-key.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias avicenna-key
```

### Upload Keystore Reference
Create `android/key.properties`:
```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=avicenna-key
storeFile=/path/to/avicenna-release-key.keystore
```

### Update build.gradle
```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

signingConfigs {
    release {
        keyAlias keystoreProperties['keyAlias']
        keyPassword keystoreProperties['keyPassword']
        storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
        storePassword keystoreProperties['storePassword']
    }
}
```

## Build Commands

### Build Debug APK
```bash
flutter build apk --debug
```

### Build Release APK
```bash
flutter build apk --release
```

### Build App Bundle
```bash
flutter build appbundle --release
```

### Build for Multiple Architectures
```bash
flutter build apk --release --split-per-abi
```

## Testing on Device

### Connect Device
```bash
adb devices
```

### Install APK
```bash
adb install build/app/outputs/flutter-apk/app-release.apk
```

### View Logs
```bash
adb logcat
```

### Run App on Device
```bash
flutter run -v
```

## Firebase Setup

### 1. Create Firebase Project
- Go to [Firebase Console](https://console.firebase.google.com)
- Create new project "avicenna-health"
- Add Android app

### 2. Download google-services.json
- Place in `android/app/google-services.json`

### 3. Update build.gradle
- Already done in the configuration above

### 4. Initialize Firebase in Dart
```dart
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const AvicentaApp());
}
```

## Troubleshooting

### Gradle Build Issues
```bash
# Clean build
flutter clean
cd android
./gradlew clean
cd ..
flutter pub get
flutter build apk --debug
```

### Dependency Issues
```bash
# Update Android dependencies
cd android
./gradlew app:dependencies
```

### Multi-dex Error
Already handled with `multiDexEnabled true` in build.gradle

### Permission Denied
Check `AndroidManifest.xml` has required permissions

### API Level Issues
- Minimum SDK: 21
- Target SDK: 33
- Compile SDK: 33
