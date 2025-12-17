# 🏥 AvicennaAI - Health Diagnosis Platform
## Traditional Persian Medicine + Modern AI + IoT Health Monitoring

<div align="center">

**Your gateway to personalized health diagnosis using Ibn Sina's wisdom and modern AI**

[Quick Start](#-quick-start) • [Documentation](#-documentation) • [Architecture](#-architecture) • [Status](#-project-status) • [Contributing](#-contributing)

</div>

---

## 🎯 Project Overview

AvicennaAI is an innovative healthcare platform that combines:

- **📚 Traditional Persian Medicine** (Ibn Sina / Avicenna's principles)
- **🤖 Modern AI/ML** (Claude 3, TensorFlow, audio analysis)
- **📱 IoT Sensors** (smartphone camera, wearables, phone sensors)
- **🌍 Holistic Health** (diagnosis, treatment, prevention)

### The Vision

Enable anyone with a smartphone to get personalized, intelligent health diagnostics by combining:
1. Clinical images (tongue, eye, face, skin) from phone camera
2. Vital data (heart rate, SpO2, blood pressure, temperature, movement)
3. Sounds (heartbeat, breathing patterns)
4. Traditional medical wisdom + modern AI analysis

**Result**: Accurate, affordable, accessible healthcare diagnosis for everyone.

---

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Required
python >= 3.10
node >= 16
flutter >= 3.0

# Check installations
python --version
node --version
flutter --version
```

### 2. Backend Setup (5 minutes)
```bash
cd backend
pip install -r requirements.txt
python app/main.py
# Server running on http://localhost:8000
```

### 3. Check API Status
```bash
curl http://localhost:8000/
# Response: {"message": "Avicenna AI API"}
```

### 4. Mobile App (optional)
```bash
cd mobile
flutter pub get
flutter run
```

---

## 📚 Documentation

**Start here based on your role:**

| Role | Start With | Time |
|------|-----------|------|
| **Project Lead** | [Executive Summary](./EXECUTIVE_SUMMARY_AND_QUICK_START.md) | 20 min |
| **Backend Dev** | [Phase 1 Guide](./PHASE_1_IMPLEMENTATION_GUIDE.md) | 40 min |
| **Mobile Dev** | [Roadmap Phase 2](./AVICENNA_COMPLETE_ROADMAP.md#-phase-2-mobile-app---sensor-integration) | 30 min |
| **AI/ML Engineer** | [AI Comparison](./AI_PROVIDERS_COMPARISON_AND_RECOMMENDATION.md) | 50 min |
| **Medical Expert** | [Medical KB](./AVICENNA_MEDICAL_KNOWLEDGE_BASE.md) | 60 min |

### All Documentation

1. **[EXECUTIVE_SUMMARY_AND_QUICK_START.md](./EXECUTIVE_SUMMARY_AND_QUICK_START.md)** ⭐ START HERE
   - Project overview
   - Quick timeline
   - Key priorities
   - Getting started guide

2. **[AVICENNA_COMPLETE_ROADMAP.md](./AVICENNA_COMPLETE_ROADMAP.md)** - The Master Plan
   - 5 phases of development
   - Technical architecture
   - All API endpoints
   - Database schema
   - Cost analysis

3. **[PHASE_1_IMPLEMENTATION_GUIDE.md](./PHASE_1_IMPLEMENTATION_GUIDE.md)** - Build Week 1
   - Week-by-week checklist
   - Code templates
   - Testing strategy
   - Common issues

4. **[AVICENNA_MEDICAL_KNOWLEDGE_BASE.md](./AVICENNA_MEDICAL_KNOWLEDGE_BASE.md)** - Medical Reference
   - Ibn Sina's principles
   - Clinical examinations
   - 4 humors system
   - AI prompts
   - Modern medicine correlation

5. **[AI_PROVIDERS_COMPARISON_AND_RECOMMENDATION.md](./AI_PROVIDERS_COMPARISON_AND_RECOMMENDATION.md)** - AI Analysis
   - Claude 3 vs GPT-4 vs TensorFlow
   - Cost comparison
   - Implementation examples
   - Hybrid architecture

6. **[DOCUMENTATION_INDEX_COMPLETE.md](./DOCUMENTATION_INDEX_COMPLETE.md)** - Guide to All Docs
   - Document index
   - Reading order by role
   - Quick lookup guide
   - Cross-references

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│            Avicenna AI Platform                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Mobile App (Flutter)          Web Dashboard    │
│  ├─ Camera Module              ├─ Patient Portal│
│  ├─ Sensors & Wearables        ├─ Doctor Panel  │
│  ├─ Data Collection            └─ Analytics    │
│  └─ Results Display                             │
│          │                           │           │
│          └───────────┬───────────────┘           │
│                      │                           │
│          ┌───────────▼──────────────┐           │
│          │   FastAPI Backend        │           │
│          ├─────────────────────────┤           │
│          │ • User Authentication   │           │
│          │ • API Endpoints         │           │
│          │ • Data Processing       │           │
│          │ • AI Orchestration      │           │
│          └───────────┬──────────────┘           │
│                      │                           │
│      ┌───────────────┼───────────────┐           │
│      │               │               │           │
│  ┌───▼──┐    ┌──────▼──┐    ┌──────▼───┐      │
│  │Claude│    │Local TF │    │PostgreSQL │      │
│  │Vision│    │Models   │    │Database   │      │
│  └──────┘    └─────────┘    └───────────┘      │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Data Flow

```
Patient Interaction:
  1. Takes images (tongue, eye, face, skin)
  2. Connects wearable device (Apple Watch, Fitbit)
  3. Records audio (heartbeat, breathing)
  4. Uploads to backend
     ↓
Backend Processing:
  1. Validates data quality
  2. Sends to AI provider (Claude primary)
  3. Analyzes images & audio
  4. Maps to Avicenna diagnosis
  5. Cross-references with modern medicine
     ↓
Results:
  1. Generates personalized diagnosis
  2. Provides treatment recommendations
  3. Returns to mobile app
  4. Stores in database
```

---

## 🗂️ Project Structure

```
AvicennaAI/
├── backend/                           # FastAPI server
│   ├── app/
│   │   ├── main.py                   # Entry point
│   │   ├── database.py               # SQLAlchemy config
│   │   ├── models/                   # Database models
│   │   │   ├── patient.py            # Patient model
│   │   │   ├── user.py
│   │   │   ├── sensor_data.py        # NEW in Phase 1
│   │   │   ├── image_analysis.py     # NEW in Phase 1
│   │   │   └── ...
│   │   ├── schemas/                  # Pydantic schemas
│   │   ├── routers/                  # API routes
│   │   │   ├── auth.py
│   │   │   ├── patients.py
│   │   │   ├── sensors.py            # NEW in Phase 1
│   │   │   ├── image_analysis.py     # NEW in Phase 1
│   │   │   └── ...
│   │   └── services/                 # Business logic
│   │       ├── ai_factory.py         # NEW in Phase 1
│   │       ├── avicenna_engine.py    # NEW in Phase 1
│   │       └── ...
│   ├── requirements.txt              # Python dependencies
│   └── run_backend.bat               # Windows startup
│
├── mobile/                            # Flutter app
│   ├── lib/
│   │   ├── main.dart                 # Entry point
│   │   ├── config/                   # Configuration
│   │   ├── screens/                  # UI screens
│   │   ├── controllers/              # State management
│   │   ├── services/                 # Device services
│   │   │   ├── camera_service.dart   # NEW in Phase 2
│   │   │   ├── sensor_service.dart   # NEW in Phase 2
│   │   │   ├── wearable_service.dart # NEW in Phase 2
│   │   │   └── ...
│   │   └── models/                   # Data models
│   ├── pubspec.yaml                  # Flutter dependencies
│   └── run_mobile.bat                # Windows startup
│
├── docs/                             # Documentation
├── ml_models/                        # AI models storage
└── DOCUMENTATION/                    # All guides (YOU ARE HERE)
    ├── EXECUTIVE_SUMMARY_AND_QUICK_START.md
    ├── AVICENNA_COMPLETE_ROADMAP.md
    ├── PHASE_1_IMPLEMENTATION_GUIDE.md
    ├── AVICENNA_MEDICAL_KNOWLEDGE_BASE.md
    ├── AI_PROVIDERS_COMPARISON_AND_RECOMMENDATION.md
    └── DOCUMENTATION_INDEX_COMPLETE.md
```

---

## 📊 Technology Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT + bcrypt
- **AI**: Claude 3 API, TensorFlow, OpenAI Vision API
- **Server**: Uvicorn

### Mobile
- **Framework**: Flutter 3.0+
- **Language**: Dart
- **State**: GetX
- **Camera**: camera package
- **Wearables**: flutter_blue_plus, health package

### Web (Phase 4)
- **Framework**: React + TypeScript
- **UI**: TailwindCSS
- **Charts**: Chart.js / D3.js
- **API**: Axios

### AI/ML
- **Vision**: Claude 3 Opus (primary), TensorFlow (local)
- **Audio**: Librosa, SoundFile
- **Text**: Anthropic Claude (diagnosis)

---

## 🔑 Features

### Phase 1: Backend (Current - Week 1)
- ✅ User authentication & profiles
- ✅ API framework setup
- 🔄 **Database for sensors (IN PROGRESS)**
- 🔄 **API endpoints (IN PROGRESS)**
- 🔄 **Claude integration (IN PROGRESS)**

### Phase 2: Mobile Sensors (Week 2-3)
- [ ] Camera module (tongue, eye, face, skin)
- [ ] Wearable device connection (Bluetooth)
- [ ] Phone sensors (gyroscope, microphone)
- [ ] Local data validation & storage
- [ ] Sync to backend

### Phase 3: AI Models (Week 4-5)
- [ ] Image analysis models
- [ ] Audio analysis (heart sounds, breathing)
- [ ] Avicenna diagnostic engine
- [ ] Treatment recommendations
- [ ] Report generation

### Phase 4: Web Dashboard (Week 6-7)
- [ ] Patient health portal
- [ ] Doctor dashboard
- [ ] Data visualization
- [ ] Report management
- [ ] User settings

### Phase 5: Launch & Scale (Week 8+)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security hardening
- [ ] HIPAA compliance (optional)
- [ ] Production deployment

---

## 💻 Development Workflow

### Getting Latest Code
```bash
git pull origin main
cd backend && pip install -r requirements.txt
cd mobile && flutter pub get
```

### Running Locally

**Backend**:
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Mobile**:
```bash
cd mobile
flutter run
```

**Web** (Phase 4+):
```bash
cd web
npm install
npm start
```

### Testing
```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Mobile tests
cd mobile
flutter test

# API testing (Postman/Insomnia)
# Import collection from: backend/postman_collection.json
```

---

## 📈 Project Status

### Current Phase: 1/5 (Backend)

```
Phase 1 - Backend Enhancement [████░░░░░░] 40%
  ├─ Database schema .......... [████████░░] 90%
  ├─ API endpoints ............ [████░░░░░░] 40%
  ├─ AI integration ........... [██░░░░░░░░] 20%
  └─ Testing .................. [██░░░░░░░░] 20%

Estimated Completion: This Week (Dec 22, 2025)
Next Milestone: Phase 2 Start (Dec 23, 2025)
```

### Recently Completed
- ✅ Initial backend setup
- ✅ User authentication system
- ✅ Patient data models
- ✅ Health record structure
- ✅ API framework
- ✅ CORS configuration
- ✅ All documentation (6 comprehensive guides)

### In Progress
- 🔄 Sensor data models
- 🔄 Image analysis pipeline
- 🔄 Wearable integration framework
- 🔄 Claude 3 integration

### Up Next
- [ ] Vital signs tracking
- [ ] Audio analysis
- [ ] Avicenna diagnosis engine
- [ ] Mobile app sensors
- [ ] Web dashboard

---

## 🎯 Current Focus (This Week)

### Top Priorities
1. **Database**: Create sensor, image, and wearable tables
2. **APIs**: Build endpoints for data collection
3. **AI**: Integrate Claude 3 Vision for image analysis
4. **Testing**: Ensure end-to-end data pipeline works

### Tasks
- [ ] Create `/backend/app/models/sensor_data.py`
- [ ] Create `/backend/app/routers/sensors.py`
- [ ] Set up Claude API integration
- [ ] Test image analysis with sample images
- [ ] Create database migrations

---

## 🛠️ Installation & Setup

### Backend Setup
```bash
# Clone and navigate
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys (Claude, OpenAI, etc.)

# Create database
alembic upgrade head

# Run server
python -m uvicorn app.main:app --reload
```

### Mobile Setup
```bash
# Clone and navigate
cd mobile

# Get dependencies
flutter pub get

# Run on device/emulator
flutter run
```

### Environment Variables
```env
# backend/.env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://user:password@localhost:5432/avicenna
JWT_SECRET=your-secret-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 📊 Architecture Decisions

### Why Claude 3 as Primary AI?
- Superior medical knowledge understanding
- Best at interpreting traditional medicine concepts
- Cost-effective ($0.009 per image analysis)
- Excellent structured output capability
- Strong context window (200K tokens)

See: [AI Providers Comparison](./AI_PROVIDERS_COMPARISON_AND_RECOMMENDATION.md)

### Why Hybrid AI Approach?
- Claude for complex analysis (best accuracy)
- Local TensorFlow for offline capability
- OpenAI as emergency fallback
- Reduces single-provider dependency
- Optimizes cost at scale

### Why 4-humors System?
- Scientifically meaningful metaphors
- Correlates well with modern biomarkers
- Bridges traditional and modern medicine
- Culturally resonant for target market
- Improves patient engagement

---

## 🤝 Contributing

### Report Issues
- Use GitHub Issues
- Include: symptoms, expected behavior, actual behavior
- Attach relevant logs if applicable

### Submit Features
1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push: `git push origin feature/your-feature`
5. Submit Pull Request

### Development Guidelines
- Follow PEP 8 (Python)
- Use flutter_lints (Dart)
- Write tests for new features
- Update documentation
- Use conventional commit messages

---

## 📞 Support

### Questions?
- 📖 Check [DOCUMENTATION_INDEX_COMPLETE.md](./DOCUMENTATION_INDEX_COMPLETE.md)
- 📚 Read relevant guide from Documentation section
- 🔍 Search existing issues
- 💬 Start a discussion

### Troubleshooting
- Backend won't start? → Check PostgreSQL connection
- Claude API fails? → Verify API key in `.env`
- Mobile compilation issues? → Run `flutter clean && flutter pub get`
- Database migration error? → Check SQL migration files

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Ibn Sina (Avicenna)** - Foundational medical knowledge
- **Anthropic** - Claude AI models
- **Flutter Team** - Mobile framework
- **Open Source Community** - All libraries and frameworks

---

## 📋 Roadmap

- **Week 1**: Backend database & APIs
- **Week 2-3**: Mobile sensor integration
- **Week 4**: AI model training
- **Week 5**: Avicenna diagnosis engine
- **Week 6-7**: Web dashboard
- **Week 8+**: Testing & production launch
- **Month 3+**: Scale & optimization
- **Month 6+**: Advanced features & research

---

## 📞 Contact

- **Project Lead**: [Your Name/Email]
- **Backend Team**: backend@avicennaai.dev
- **Mobile Team**: mobile@avicennaai.dev
- **Questions**: help@avicennaai.dev

---

## 🎓 Learning Resources

### Medical
- Book: "The Canon of Medicine" - Ibn Sina
- Course: "Islamic Golden Age Medicine" - Coursera
- Paper: "Avicenna's Influence on Modern Medicine"

### Technical
- Course: "FastAPI Complete Course" - Udemy
- Course: "Flutter for Beginners" - Google Codelabs
- Course: "AI Image Recognition" - Fast.ai

### AI
- Course: "Claude API Mastery" - Anthropic Docs
- Course: "TensorFlow for Medical Imaging" - Google
- Paper: "Vision Transformers in Medical Imaging" - arxiv

---

<div align="center">

**Made with ❤️ for better healthcare**

[⬆ back to top](#-avicentaai---health-diagnosis-platform)

---

**Status**: 🟡 In Active Development (Phase 1)  
**Last Updated**: December 15, 2025  
**Version**: 0.1.0-alpha  
**Next Milestone**: Phase 1 Completion (Dec 22, 2025)

</div>
