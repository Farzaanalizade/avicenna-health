# Avicenna Health Platform 🏥

> Traditional Persian Medicine Diagnostic Platform with AI-Powered Analysis

## 📋 Overview

**Avicenna Health** is a comprehensive health diagnostic platform based on Abu Ali Sina's (Avicenna) medical teachings. The system combines traditional Persian medicine diagnostic principles with modern technology to provide personalized health analysis and treatment recommendations.

### Key Features

✅ **Pulse Analysis** (نبض شناسی)
- Analyze pulse characteristics (rate, type, rhythm, strength)
- Determine mizaj (temperament) from pulse indicators

✅ **Urine Analysis** (ادرار شناسی)
- Track color, density, clarity
- Identify abnormalities and sediments
- Correlate with health conditions

✅ **Tongue Diagnosis** (زبان شناسی)
- Visual tongue assessment
- Coating, color, and moisture analysis
- Organ health indicators

✅ **AI-Powered Analysis**
- Comprehensive diagnosis from combined data
- Mizaj (temperament) determination
- Disease prediction and matching

✅ **Personalized Treatment**
- 3-phase treatment plans
- Traditional remedy recommendations
- Lifestyle and dietary guidelines

✅ **Mobile-First Design**
- Flutter-based mobile application
- User-friendly diagnostic interface
- Real-time analysis and recommendations

---

## 🏗️ Architecture

```
Avicenna Health Platform
├── Backend (FastAPI + SQLAlchemy)
│   ├── REST API (70+ endpoints)
│   ├── Analysis Services (Pulse, Urine, Tongue)
│   ├── Recommendation Engine
│   └── PostgreSQL/SQLite Database
│
└── Frontend (Flutter)
    ├── Diagnostic Interface
    ├── Personalized Plans
    ├── Health History
    └── Reports & Analytics
```

### System Components

1. **Backend Server** - FastAPI with Python
2. **Database** - PostgreSQL (production) / SQLite (development)
3. **Mobile App** - Flutter with GetX state management
4. **API Layer** - RESTful API with 70+ endpoints
5. **Services** - Analysis, recommendations, image processing

---

## 📦 Installation

### Prerequisites

```bash
# Backend
- Python 3.9+
- PostgreSQL (optional, SQLite for dev)
- pip

# Mobile
- Flutter SDK 3.0+
- Android Studio / Xcode
- Dart 3.0+
```

### Quick Start

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python seed_data.py
python seed_extended_data.py

# Start server
python -m uvicorn app.main:app --reload
```

Server will be available at: `http://localhost:8000`

#### Mobile Setup

```bash
# Navigate to mobile
cd mobile

# Get dependencies
flutter pub get

# Run on emulator/device
flutter run

# Build APK
flutter build apk --release
```

---

## 🚀 Usage

### 1. Submit Diagnostic Data

```bash
# Submit Pulse Analysis
curl -X POST http://localhost:8000/api/v1/diagnosis/pulse \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "pulse_rate": 72,
    "type": "daqiq",
    "rhythm": "montazem"
  }'
```

### 2. Get Comprehensive Analysis

```bash
# Analyze all diagnostic data
curl -X POST http://localhost:8000/api/v1/analysis/comprehensive/1 \
  -H "Content-Type: application/json" \
  -d '{
    "pulse_data": {...},
    "urine_data": {...},
    "tongue_data": {...}
  }'
```

### 3. View Personalized Plan

```bash
# Get 3-phase treatment plan
curl http://localhost:8000/api/v1/analysis/personalized-plan/1
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `SETUP_CHECKLIST.md` | Complete setup checklist and architecture |
| `backend/DEPLOYMENT_GUIDE.md` | Backend deployment and configuration |
| `backend/QUICK_START.md` | 5-minute backend setup |
| `backend/AVICENNA_DATABASE_GUIDE.md` | Database schema and models |
| `backend/SERVICES_DOCUMENTATION.md` | Service layer documentation |
| `mobile/MOBILE_SETUP.md` | Mobile app setup and build guide |
| `mobile/INTEGRATION_GUIDE.md` | Mobile-Backend integration |
| `mobile/ANDROID_CONFIG.md` | Android-specific configuration |

---

## 🗄️ Database Models

### Core Models

**Patient**
- Basic patient information
- Medical history
- Contact information

**Diagnostic Models**
- `PulseAnalysis` - Pulse characteristics and indicators
- `UrineAnalysis` - Urine properties and abnormalities
- `TongueAnalysis` - Tongue appearance and indicators
- `DiagnosticFinding` - Synthesized diagnosis

**Disease Models**
- `Disease` - Disease information and categories
- `Symptom` - Individual symptoms
- `TraditionalRemedy` - Herbal and traditional treatments
- `MedicalPlant` - Medicinal plant database

**Treatment Models**
- `MizajBalanceTreatment` - Personalized 3-phase plans
- `DiseaseRemedyRelation` - Disease-remedy mapping

---

## 🔌 API Endpoints

### Diagnostic Endpoints (22)
```
POST   /api/v1/diagnosis/pulse              - Submit pulse
GET    /api/v1/diagnosis/pulse/{id}         - Get pulse
GET    /api/v1/diagnosis/pulses              - List pulses
POST   /api/v1/diagnosis/urine               - Submit urine
POST   /api/v1/diagnosis/tongue              - Submit tongue
GET    /api/v1/diagnosis/report/patient/{id} - Get diagnosis report
```

### Disease Endpoints (25)
```
GET    /api/v1/diseases                     - List diseases
GET    /api/v1/diseases/category/{cat}      - Filter by category
POST   /api/v1/remedies                      - Add remedy
GET    /api/v1/remedies/disease/{id}        - Get disease remedies
GET    /api/v1/symptoms/disease/{id}        - Get disease symptoms
```

### Analysis Endpoints (12)
```
POST   /api/v1/analysis/comprehensive/{id}  - Full diagnosis
POST   /api/v1/analysis/analyze-tongue-image/{id} - Image analysis
GET    /api/v1/analysis/personalized-plan/{id}   - Treatment plan
GET    /api/v1/analysis/weekly-schedule/{id}     - Weekly routine
GET    /api/v1/analysis/dietary-plan/{id}        - Diet plan
GET    /api/v1/analysis/full-report/{id}         - Complete report
```

---

## 🎨 Mobile App Screens

1. **Splash Screen** - App initialization
2. **Authentication** - Login/Register
3. **Home Screen** - Main dashboard
4. **Diagnostic Screen** - 3-tab interface
   - Pulse analysis
   - Urine analysis
   - Tongue analysis
5. **Results Screen** - Analysis results
6. **Personalized Plan** - 3-phase treatment plan
7. **Weekly Schedule** - Daily routines
8. **Dietary Plan** - Food recommendations
9. **Health History** - Past records
10. **Device Connect** - Connect to health devices (future)

---

## 🔐 Security

- Input validation on all endpoints
- CORS configuration for mobile app
- Optional JWT authentication (to be implemented)
- Database encryption (production)
- HTTPS/SSL support

---

## 🧪 Testing

### Backend API Testing

```bash
# Using curl
curl http://localhost:8000/docs

# Or use Postman
# Import: avicenna-api.postman_collection.json
```

### Mobile Testing

```bash
# Run on emulator
flutter run

# Debug mode
flutter run --debug

# Release mode
flutter run --release
```

---

## 📊 Data Structure Example

### Complete Diagnostic Flow

```json
{
  "patient_id": 1,
  "pulse_analysis": {
    "pulse_rate": 72,
    "type": "daqiq",
    "rhythm": "montazem",
    "temperature": "normal",
    "mizaj_indicators": {
      "garm_sard": 0.5,
      "khosh_khoshk": 0.6
    }
  },
  "urine_analysis": {
    "color": "zard",
    "density": "motavassset",
    "abnormalities": [],
    "mizaj_correlation": {
      "garm": 0.4,
      "sard": 0.2
    }
  },
  "tongue_analysis": {
    "body_color": "pink",
    "coating": "white",
    "organ_indicators": {
      "heart": "normal",
      "liver": "slightly_warm"
    }
  },
  "diagnosis": {
    "dominant_mizaj": "garm_motavassset",
    "health_status": "balanced",
    "confidence": 0.85,
    "recommended_remedies": [
      "honey",
      "rose_water",
      "sumac"
    ],
    "lifestyle_tips": [
      "Moderate exercise",
      "Cool diet in summer"
    ]
  }
}
```

---

## 🚀 Deployment

### Development

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Mobile (Emulator)
cd mobile
flutter run
```

### Production

```bash
# Backend (Cloud)
# Deploy to AWS/Heroku/DigitalOcean
# Set environment variables
# Configure database

# Mobile (Play Store)
cd mobile
flutter build appbundle --release
# Upload to Google Play Store
```

---

## 📱 Mobile Requirements

- **Minimum SDK**: Android 21+
- **Target SDK**: Android 33+
- **iOS**: 12.0+
- **Storage**: ~100MB
- **RAM**: 512MB minimum

---

## 🔄 Development Roadmap

### Phase 1 ✅ (Complete)
- Core database design
- API endpoints development
- Basic analysis services
- Mobile UI screens

### Phase 2 🔄 (In Progress)
- Real ML models for image analysis
- Doctor dashboard
- Advanced analytics

### Phase 3 📋 (Planned)
- Firebase integration
- Push notifications
- Multi-language support
- Advanced reporting

### Phase 4 📋 (Future)
- Web portal
- API marketplace
- Integration with health devices
- Clinical validation studies

---

## 💡 Key Concepts

### Mizaj (Temperament)
- **Garm-Khoshk** (Hot-Dry)
- **Garm-Tar** (Hot-Moist)
- **Sard-Khoshk** (Cold-Dry)
- **Sard-Tar** (Cold-Moist)

### Diagnostic Principles
1. Pulse analysis for vital energy
2. Urine analysis for internal balance
3. Tongue diagnosis for organ health
4. Symptom correlation
5. Mizaj determination

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see `LICENSE` file for details.

---

## 👨‍💼 Author

**Avicenna Health Team**
- Based on Abu Ali Sina's medical teachings
- Modern implementation with Flutter & FastAPI

---

## 📞 Support

- **Documentation**: See `/docs` directory
- **Issues**: GitHub Issues
- **Email**: support@avicenna-health.com

---

## 🙏 Acknowledgments

- Abu Ali Sina (Avicenna) - Founder of Persian Medicine
- Flutter Community
- FastAPI Community
- Contributors and Testers

---

## 🔗 Links

- [Flutter Official](https://flutter.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Avicenna - Wikipedia](https://en.wikipedia.org/wiki/Avicenna)
- [GetX Documentation](https://github.com/jonataslaw/getx)

---

**Last Updated**: December 2025
**Version**: 1.0.0

---

## ⚡ Quick Commands

```bash
# Backend
backend:setup       # pip install -r requirements.txt
backend:seed        # python seed_data.py
backend:run         # uvicorn app.main:app --reload

# Mobile
mobile:setup        # flutter pub get
mobile:run          # flutter run
mobile:build        # flutter build apk --release

# Full
setup:all           # Run all setup commands
test:api            # Test API endpoints
test:app            # Test mobile app
```

---

**Status**: ✅ Ready for Development
**Last Check**: December 5, 2025
