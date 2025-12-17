# Environment Setup Script & Project Overview

## 📁 Complete File Structure

```
D:\AvicennaAI\
│
├── 📋 Documentation (Root Level)
│   ├── README.md                        # Original README
│   ├── README_COMPLETE.md              # ⭐ Full project overview
│   ├── GETTING_STARTED.md              # ⭐ Quick start guide (30 min)
│   ├── SETUP_CHECKLIST.md              # ⭐ Complete setup checklist
│   ├── IMPLEMENTATION_GUIDE.md          # Implementation notes
│   ├── IMPLEMENTATION_COMPLETE.md       # Completion status
│   ├── AI_APIS_COMPARISON.md            # API comparison
│   └── ... (other docs)
│
├── 📁 backend/                         # Backend - FastAPI + Python
│   ├── 📄 Configuration & Setup
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                 # ⭐ FastAPI app entry point
│   │   │   ├── database.py             # Database connection
│   │   │   └── config.py               # App configuration
│   │   │
│   │   ├── requirements.txt            # Python dependencies
│   │   ├── .env (CREATE THIS)          # Environment variables
│   │   ├── .gitignore
│   │   └── setup.py
│   │
│   ├── 📊 Database Models
│   │   ├── app/models/
│   │   │   ├── __init__.py
│   │   │   ├── patient.py             # Patient model
│   │   │   ├── user.py
│   │   │   ├── avicenna_diagnosis.py  # ⭐ Pulse, Urine, Tongue
│   │   │   ├── avicenna_diseases.py   # ⭐ Disease, Remedy, Plant
│   │   │   └── ...
│   │   │
│   │   └── app/schemas/               # Pydantic validation schemas
│   │       ├── avicenna_diagnosis.py
│   │       ├── avicenna_diseases.py
│   │       └── ...
│   │
│   ├── 🔌 API Routes (Endpoints)
│   │   ├── app/routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Authentication endpoints
│   │   │   ├── avicenna_diagnosis.py # ⭐ 22 diagnostic endpoints
│   │   │   ├── avicenna_diseases.py  # ⭐ 25 disease endpoints
│   │   │   ├── analysis_service.py   # ⭐ 12 analysis endpoints
│   │   │   └── ...
│   │   │
│   │   └── (Total: 70+ endpoints)
│   │
│   ├── ⚙️ Business Logic (Services)
│   │   ├── app/services/
│   │   │   ├── avicenna_analysis.py      # ⭐ Core analysis engine
│   │   │   ├── image_analysis.py         # ⭐ Image processing
│   │   │   ├── personalized_recommendations.py  # ⭐ Treatment plans
│   │   │   └── ...
│   │   │
│   │   └── app/crud/                 # Database CRUD operations
│   │       ├── avicenna_diagnosis.py
│   │       ├── avicenna_diseases.py
│   │       └── ...
│   │
│   ├── 📚 Documentation
│   │   ├── DEPLOYMENT_GUIDE.md        # ⭐ Full deployment guide
│   │   ├── QUICK_START.md            # ⭐ 5-min quick start
│   │   ├── AVICENNA_DATABASE_GUIDE.md # ⭐ Database schema details
│   │   └── SERVICES_DOCUMENTATION.md # ⭐ Service layer docs
│   │
│   ├── 🌱 Data Initialization
│   │   ├── seed_data.py              # Initial 20 records
│   │   ├── seed_extended_data.py     # Extended 50+ records
│   │   └── data/                     # Data files
│   │
│   ├── 🧪 Testing & Utils
│   │   ├── test_api.py
│   │   ├── tests/
│   │   ├── uploads/                  # Image uploads
│   │   └── utils/
│   │
│   └── 🐳 Deployment
│       ├── Dockerfile
│       ├── docker-compose.yml
│       └── .dockerignore
│
├── 📁 mobile/                          # Mobile App - Flutter
│   ├── 📱 Flutter Project Root
│   │   ├── pubspec.yaml              # ⭐ Flutter dependencies
│   │   ├── pubspec.lock              # Lock file
│   │   ├── analysis_options.yaml
│   │   ├── .gitignore
│   │   └── README.md
│   │
│   ├── 📄 Entry Point
│   │   └── lib/
│   │       └── main.dart             # ⭐ App entry point
│   │
│   ├── ⚙️ Configuration
│   │   └── lib/config/
│   │       ├── app_config.dart       # App settings & API URL
│   │       ├── theme.dart            # UI theme
│   │       └── routes.dart           # Navigation routes
│   │
│   ├── 🎮 State Management
│   │   └── lib/controllers/
│   │       ├── auth_controller.dart
│   │       ├── health_controller.dart
│   │       └── diagnostic_controller.dart  # ⭐ Diagnostic logic
│   │
│   ├── 🔌 API Integration
│   │   └── lib/services/
│   │       └── api_service.dart      # HTTP client & API calls
│   │
│   ├── 📊 Data Models
│   │   └── lib/models/
│   │       ├── patient.dart
│   │       ├── health_record.dart
│   │       └── ...
│   │
│   ├── 📲 UI Screens
│   │   └── lib/screens/
│   │       ├── splash_screen.dart         # Splash screen
│   │       ├── auth/
│   │       │   ├── login_screen.dart
│   │       │   └── register_screen.dart
│   │       ├── home/
│   │       │   └── home_screen.dart
│   │       ├── capture/
│   │       │   ├── tongue_capture_screen.dart
│   │       │   ├── eye_capture_screen.dart
│   │       │   └── vitals_input_screen.dart
│   │       ├── diagnostic_screen.dart     # ⭐ Main diagnostic UI
│   │       ├── personalized_plan_screen.dart  # ⭐ Treatment plan UI
│   │       ├── history/
│   │       ├── report/
│   │       └── device/
│   │
│   ├── 🎨 Assets
│   │   └── assets/
│   │       ├── images/
│   │       ├── icons/
│   │       ├── animations/
│   │       ├── fonts/
│   │       │   ├── IranSans.ttf
│   │       │   └── Vazirmatn-Regular.ttf
│   │       └── data/
│   │
│   ├── 📚 Documentation
│   │   ├── MOBILE_SETUP.md           # ⭐ Flutter setup guide
│   │   ├── INTEGRATION_GUIDE.md      # ⭐ Backend integration
│   │   └── ANDROID_CONFIG.md         # ⭐ Android config
│   │
│   ├── 🤖 Android Configuration
│   │   ├── android/
│   │   │   ├── app/
│   │   │   │   ├── build.gradle
│   │   │   │   └── src/main/AndroidManifest.xml
│   │   │   └── build.gradle
│   │   │
│   │   ├── build_apk.bat
│   │   ├── build_apk.ps1
│   │   ├── build_apk.sh
│   │   └── init_android.bat
│   │
│   ├── 🍎 iOS Configuration
│   │   ├── ios/
│   │   │   ├── Runner/
│   │   │   └── Podfile
│   │   └── Dockerfile
│   │
│   └── 🐳 Deployment
│       └── Dockerfile
│
├── 📁 ml_models/                       # ML & Training
│   ├── datasets/
│   ├── saved_models/
│   └── training/
│
├── 📁 scripts/                         # Helper Scripts
│   └── (Build, setup scripts)
│
├── 📁 docs/                            # Documentation
│   └── (Additional documentation)
│
└── 🔧 Root Configuration Files
    ├── auto_setup_token.ps1
    ├── auto_setup_token.py
    ├── auto_setup_token.sh
    ├── .gitignore
    └── py.txt
```

---

## 🌍 Environment Variables Setup

### Create `.env` file in `backend/`

**File**: `backend/.env`

```bash
# Database Configuration
DATABASE_URL=sqlite:///./test.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/avicenna_db

# API Configuration
API_TITLE=Avicenna Health API
API_VERSION=1.0.0
API_DESCRIPTION=Traditional Persian Medicine Diagnostic Platform

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (For Mobile App)
ALLOWED_ORIGINS=["http://localhost:8100", "http://192.168.1.1:8100"]

# Debug Mode
DEBUG=True
LOG_LEVEL=INFO

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Firebase (Optional)
FIREBASE_PROJECT_ID=avicenna-health
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_AUTH_DOMAIN=avicenna-health.firebaseapp.com
```

---

## 🚀 Quick Setup Scripts

### Windows PowerShell Script

**File**: `setup.ps1` (Create in root)

```powershell
# Avicenna Health Setup Script for Windows

Write-Host "🚀 Starting Avicenna Health Setup..." -ForegroundColor Green

# Step 1: Backend Setup
Write-Host "`n📦 Setting up Backend..." -ForegroundColor Cyan
cd backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install -r requirements.txt

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# Seed data
Write-Host "Loading seed data..." -ForegroundColor Yellow
python seed_data.py
python seed_extended_data.py

Write-Host "✅ Backend setup complete!" -ForegroundColor Green

# Step 2: Mobile Setup
Write-Host "`n📱 Setting up Mobile App..." -ForegroundColor Cyan
cd ..\mobile

# Get Flutter packages
Write-Host "Getting Flutter packages..." -ForegroundColor Yellow
flutter pub get

Write-Host "✅ Mobile setup complete!" -ForegroundColor Green

Write-Host "`n🎉 All setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start backend: cd backend && python -m uvicorn app.main:app --reload"
Write-Host "2. Open API docs: http://localhost:8000/docs"
Write-Host "3. Run mobile: cd mobile && flutter run"
```

### macOS/Linux Shell Script

**File**: `setup.sh` (Create in root)

```bash
#!/bin/bash

echo "🚀 Starting Avicenna Health Setup..."

# Step 1: Backend Setup
echo -e "\n📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# Seed data
echo "Loading seed data..."
python seed_data.py
python seed_extended_data.py

echo "✅ Backend setup complete!"

# Step 2: Mobile Setup
echo -e "\n📱 Setting up Mobile App..."
cd ../mobile

# Get Flutter packages
echo "Getting Flutter packages..."
flutter pub get

echo "✅ Mobile setup complete!"

echo -e "\n🎉 All setup complete!"
echo "Next steps:"
echo "1. Start backend: cd backend && python -m uvicorn app.main:app --reload"
echo "2. Open API docs: http://localhost:8000/docs"
echo "3. Run mobile: cd mobile && flutter run"
```

### Windows Batch Script

**File**: `setup.bat` (Create in root)

```batch
@echo off
echo 🚀 Starting Avicenna Health Setup...

REM Step 1: Backend Setup
echo.
echo 📦 Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python packages...
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

REM Seed data
echo Loading seed data...
python seed_data.py
python seed_extended_data.py

echo ✅ Backend setup complete!

REM Step 2: Mobile Setup
echo.
echo 📱 Setting up Mobile App...
cd ..\mobile

REM Get Flutter packages
echo Getting Flutter packages...
flutter pub get

echo ✅ Mobile setup complete!

echo.
echo 🎉 All setup complete!
echo Next steps:
echo 1. Start backend: cd backend ^&& python -m uvicorn app.main:app --reload
echo 2. Open API docs: http://localhost:8000/docs
echo 3. Run mobile: cd mobile ^&& flutter run

pause
```

---

## 📋 Installation Verification

### Backend Verification

```bash
# 1. Check virtual environment
python --version
# Should be 3.9+

# 2. Check key packages
python -c "import fastapi; import sqlalchemy; import pydantic; print('✅ All OK')"

# 3. Check database
python -c "from app.models.patient import Patient; print('✅ Database models OK')"

# 4. List API routes
python -c "from app.main import app; print([route.path for route in app.routes][:10])"
```

### Mobile Verification

```bash
# 1. Check Flutter installation
flutter --version
dart --version

# 2. Check project structure
flutter pub list
# Should show all dependencies

# 3. Check analysis
flutter analyze
# Should show no errors

# 4. Check connected devices
flutter devices
# Should show emulator or device
```

---

## 🔄 Common Environment Issues

### Python Virtual Environment Issues

```bash
# Recreate if corrupted
rm -rf backend/venv
python -m venv backend/venv

# Activate in different shells
# PowerShell:
.\venv\Scripts\Activate.ps1

# CMD:
venv\Scripts\activate.bat

# Bash:
source venv/bin/activate
```

### Flutter Environment Issues

```bash
# Get full diagnosis
flutter doctor

# Clean cache
flutter clean

# Update Flutter
flutter upgrade

# Reinstall packages
rm -rf pubspec.lock
flutter pub get
```

### Database Issues

```bash
# SQLite check
python -c "import sqlite3; print(sqlite3.version)"

# Create fresh database
rm test.db
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# Verify tables
sqlite3 test.db ".tables"
```

---

## ✅ Pre-Flight Checklist

Before starting development:

- [ ] Python 3.9+ installed and accessible
- [ ] Flutter SDK 3.0+ installed and in PATH
- [ ] Android Studio / Xcode installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] `.env` file created in backend/
- [ ] Virtual environment created and activated
- [ ] All Python packages installed
- [ ] All Flutter packages installed
- [ ] Backend starts without errors
- [ ] Mobile app runs without errors
- [ ] API endpoints accessible at http://localhost:8000/docs
- [ ] Database tables created

---

## 🎯 Success Indicators

### Backend Success
```
✅ Virtual environment activated
✅ All packages installed successfully
✅ Database initialized with tables
✅ Seed data loaded (20+ records)
✅ Server starts on port 8000
✅ Swagger UI accessible
✅ Can query /api/v1/diseases endpoint
```

### Mobile Success
```
✅ Flutter packages installed
✅ No build errors
✅ App launches on emulator/device
✅ Can navigate between screens
✅ No console errors
```

### Integration Success
```
✅ Mobile app can connect to backend
✅ Can submit diagnostic data
✅ Can receive analysis results
✅ All features working end-to-end
```

---

**Remember**: Always check `GETTING_STARTED.md` for a complete 30-minute quick start!
