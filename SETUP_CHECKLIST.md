# Avicenna Health System - Architecture & Setup Checklist

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Avicenna Health Platform                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌────────────────┐  ┌──────────────────┐ │
│  │   Flutter App   │  │   Web Portal   │  │   Doctor Portal  │ │
│  │                 │  │  (Future)      │  │  (Future)        │ │
│  │ - Diagnostics   │  │                │  │                  │ │
│  │ - Reports       │  │  - Admin       │  │  - Patient Mgmt  │ │
│  │ - Plans         │  │  - Analytics   │  │  - Adjustments   │ │
│  └────────┬────────┘  └────────────────┘  └──────────────────┘ │
│           │                                                     │
│           └─────────────────┬──────────────────────────────────┘ │
│                             │                                    │
│                 ┌───────────▼────────────┐                      │
│                 │   FastAPI Backend      │                      │
│                 │  (http://localhost:    │                      │
│                 │       8000)            │                      │
│                 │                        │                      │
│                 │ ┌──────────────────┐   │                      │
│                 │ │ Routers:         │   │                      │
│                 │ │ - Diagnosis      │   │                      │
│                 │ │ - Diseases       │   │                      │
│                 │ │ - Analysis       │   │                      │
│                 │ │ - Auth           │   │                      │
│                 │ └──────────────────┘   │                      │
│                 │                        │                      │
│                 │ ┌──────────────────┐   │                      │
│                 │ │ Services:        │   │                      │
│                 │ │ - Analysis       │   │                      │
│                 │ │ - Image          │   │                      │
│                 │ │ - Recommend      │   │                      │
│                 │ └──────────────────┘   │                      │
│                 └───────────┬────────────┘                      │
│                             │                                    │
│                 ┌───────────▼────────────┐                      │
│                 │   SQLAlchemy ORM       │                      │
│                 │                        │                      │
│                 │ ┌──────────────────┐   │                      │
│                 │ │ Models:          │   │                      │
│                 │ │ - Patient        │   │                      │
│                 │ │ - Pulse          │   │                      │
│                 │ │ - Urine          │   │                      │
│                 │ │ - Tongue         │   │                      │
│                 │ │ - Disease        │   │                      │
│                 │ │ - Remedy         │   │                      │
│                 │ └──────────────────┘   │                      │
│                 └───────────┬────────────┘                      │
│                             │                                    │
│                 ┌───────────▼────────────┐                      │
│                 │   PostgreSQL DB        │                      │
│                 │  (or SQLite Dev)       │                      │
│                 └────────────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow: Diagnostic Process

```
Mobile App
    ├─ Input Pulse Data
    │   ├─ Rate (bpm)
    │   ├─ Type
    │   ├─ Rhythm
    │   └─ Other Properties
    │
    ├─ POST /api/v1/diagnosis/pulse
    │   └─ Save PulseAnalysis
    │
    ├─ Input Urine Data
    │   ├─ Color
    │   ├─ Density
    │   └─ Abnormalities
    │
    ├─ POST /api/v1/diagnosis/urine
    │   └─ Save UrineAnalysis
    │
    ├─ Input Tongue Data
    │   ├─ Color
    │   ├─ Coating
    │   └─ Moisture
    │
    ├─ POST /api/v1/diagnosis/tongue
    │   └─ Save TongueAnalysis
    │
    └─ POST /api/v1/analysis/comprehensive/{id}
        ├─ AvicennaAnalysisEngine
        │   ├─ analyze_pulse()
        │   ├─ analyze_urine()
        │   ├─ analyze_tongue()
        │   └─ synthesize_diagnosis()
        │
        ├─ Determine Mizaj
        │ │
        │ ├─ Pulse + Urine + Tongue Analysis
        │ ├─ Cross-reference with Database
        │ └─ Calculate Mizaj Scores
        │
        ├─ Find Matching Diseases
        ├─ Recommend Remedies
        ├─ Suggest Lifestyle Changes
        ├─ Create Dietary Plan
        │
        └─ Return Results
            ├─ Dominant Mizaj
            ├─ Health Status
            ├─ Recommended Remedies
            ├─ Lifestyle Advice
            └─ Dietary Recommendations
```

## Complete Setup Checklist

### Phase 1: Environment Setup
- [ ] Install Python 3.9+
- [ ] Install Flutter SDK 3.0+
- [ ] Install Android Studio / Xcode
- [ ] Clone Repository
- [ ] Create Virtual Environment

### Phase 2: Backend Setup
- [ ] Navigate to `backend/` directory
- [ ] Create `.env` file with DATABASE_URL
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Initialize database: `python backend/app/database.py`
- [ ] Populate seed data:
  - [ ] `python backend/seed_data.py`
  - [ ] `python backend/seed_extended_data.py`
- [ ] Verify migrations complete
- [ ] Start FastAPI server: `uvicorn app.main:app --reload`
- [ ] Access API docs: `http://localhost:8000/docs`
- [ ] Test endpoints work:
  - [ ] `GET /api/v1/diseases`
  - [ ] `GET /api/v1/symptoms`
  - [ ] `GET /api/v1/medical-plants`

### Phase 3: Mobile Setup
- [ ] Navigate to `mobile/` directory
- [ ] Run `flutter doctor` and resolve issues
- [ ] Run `flutter pub get`
- [ ] Update `lib/config/app_config.dart` with backend URL
- [ ] Start emulator or connect device
- [ ] Run `flutter run`
- [ ] Test app navigation

### Phase 4: Integration Testing
- [ ] Test Pulse Submission Flow
  - [ ] Open Diagnostic Screen
  - [ ] Enter pulse data
  - [ ] Submit pulse
  - [ ] Verify in API docs
- [ ] Test Urine Submission Flow
  - [ ] Enter urine data
  - [ ] Submit urine
  - [ ] Verify in API docs
- [ ] Test Tongue Submission Flow
  - [ ] Enter tongue data
  - [ ] Submit tongue
  - [ ] Verify in API docs
- [ ] Test Comprehensive Analysis
  - [ ] Click "Analyze" button
  - [ ] Verify results display correctly
  - [ ] Check mizaj determination
  - [ ] Review recommendations

### Phase 5: Advanced Features (Optional)
- [ ] Implement image upload for tongue/eye
- [ ] Add real ML models for image analysis
- [ ] Create doctor dashboard
- [ ] Set up Firebase Authentication
- [ ] Add push notifications
- [ ] Create analytics dashboard

### Phase 6: Deployment Preparation
- [ ] Create keystore for Android
- [ ] Build release APK: `flutter build apk --release`
- [ ] Test APK on real device
- [ ] Prepare app store listings
- [ ] Create privacy policy
- [ ] Create terms of service

### Phase 7: Production Deployment
- [ ] Deploy Backend to Cloud (AWS/Heroku/DigitalOcean)
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Upload APK to Google Play Store
- [ ] Submit for review
- [ ] Monitor analytics

---

## Quick Start Commands

### Backend

```bash
# Setup
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt

# Initialize
python seed_data.py
python seed_extended_data.py

# Run
python -m uvicorn app.main:app --reload
```

### Mobile

```bash
# Setup
cd mobile
flutter pub get

# Run
flutter run

# Build
flutter build apk --release
```

---

## API Endpoints Reference

### Diagnostic Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/diagnosis/pulse` | POST | Submit pulse analysis |
| `/api/v1/diagnosis/urine` | POST | Submit urine analysis |
| `/api/v1/diagnosis/tongue` | POST | Submit tongue analysis |
| `/api/v1/diagnosis/pulse/{id}` | GET | Get specific pulse |
| `/api/v1/diagnosis/urine/{id}` | GET | Get specific urine |
| `/api/v1/diagnosis/tongue/{id}` | GET | Get specific tongue |

### Analysis Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/analysis/comprehensive/{patient_id}` | POST | Full diagnosis |
| `/api/v1/analysis/personalized-plan/{patient_id}` | GET | 3-phase plan |
| `/api/v1/analysis/weekly-schedule/{patient_id}` | GET | Weekly routine |
| `/api/v1/analysis/dietary-plan/{patient_id}` | GET | Diet plan |
| `/api/v1/analysis/full-report/{patient_id}` | GET | Complete report |

### Disease Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/diseases` | GET | All diseases |
| `/api/v1/diseases/category/{category}` | GET | Diseases by category |
| `/api/v1/remedies/disease/{disease_id}` | GET | Remedies for disease |
| `/api/v1/symptoms/disease/{disease_id}` | GET | Symptoms of disease |

---

## Default Credentials

```
Backend API:
- Base URL: http://localhost:8000
- Docs: http://localhost:8000/docs
- No authentication required (Development)

Database:
- Type: SQLite (development)
- File: test.db
```

---

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --port 8001
```

### Database Connection Error
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Recreate database
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"
```

### Flutter Can't Connect to Backend
```
1. Check backend is running
2. Check API URL in app_config.dart
3. Use 10.0.2.2 instead of localhost for emulator
4. Check device is on same network for real device
```

---

## Support & Documentation

- **Backend Guide**: `backend/DEPLOYMENT_GUIDE.md`
- **Backend Quick Start**: `backend/QUICK_START.md`
- **Mobile Guide**: `mobile/MOBILE_SETUP.md`
- **Integration Guide**: `mobile/INTEGRATION_GUIDE.md`
- **Database Guide**: `backend/AVICENNA_DATABASE_GUIDE.md`
- **Services Doc**: `backend/SERVICES_DOCUMENTATION.md`
