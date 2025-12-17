# Avicenna AI - AI Agent Instructions

## Project Overview

**Avicenna Health** is a comprehensive health monitoring platform combining traditional medicine (Persian, Chinese, Indian) with modern AI and IoT sensors. It's a **full-stack system** with:
- FastAPI backend (Python)
- Flutter mobile app (Dart)
- AI integration (Google Gemini, Claude vision)
- Sensor & wearable device support
- Multi-modal analysis (tongue, eye, audio, skin)

## Architecture Quick Reference

```
┌─ Backend (FastAPI)
│  ├─ models/: SQLAlchemy ORM (Patient, SensorData, HealthRecord, etc.)
│  ├─ routers/: API endpoints (auth, patients, diagnosis, sensors)
│  ├─ services/: Business logic (GeminiService, TongueAnalyzer, etc.)
│  ├─ schemas/: Pydantic request/response models
│  ├─ core/: Config, security, dependencies
│  └─ crud/: Database operations
│
├─ Mobile (Flutter)
│  ├─ lib/screens/: UI pages (authentication, dashboard, analysis)
│  ├─ lib/services/: API calls, sensor integration, local storage
│  ├─ lib/models/: Data classes matching backend schemas
│  ├─ lib/database/: SQLite local storage (offline-first)
│  └─ lib/controllers/: State management (GetX)
│
└─ ML Models (Optional local processing)
   └─ ml_models/: TensorFlow/PyTorch models for offline analysis
```

## Critical Patterns & Conventions

### Database Models
- **Location**: `backend/app/models/`
- **Pattern**: Inherit from `Base` (SQLAlchemy `declarative_base`)
- **Standard Fields**: `id`, `created_at`, `updated_at` (use `func.now()` for defaults)
- **Relationships**: Use `relationship()` with `back_populates` for bidirectional links
- **Example**: `Patient` model has many-to-many with `SensorData`, `HealthRecord`, etc.
- **Key Models**:
  - `Patient`: Core user with gender, MizajType (constitutional type), medical history
  - `SensorData`: Raw sensor readings with confidence scores
  - `WearableDevice`: Device tracking (Apple Watch, Fitbit) with connection status
  - `PulseAnalysis`: Avicenna-specific pulse diagnostics

### Enums for Medical Concepts
- **Location**: `backend/app/models/enums.py`
- **Current Enums**: `Gender`, `MizajType` (9 types: GARM, SARD, TAR, KHOSHK, and combinations)
- **Usage**: Stored as SQLAlchemy `Enum` columns, passed through schemas
- **Persian Medicine Terms**: MizajType represents the 4 humours balance system

### API Routers
- **Location**: `backend/app/routers/`
- **Pattern**: FastAPI `APIRouter` with prefix (e.g., `/api/auth`, `/api/patients`)
- **Dependency Injection**: Use `Depends(get_db)` for database sessions
- **Response Models**: Always specify `response_model` from schemas
- **Key Routers**:
  - `auth.py`: Register, login (returns JWT token)
  - `patients.py`: CRUD operations for patient profiles
  - `avicenna_diagnosis.py`: Diagnostic endpoints using traditional medicine logic
  - `sensor_diagnostic.py`: Sensor data upload and processing
  - `analysis_service.py`: Multi-modal analysis coordination

### Schemas (Request/Response)
- **Location**: `backend/app/schemas/`
- **Pattern**: Pydantic `BaseModel` for validation and serialization
- **Convention**: Separate `{Model}Register`, `{Model}Response`, `{Model}Update` schemas
- **Enum Usage**: Import from `models.enums` directly
- **JSON Responses**: Return JSON instead of model instances

### Services & Business Logic
- **Location**: `backend/app/services/`
- **Pattern**: Stateless service classes with static or instance methods
- **Key Services**:
  - `gemini_service.py`: Image analysis (tongue, eye) via Google Gemini API
  - `tongue_analyzer.py`: Avicenna-specific tongue diagnosis logic
  - `avicenna_knowledge.py`: Traditional medicine knowledge base and recommendations
  - `image_analysis.py`: General image processing (OpenCV, PIL)
  - `audio_analysis.py`: Heartbeat/breathing sound analysis (librosa)
- **Fallback Pattern**: Services check `if not self.model:` and return `_get_default_response()` for graceful degradation

### Authentication & Security
- **Location**: `backend/app/core/security.py`
- **Pattern**: JWT tokens with `python-jose` and bcrypt password hashing
- **Dependency**: `Depends(get_current_user)` in protected routes
- **Token Expiry**: Default 7 days (168 hours) - defined in config

### Configuration
- **Location**: `backend/app/core/config.py`
- **Pattern**: Pydantic `BaseSettings` with `.env` file loading
- **Environment Variables**: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `DATABASE_URL`
- **CORS**: Configured for localhost:3000, localhost:5173, and mobile clients
- **File Uploads**: Max 5MB for images, allowed types: JPEG, PNG, WebP

### Database Session Management
- **Pattern**: `get_db()` dependency yields sessions from `SessionLocal`
- **Cleanup**: Session automatically closes in finally block
- **Usage**: Pass to routers as `db: Session = Depends(get_db)`

## Mobile App Patterns (Flutter)

### Architecture
- **State Management**: GetX (simple and reactive)
- **Database**: sqflite (SQLite) for offline-first data storage
- **API Client**: http or Dio with JWT token handling
- **Pattern**: Models match backend schemas exactly (code generation possible)

### Key Services
- `services/api_service.dart`: Backend API calls with auth headers
- `services/sensor_service.dart`: Phone sensors (camera, microphone, gyroscope)
- `services/storage_service.dart`: Local SQLite operations
- `controllers/`: GetX state management (extends GetxController)

### Testing Strategy
- **Backend**: Use pytest with `TestClient` from FastAPI
- **Mobile**: Flutter widget tests with `testWidgets`
- **Integration**: Curl/Postman scripts provided (see `backend_test.html`, `test_api.py`)

## Critical Developer Workflows

### Starting Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your API keys
python run_backend.py
# or: uvicorn app.main:app --reload
# API docs at: http://localhost:8000/docs
```

### Starting Mobile
```bash
cd mobile
flutter pub get
flutter run  # Requires connected device or emulator
```

### Database Initialization
- Tables created automatically via `Base.metadata.create_all(bind=engine)` in `main.py`
- Models must be imported in `main.py` before table creation
- Use seed scripts: `backend/seed_data.py`, `backend/seed_extended_data.py`

### Testing Backend
```bash
pytest backend/tests/  # Run test suite
python test_api.py     # Quick API validation
curl http://localhost:8000/health  # Health check
```

## Integration Points

### Backend to AI APIs
- **Google Gemini**: Used for image analysis (tongue, eye, skin)
  - Prompt engineering for medical context in Persian/English
  - Fallback responses if API unavailable
  - Retry logic with exponential backoff
- **Local Models**: Optional TensorFlow models in `ml_models/` directory
  - Deployment strategy: Quantized models for mobile
  - Performance: Async processing with background tasks

### Backend to Mobile
- **API Authentication**: JWT tokens in `Authorization: Bearer {token}` headers
- **Data Sync**: Patient creates account → Backend stores encrypted password → Mobile authenticates → Receives JWT
- **Sensor Data Flow**: Mobile captures data locally → Batches upload to `/api/sensor_diagnostic/` endpoint
- **Real-time Updates**: WebSocket support (if needed, add to future roadmap)

### Mobile to Sensors
- **Wearables**: Bluetooth LE protocol (iOS: HealthKit, Android: Google Fit)
- **Phone Sensors**: Camera (image capture), microphone (audio), gyroscope (motion)
- **Data Storage**: Local SQLite until network available, then sync

## Project-Specific Conventions

### Naming Conventions
- **Database Tables**: `snake_case` plural (e.g., `patients`, `sensor_data`, `wearable_devices`)
- **API Endpoints**: `/api/{resource}/{action}` (e.g., `/api/auth/login`, `/api/patients/{id}`)
- **Variables**: Persian medicine context uses Persian names in comments (e.g., "نبض" for pulse)
- **Enum Values**: `snake_case` lowercase (e.g., `MizajType.GARM_TAR`)

### Documentation
- **Persian Text**: Supported throughout (comments, field descriptions, prompts)
- **Medical Context**: Include traditional medicine context in docstrings
- **API Docs**: Auto-generated at `/docs` (Swagger UI) and `/redoc` (ReDoc)

### Error Handling
- **HTTP Status Codes**: 401 for auth failures, 400 for validation, 404 for not found, 500 for server errors
- **Error Messages**: Include specific details (e.g., "این ایمیل قبلاً ثبت شده است" - this email already registered)
- **Validation**: Pydantic handles most validation; add custom validators in schemas

### Code Organization
- **Circular Imports**: Avoid by importing models only in `main.py` before table creation
- **Async/Await**: Used in services for I/O-bound operations (API calls, file reading)
- **Decorators**: `@router.post()`, `@router.get()` for endpoints; `@app.on_event("startup")` for initialization

## Key Files Reference

| Component | Files | Purpose |
|-----------|-------|---------|
| Core Setup | `backend/app/main.py` | FastAPI app initialization, route registration |
| Models | `backend/app/models/*.py` | Database schema definitions |
| API | `backend/app/routers/*.py` | Endpoint definitions |
| Business Logic | `backend/app/services/*.py` | AI analysis, sensor processing |
| Schema Validation | `backend/app/schemas/*.py` | Request/response validation |
| Config | `backend/app/core/config.py` | Environment and app settings |
| Database | `backend/app/database.py` | SQLAlchemy session management |
| Mobile | `mobile/lib/**/*.dart` | Flutter UI, state management, API client |

## Common Tasks

### Adding a New API Endpoint
1. Define request/response schemas in `backend/app/schemas/`
2. Create route in `backend/app/routers/`
3. Add business logic in `backend/app/services/` if needed
4. Test with `/docs` or `curl`

### Adding a New Sensor Type
1. Add to `SensorData` model (`backend/app/models/sensor_and_diagnostic_data.py`)
2. Create analysis service in `backend/app/services/`
3. Add router endpoint in `backend/app/routers/sensor_diagnostic.py`
4. Mobile app updates device configuration

### Debugging Issues
- **Backend Logs**: Check FastAPI console output or enable logging in `core/config.py`
- **Database**: SQLite browser for local inspection or `python -c "import sqlite3; ..."`
- **Mobile**: Use `flutter logs` or Android Studio logcat
- **AI API Failures**: Check `.env` file for valid API keys; test with `test_api.py`

## Avoid These Common Mistakes

❌ **Don't**: Forget to import models in `main.py` before `Base.metadata.create_all()`  
✅ **Do**: Import all models at top of `main.py` with `# noqa: F401` to avoid unused-import linting

❌ **Don't**: Store sensitive data (API keys, passwords) in code or Git  
✅ **Do**: Use `.env` file (git-ignored) and `BaseSettings` from Pydantic

❌ **Don't**: Hardcode database URLs or CORS origins  
✅ **Do**: Load from `config.py` using environment variables

❌ **Don't**: Return database models directly from endpoints  
✅ **Do**: Convert to Pydantic schemas using `response_model`

❌ **Don't**: Ignore error handling in AI service calls  
✅ **Do**: Implement fallback responses when APIs are unavailable

---

**Last Updated**: December 2025  
**Status**: Production-ready for Phase 2 mobile integration
