# 🚀 Getting Started - راهنمای شروع کار

## ⏱️ 30-Minute Quick Start

### Step 1: Backend (10 minutes)

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Populate database
python seed_data.py
python seed_extended_data.py

# Start server
python -m uvicorn app.main:app --reload
```

✅ Backend running at: **http://localhost:8000**
✅ API Docs at: **http://localhost:8000/docs**

### Step 2: Mobile Setup (10 minutes)

```bash
# Navigate to mobile
cd mobile

# Get dependencies
flutter pub get

# Check everything is OK
flutter doctor

# Run app
flutter run
```

✅ Mobile app should launch on emulator/device

### Step 3: Test Integration (10 minutes)

1. **Open mobile app**
2. **Go to Diagnostic Screen**
3. **Enter sample data:**
   - Pulse: 72 bpm
   - Type: daqiq (دقیق)
   - Rhythm: montazem (منتظم)
4. **Submit pulse**
5. **Repeat for urine and tongue**
6. **Click "Analyze" button**
7. **See results!**

---

## 📋 Detailed Checklist

### ✅ Pre-Installation

- [ ] Python 3.9+ installed
- [ ] Flutter SDK 3.0+ installed
- [ ] Android Studio / Xcode installed
- [ ] Git installed
- [ ] Repository cloned

### ✅ Backend Setup

```bash
cd backend

# 1. Create environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows

# 2. Install packages
pip install -r requirements.txt

# 3. Check database
# Edit app/main.py if needed (SQLite vs PostgreSQL)

# 4. Initialize database
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# 5. Load initial data
python seed_data.py
python seed_extended_data.py

# 6. Start server
python -m uvicorn app.main:app --reload
```

**Verification:**
- Open `http://localhost:8000/docs`
- Should see Swagger UI with all endpoints
- Try GET `/api/v1/diseases` - should return list of diseases

### ✅ Mobile Setup

```bash
cd mobile

# 1. Install Flutter packages
flutter pub get

# 2. Check setup
flutter doctor
# Should show: Android toolchain - develop for Android devices ✓

# 3. Configure backend URL
# Edit: lib/config/app_config.dart
# Change apiBaseUrl to your backend address

# 4. Start emulator or connect device
flutter emulators --launch Pixel_6_API_33

# 5. Run app
flutter run
```

**Verification:**
- App should launch
- You should see login/splash screen
- No error messages in console

### ✅ Integration Test

1. **Backend check:**
   ```bash
   curl http://localhost:8000/api/v1/diseases
   ```
   Should return JSON list of diseases

2. **Mobile check:**
   - Diagnostic screen should load
   - Can enter pulse data
   - Can submit data

---

## 🎯 Common Tasks

### Start Fresh

```bash
# Backend
cd backend
flutter clean
python -m venv venv --clear
pip install -r requirements.txt
python seed_data.py

# Mobile
cd mobile
flutter clean
flutter pub get
```

### Test Single Endpoint

```bash
# Test pulse submission
$body = @{
    patient_id = 1
    pulse_rate = 72
    type = "daqiq"
    rhythm = "montazem"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/diagnosis/pulse" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### View Database

```bash
# Using Python
python -c "
from app.database import SessionLocal
from app.models.patient import Patient

db = SessionLocal()
patients = db.query(Patient).all()
for p in patients:
    print(f'Patient: {p.name}')
"
```

### Debug Mobile App

```bash
# Verbose output
flutter run -v

# Debug on device
adb logcat

# Hot reload
r key in console
R key for full restart
```

---

## 🔧 Configuration Files

### Backend Configuration

**File:** `backend/app/core/config.py`

```python
class Settings:
    # Database
    DATABASE_URL = "sqlite:///./test.db"
    # or
    # DATABASE_URL = "postgresql://user:pass@localhost/db"
    
    # API
    API_TITLE = "Avicenna Health API"
    API_VERSION = "1.0.0"
    
    # CORS
    ALLOWED_ORIGINS = ["http://localhost:8100"]
    
    # Security
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
```

### Mobile Configuration

**File:** `mobile/lib/config/app_config.dart`

```dart
class AppConfig {
  // API
  static const String apiBaseUrl = 'http://192.168.1.X:8000';
  static const Duration apiTimeout = Duration(seconds: 30);
  
  // App
  static const String appName = 'Avicenna Health';
  static const bool debugMode = true;
  
  // Patient
  static const int defaultPatientId = 1;
}
```

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Solution
pip install -r requirements.txt
pip install fastapi uvicorn
```

**Issue: "Port 8000 already in use"**
```bash
# Find process
netstat -ano | findstr :8000

# Kill it
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 8001
```

**Issue: "Database connection refused"**
```bash
# Check if DB file exists
Test-Path test.db

# Reset database
rm test.db
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"
```

### Mobile Issues

**Issue: "flutter: command not found"**
```bash
# Add Flutter to PATH
# Windows: Check Environment Variables
# macOS: echo 'export PATH="$PATH:~/flutter/bin"' >> ~/.zshrc
```

**Issue: "Android toolchain not installed"**
```bash
flutter doctor

# Follow suggestions to install missing components
```

**Issue: "App can't connect to backend"**
```dart
// In app_config.dart
// For emulator: 10.0.2.2 instead of localhost
// For real device: Use actual machine IP
static const String apiBaseUrl = 'http://10.0.2.2:8000';
```

**Issue: "Build fails with gradle error"**
```bash
cd mobile
flutter clean
cd android
./gradlew clean
cd ..
flutter pub get
flutter run
```

---

## 📊 Project Structure

```
avicenna-health/
│
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Entry point
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── crud/              # Database operations
│   │   └── core/              # Configuration
│   ├── seed_data.py           # Initial data
│   ├── seed_extended_data.py  # Extended data
│   ├── requirements.txt       # Python packages
│   └── README.md
│
├── mobile/                     # Flutter App
│   ├── lib/
│   │   ├── main.dart          # Entry point
│   │   ├── config/            # App configuration
│   │   ├── models/            # Data models
│   │   ├── controllers/       # GetX controllers
│   │   ├── services/          # API & services
│   │   ├── screens/           # UI screens
│   │   └── assets/            # Images, fonts
│   ├── android/               # Android config
│   ├── ios/                   # iOS config
│   ├── pubspec.yaml          # Flutter packages
│   └── README.md
│
├── docs/                       # Documentation
│   ├── DATABASE.md
│   ├── API.md
│   └── ...
│
└── README.md                   # Main readme
```

---

## 🎓 Learning Resources

### API Testing
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman**: Import collection from docs

### Code Examples

**Create patient:**
```python
from app.database import SessionLocal
from app.models.patient import Patient

db = SessionLocal()
patient = Patient(name="John Doe", age=30)
db.add(patient)
db.commit()
```

**Query disease:**
```python
from app.models.avicenna_diseases import Disease

db = SessionLocal()
diseases = db.query(Disease).filter(
    Disease.mizaj_type == "garm"
).all()
```

**API call from Flutter:**
```dart
final response = await http.get(
  Uri.parse('http://localhost:8000/api/v1/diseases'),
);
print(response.body);
```

---

## ✨ Next Steps

### After Setup

1. **Explore API Docs**
   - Open http://localhost:8000/docs
   - Try each endpoint
   - Understand data structure

2. **Test Mobile App**
   - Enter diagnostic data
   - See analysis results
   - Check recommendations

3. **Review Code**
   - Understand architecture
   - Read models and services
   - Study API routes

4. **Customize**
   - Add more disease data
   - Modify analysis rules
   - Update UI themes

### Advanced Tasks

- [ ] Implement real authentication
- [ ] Add image upload for tongue/eye
- [ ] Integrate ML model for image analysis
- [ ] Create doctor dashboard
- [ ] Deploy to cloud
- [ ] Publish to Play Store

---

## 📞 Getting Help

1. **Check Documentation**
   - `backend/DEPLOYMENT_GUIDE.md`
   - `mobile/MOBILE_SETUP.md`
   - `backend/AVICENNA_DATABASE_GUIDE.md`

2. **Review Examples**
   - API examples in `backend/SERVICES_DOCUMENTATION.md`
   - Flutter examples in `mobile/INTEGRATION_GUIDE.md`

3. **Debug Mode**
   - Flutter: `flutter run -v`
   - Backend: Set `DEBUG=True`

4. **Common Issues**
   - See troubleshooting section above

---

## 🎉 Success!

If you can:
- ✅ Access http://localhost:8000/docs
- ✅ See API endpoints listed
- ✅ Run Flutter app without errors
- ✅ Enter diagnostic data
- ✅ Get analysis results

**Congratulations! System is working! 🎊**

---

**Status**: Ready for Development
**Last Updated**: December 5, 2025
**Version**: 1.0.0

Enjoy using Avicenna Health Platform! 🚀
