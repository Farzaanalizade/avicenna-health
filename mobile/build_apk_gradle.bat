@echo off
REM Avicenna Health - Direct Gradle APK Builder
REM This bypasses Flutter tool's pub.dev requirement and builds directly with Gradle

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo      Avicenna Health - Direct Gradle APK Builder
echo ========================================================
echo.

cd /d "%~dp0"

if not exist "android" (
    echo ERROR: Android folder not found. Run this from mobile root directory.
    exit /b 1
)

echo Step 1: Setting up environment variables...
set JAVA_HOME=
for /d %%i in ("C:\Program Files\Java\jdk*") do set JAVA_HOME=%%i
if "!JAVA_HOME!"=="" for /d %%i in ("C:\Program Files\AdoptOpenJDK\jdk*") do set JAVA_HOME=%%i

if "!JAVA_HOME!"=="" (
    echo ERROR: Java not found. Please install JDK 11 or higher.
    echo Download from: https://adoptopenjdk.net/ or https://www.oracle.com/java/technologies/downloads/
    exit /b 1
)

echo Java Home: !JAVA_HOME!

set ANDROID_SDK_ROOT=%APPDATA%\Local\Android\Sdk
if not exist "!ANDROID_SDK_ROOT!" (
    set ANDROID_SDK_ROOT=C:\Android\sdk
)

if not exist "!ANDROID_SDK_ROOT!" (
    echo ERROR: Android SDK not found at !ANDROID_SDK_ROOT!
    echo Please set ANDROID_SDK_ROOT environment variable.
    exit /b 1
)

echo Android SDK: !ANDROID_SDK_ROOT!
echo.

echo Step 2: Checking dependencies...
if not exist "!JAVA_HOME!\bin\java.exe" (
    echo ERROR: Java executable not found
    exit /b 1
)

echo Java found: !JAVA_HOME!\bin\java.exe
echo.

echo Step 3: Building APK with Gradle...
cd android

if exist "gradlew.bat" (
    echo Using local Gradle wrapper...
    call gradlew.bat clean assembleRelease
) else (
    echo ERROR: Gradle wrapper not found
    exit /b 1
)

cd ..

echo.
echo Step 4: Verifying APK...
if exist "android\app\build\outputs\apk\release\app-release.apk" (
    echo.
    echo ========================================================
    echo          SUCCESS: APK BUILT!
    echo ========================================================
    echo.
    echo APK Location:
    echo %CD%\android\app\build\outputs\apk\release\app-release.apk
    echo.
    echo Next steps:
    echo 1. Connect Android phone via USB
    echo 2. Enable USB Debugging (Settings ^> Developer options)
    echo 3. Run: adb install -r android\app\build\outputs\apk\release\app-release.apk
    echo.
) else if exist "android\app\build\outputs\apk\debug\app-debug.apk" (
    echo.
    echo DEBUG APK found at:
    echo %CD%\android\app\build\outputs\apk\debug\app-debug.apk
    echo.
    echo Install with: adb install -r android\app\build\outputs\apk\debug\app-debug.apk
    echo.
) else (
    echo ERROR: APK not found at expected location
    exit /b 1
)

endlocal
exit /b 0
