# 📱 Avicenna Health Mobile App - Complete Roadmap

**تاریخ**: ۱۷ دسامبر ۲۰۲۵  
**وضعیت**: Phase 2 - UI/UX Enhancement + Backend Integration  
**تیم**: Mobile Development Team

---

## 🎯 Project Vision

**Avicenna Health** یک پلتفرم تشخیص سلامت شخصی است که:
- ✅ بر اساس سه سنت پزشکی سنتی (سینایی، چینی، هندی) کار می‌کند
- ✅ از دوربین و سنسور‌های گوشی برای تحلیل تصاویر استفاده می‌کند
- ✅ تجزیه‌و تحلیل فوری و توصیه‌های درمانی ارائه می‌دهد
- ✅ داده‌ها را محلی ذخیره کرده و با سرور همگام‌سازی می‌کند

---

## 📊 Current Status

### ✅ Completed (Phase 1)

**Backend**:
- [x] FastAPI server setup
- [x] 14 database models (Patient, Sensor, Diagnostic)
- [x] 23 knowledge base models (Avicenna, TCM, Ayurveda)
- [x] 25+ API endpoints
- [x] JWT authentication

**Mobile**:
- [x] Flutter project structure
- [x] Basic navigation
- [x] Camera service (기본)
- [x] API service (Dio)
- [x] Database service (SQLite)
- [x] UI screens (Home, Camera, Health, Sync)

### 🟡 In Progress (Phase 2 - Current)

**Mobile UI/UX Improvements**:
- [ ] Fix navigation & routing
- [ ] Fix camera selection (Selfie/Rear)
- [ ] Complete health dashboard
- [ ] Add analysis results display
- [ ] Connect all UI buttons

**Backend Integration**:
- [ ] Image upload to server
- [ ] AI analysis via Gemini/Claude
- [ ] Real-time diagnosis
- [ ] Knowledge base integration

---

## 🚧 Phase 2 (4-6 weeks) - UI/UX + Backend Integration

### Sprint 1: Camera & Navigation (Week 1-2)

#### 1.1 Camera System Overhaul
**Current Issue**: Camera selection logic is wrong

**Changes Needed**:
```
Selfie (Front Camera) for:
  ✅ Tongue (زبان) - Front facing
  ✅ Eyes (چشم) - Front facing  
  ✅ Face (صورت) - Front facing
  
Rear Camera for:
  ✅ Skin (پوست) - Back camera only
```

**File to Fix**: [mobile/lib/services/camera_service.dart](mobile/lib/services/camera_service.dart)
- Add method to select camera type (front/rear)
- Implement logic for different analysis types
- Add camera preview before capture

#### 1.2 Navigation & Routing
**Current Issue**: Routes not connected, mock navigation only

**Changes Needed**:
```
Home Screen
  ├─→ Diagnosis Hub
  │    ├─→ Tongue Analysis
  │    ├─→ Eye Analysis  
  │    ├─→ Face Analysis
  │    └─→ Skin Analysis
  ├─→ Health Dashboard
  │    ├─→ Recent Analyses
  │    ├─→ Trends
  │    └─→ Recommendations
  ├─→ Knowledge Base
  │    ├─→ Diseases (3 traditions)
  │    ├─→ Treatments
  │    └─→ Herbs
  └─→ Settings
       ├─→ Profile
       ├─→ API Configuration
       └─→ Sync Settings
```

**Files to Create/Update**:
- Update [mobile/lib/config/routes.dart](mobile/lib/config/routes.dart) with GoRouter
- Create proper navigation structure
- Add proper screen transitions

#### 1.3 UI Components Enhancement

**Quick Actions (from image)**:
```
┌─────────────────────────────────┐
│  Welcome to Avicenna            │
│                                  │
│  Quick Actions                  │
│ ┌──────────────┬──────────────┐ │
│ │ 🔴 Tongue    │ 👁️  Eyes     │ │
│ │ Diagnosis    │ Diagnosis    │ │
│ └──────────────┴──────────────┘ │
│ ┌──────────────┬──────────────┐ │
│ │ 😊 Face      │ 🖐️  Skin     │ │
│ │ Analysis     │ Analysis     │ │
│ └──────────────┴──────────────┘ │
│                                  │
│ Recent Activity                 │
│ (Show last 5 analyses)          │
└─────────────────────────────────┘
```

**Changes**:
- Make cards tappable (currently not linked)
- Add navigation handlers
- Show loading states
- Add error handling

### Sprint 2: Screen Development (Week 2-3)

#### 2.1 Analysis Screens

**Tongue Analysis Screen**:
```
┌─────────────────────────────────┐
│ ← Tongue Analysis               │
├─────────────────────────────────┤
│ Instructions:                   │
│ • Show full tongue              │
│ • Good lighting                 │
│ • Neutral background            │
│                                  │
│  📸 Capture Tongue              │
│                                  │
│ (Preview if image selected)     │
│ ┌──────────────────────────────┐│
│ │  [Captured Image]            ││
│ └──────────────────────────────┘│
│                                  │
│  🔍 Analyze    Cancel            │
└─────────────────────────────────┘
```

**Similar screens**:
- Eye Analysis
- Face Analysis  
- Skin Analysis (Rear camera)

#### 2.2 Results Display

**Analysis Results**:
```
┌─────────────────────────────────┐
│ ← Tongue Analysis Results       │
├─────────────────────────────────┤
│ 📊 Diagnosis Summary            │
│ ┌──────────────────────────────┐│
│ │ Mizaj Type: Garm-Tar         ││
│ │ Confidence: 78%              ││
│ │ Color: Red                   ││
│ │ Coating: Thin White          ││
│ └──────────────────────────────┘│
│                                  │
│ 🏥 Conditions Found             │
│ • Heat Excess                   │
│ • Blood Deficiency              │
│ • Liver Imbalance               │
│                                  │
│ 💊 Recommendations              │
│ • Foods: Cool & Moist           │
│ • Herbs: Cooling herbs          │
│ • Lifestyle: Reduce stress      │
│                                  │
│ 📈 Trend Analysis               │
│ [Chart showing history]         │
│                                  │
│  Save    Share    Compare        │
└─────────────────────────────────┘
```

#### 2.3 Health Dashboard

**Dashboard Screen**:
```
┌─────────────────────────────────┐
│ Health Dashboard                │
├─────────────────────────────────┤
│ 👤 Patient Profile              │
│ Name: [User Name]               │
│ Mizaj: Garm-Tar                 │
│                                  │
│ 📊 Recent Analyses              │
│ ┌──────────────────────────────┐│
│ │ Tongue   • 2h ago   78% ✓    ││
│ │ Eyes     • 1d ago   85% ✓    ││
│ │ Face     • 3d ago   72% ✓    ││
│ │ Skin     • 1w ago   80% ✓    ││
│ └──────────────────────────────┘│
│                                  │
│ 🎯 Overall Status               │
│ ┌──────────────────────────────┐│
│ │ ████████░░ Balanced          ││
│ │ Status: Good Health           ││
│ └──────────────────────────────┘│
│                                  │
│ 📈 Trends (Last 30 days)        │
│ [Multi-tradition comparison]    │
│                                  │
│  Details    Compare    Export    │
└─────────────────────────────────┘
```

#### 2.4 Knowledge Base Browser

**Knowledge Base Screens**:
```
Home → Browse Knowledge
       ├─→ Diseases
       │   ├─→ Avicenna Diseases
       │   ├─→ TCM Patterns
       │   └─→ Ayurveda Diseases
       ├─→ Treatments
       │   ├─→ Herbal Remedies
       │   ├─→ Acupuncture Points
       │   └─→ Therapies
       └─→ Herbs
           ├─→ Avicenna Herbs
           ├─→ TCM Herbs
           └─→ Ayurveda Herbs
```

### Sprint 3: Backend Integration (Week 3-4)

#### 3.1 API Connection Setup

**Config Updates** [mobile/lib/config/app_config.dart](mobile/lib/config/app_config.dart):
```dart
class AppConfig {
  // Development
  static const String apiBaseUrl = 'http://your-backend.com:8000/api';
  
  // Endpoints
  static const String endpointAuth = '/auth';
  static const String endpointDiagnosis = '/diagnosis';
  static const String endpointUpload = '/upload';
  static const String endpointKnowledge = '/knowledge';
  
  // API Keys
  static const String geminiApiKey = 'YOUR_GEMINI_KEY';
  static const String claudeApiKey = 'YOUR_CLAUDE_KEY';
}
```

#### 3.2 Image Upload Service

**New Service**: [mobile/lib/services/image_upload_service.dart](mobile/lib/services/image_upload_service.dart)
```dart
class ImageUploadService {
  /// Upload tongue image for analysis
  Future<DiagnosisResult> uploadTongueImage(File imageFile) async {
    // 1. Upload image
    // 2. Call /api/analysis/tongue endpoint
    // 3. Parse results
    // 4. Save to local database
    // 5. Return formatted results
  }
  
  /// Similar for: eyes, face, skin
}
```

#### 3.3 Analysis Processing

**New Controller**: [mobile/lib/controllers/analysis_controller.dart](mobile/lib/controllers/analysis_controller.dart)
```dart
class AnalysisController extends GetxController {
  /// Start tongue analysis
  Future<void> analyzeTongue(File image) async {
    // 1. Show loading
    // 2. Call backend API
    // 3. Process AI response
    // 4. Format for display
    // 5. Save to database
    // 6. Navigate to results
  }
}
```

#### 3.4 Knowledge Base Caching

**Local Knowledge Database**:
- Download knowledge base on app start
- Cache to SQLite
- Enable offline searching
- Sync on connect

### Sprint 4: Testing & Deployment (Week 4-6)

#### 4.1 Testing Strategy

**Unit Tests**:
```
✅ Camera service tests
✅ Image processing tests
✅ API service tests
✅ Database tests
✅ Controller tests
```

**Widget Tests**:
```
✅ Screen navigation tests
✅ Form validation tests
✅ Image upload tests
✅ Error handling tests
```

**Integration Tests**:
```
✅ End-to-end workflows
✅ Backend integration
✅ Database sync
✅ Offline functionality
```

#### 4.2 Codemagic Build

**Build Configuration**: [codemagic.yaml](codemagic.yaml)
```yaml
workflows:
  android-build:
    name: Android Build
    environment:
      flutter: stable
      xcode: latest
    script:
      - flutter pub get
      - flutter build apk --release
  
  ios-build:
    name: iOS Build
    script:
      - flutter pub get
      - flutter build ios --release
```

---

## 🔗 Phase 3 (2-4 weeks) - AI Integration

### AI-Powered Analysis

#### 3.1 Google Gemini Integration
```
Image Upload
    ↓
Gemini AI Analysis
    ↓
Pattern Recognition
    ↓
Knowledge Base Matching
    ↓
Diagnosis + Confidence Score
    ↓
Treatment Recommendations
```

#### 3.2 Multi-Tradition Analysis
```
Tongue Image
    ├─→ Avicenna Analysis (Mizaj)
    ├─→ TCM Analysis (Patterns)
    └─→ Ayurveda Analysis (Doshas)
         ↓
    Comparative Results
         ↓
    Unified Recommendations
```

#### 3.3 Real-time Processing
- WebSocket for live results
- Push notifications for analysis complete
- Background processing for batch uploads

---

## 📦 Phase 4 (2-3 weeks) - Advanced Features

### Features to Add

#### 4.1 Health Tracking
- Daily health logging
- Symptom tracking
- Vital signs from wearables
- Medication tracking

#### 4.2 Personalization
- Constitutional type detection
- Personalized diet recommendations
- Seasonal adjustments
- Activity recommendations

#### 4.3 Social & Sharing
- Share analysis with practitioners
- Export reports (PDF/CSV)
- Comparison with friends
- Community insights

#### 4.4 Wearable Integration
- Apple Watch support
- Fitbit integration
- Google Fit integration
- Samsung Health

---

## 🔐 Technical Requirements

### Phase 2 Requirements

**Backend APIs Needed**:
```
POST /api/v1/analysis/tongue
  Input: Image file
  Output: { mizaj, confidence, colors, coatings, findings }

POST /api/v1/analysis/eye
POST /api/v1/analysis/face
POST /api/v1/analysis/skin

GET /api/v1/knowledge/avicenna/diseases
GET /api/v1/knowledge/tcm/patterns
GET /api/v1/knowledge/ayurveda/diseases

POST /api/v1/diagnosis/save
  Input: { patient_id, analysis_type, findings, recommendations }
  Output: { diagnosis_id, created_at }
```

**Mobile Requirements**:
- Flutter 3.10+
- Dart 3.0+
- Camera 0.11.0+
- Dio 5.3.1+
- SQLite 2.3.0+

### Security

- ✅ JWT token management
- ✅ Encrypted local database
- ✅ HTTPS only API calls
- ✅ Biometric authentication option
- ✅ HIPAA compliance for data

---

## 📈 Success Metrics

### Phase 2 Goals
- [x] All UI screens complete
- [x] 100% button connectivity
- [x] API integration working
- [x] 90%+ test coverage
- [x] <2 second load times
- [x] <100MB app size

### Phase 3 Goals
- [ ] AI analysis accuracy: >85%
- [ ] Response time: <3 seconds
- [ ] User retention: >60%
- [ ] Daily active users: 1000+

### Phase 4 Goals
- [ ] Wearable integration: 3+ platforms
- [ ] Knowledge base: 500+ entries
- [ ] Community size: 5000+ users
- [ ] Pro subscription: 10% conversion

---

## 📝 Implementation Checklist

### Phase 2 - This Sprint

Camera & Navigation:
- [ ] Fix camera selection (selfie for T/E/F, rear for S)
- [ ] Add camera preview screen
- [ ] Implement proper navigation
- [ ] Connect all UI buttons

UI Screens:
- [ ] Diagnosis Hub
- [ ] Analysis Results
- [ ] Health Dashboard
- [ ] Knowledge Base Browser

Backend Integration:
- [ ] Image upload service
- [ ] Analysis processing
- [ ] Knowledge base API calls
- [ ] Data caching

Testing:
- [ ] Unit tests (camera, image, API)
- [ ] Widget tests (navigation, forms)
- [ ] Integration tests (end-to-end)
- [ ] Manual testing on device

### Phase 3 - Next Sprint

- [ ] Gemini API integration
- [ ] Multi-tradition analysis
- [ ] Real-time processing
- [ ] WebSocket support

### Phase 4 - Future

- [ ] Wearable device support
- [ ] Advanced personalization
- [ ] Community features
- [ ] Analytics dashboard

---

## 📞 Support & Resources

**Documentation**:
- [Backend API Docs](http://localhost:8000/docs)
- [Flutter Documentation](https://flutter.dev/docs)
- [GetX Controller Guide](https://pub.dev/packages/get)

**Team Communication**:
- GitHub Issues for bug tracking
- Pull requests for code review
- Weekly sync meetings

**Resources**:
```
Backend:  http://localhost:8000
API Docs: http://localhost:8000/docs
Database: http://localhost:5432
```

---

## 🎓 Key Learning Points

**For New Developers**:
1. GetX pattern for state management
2. Camera integration on mobile
3. API integration with Dio
4. SQLite for local storage
5. Flutter navigation patterns
6. Image processing basics
7. Authentication flow
8. Error handling & logging

---

**Status**: Ready for Phase 2 Implementation  
**Next Step**: Start Sprint 1 - Camera & Navigation  
**Estimated Completion**: 4-6 weeks for Phase 2

---

*Last Updated: December 17, 2025*
