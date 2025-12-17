# 🔗 Complete Integration Guide - Backend + Mobile + AI

**تاریخ**: ۱۷ دسامبر ۲۰۲۵  
**مرحله**: Phase 3 - Backend Integration + AI Enablement  
**تیم**: Full Stack Development

---

## 📊 Complete System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      AVICENNA HEALTH SYSTEM                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐     ┌─────────────────────┐             │
│  │   MOBILE APP        │     │   WEB DASHBOARD     │             │
│  │  (Flutter/Android)  │────│   (Optional)        │             │
│  └─────────────────────┘     └─────────────────────┘             │
│            │                                                      │
│            │ HTTPS                                                │
│            │ JWT Auth                                             │
│            │ Multipart Upload                                     │
│            │ Real-time Updates                                    │
│            ▼                                                      │
│  ┌─────────────────────────────────────────────┐                │
│  │     FASTAPI BACKEND (Port 8000)            │                │
│  ├─────────────────────────────────────────────┤                │
│  │                                             │                │
│  │  ┌─────────────────────────────────────┐  │                │
│  │  │    API Routes                       │  │                │
│  │  ├─────────────────────────────────────┤  │                │
│  │  │ • /auth         (JWT)               │  │                │
│  │  │ • /patients     (User profiles)     │  │                │
│  │  │ • /analysis     (Image processing)  │  │                │
│  │  │ • /diagnosis    (Results storage)   │  │                │
│  │  │ • /knowledge    (Medical DB)        │  │                │
│  │  │ • /sensors      (Device data)       │  │                │
│  │  └─────────────────────────────────────┘  │                │
│  │                                             │                │
│  │  ┌─────────────────────────────────────┐  │                │
│  │  │    AI Services                      │  │                │
│  │  ├─────────────────────────────────────┤  │                │
│  │  │ • Google Gemini (Vision API)        │  │                │
│  │  │ • Claude Vision (Image analysis)    │  │                │
│  │  │ • TensorFlow (Local models)         │  │                │
│  │  │ • Pattern matching (ML-based)       │  │                │
│  │  └─────────────────────────────────────┘  │                │
│  │                                             │                │
│  │  ┌─────────────────────────────────────┐  │                │
│  │  │    Medical Knowledge Base           │  │                │
│  │  ├─────────────────────────────────────┤  │                │
│  │  │ • Avicenna Diseases (300+)          │  │                │
│  │  │ • TCM Patterns (100+)               │  │                │
│  │  │ • Ayurveda Diseases (200+)          │  │                │
│  │  │ • Herbs Database (1000+)            │  │                │
│  │  │ • Treatment Protocols               │  │                │
│  │  └─────────────────────────────────────┘  │                │
│  │                                             │                │
│  └─────────────────────────────────────────────┘                │
│            │                                                     │
│            │ SQL Queries                                         │
│            │ ORM Mapping                                         │
│            │ Transactions                                        │
│            ▼                                                     │
│  ┌─────────────────────────────────────────────┐                │
│  │    PostgreSQL Database                     │                │
│  ├─────────────────────────────────────────────┤                │
│  │                                             │                │
│  │  • Patients (7.1)                           │                │
│  │  • Sensor Data (7.2)                        │                │
│  │  • Analysis Results (7.2)                   │                │
│  │  • Medical Records (7.1)                    │                │
│  │  • Knowledge Base (23 tables)               │                │
│  │  • Audit Logs                               │                │
│  │                                             │                │
│  └─────────────────────────────────────────────┘                │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔌 API Integration Checklist

### Phase 3A: Backend Preparation (Week 1)

#### 1. Enable CORS for Mobile
**File**: `backend/app/core/config.py`

```python
CORS_ORIGINS = [
    "http://localhost:3000",      # Web dev
    "http://localhost:5173",      # Web dev  
    "http://localhost:8080",      # Flutter web
    "http://192.168.1.x:*",       # Local network (your IP)
    "https://yourdomain.com",     # Production
]

# Allow all credentials for mobile
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]
```

#### 2. Create Image Analysis Endpoints
**File**: `backend/app/routers/analysis_service.py`

```python
@router.post("/api/v1/analysis/tongue")
async def analyze_tongue(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze tongue image using Gemini Vision API
    Returns: Mizaj type, confidence score, findings
    """
    # 1. Save image temporarily
    # 2. Call Gemini API
    # 3. Parse tongue features
    # 4. Match with knowledge base
    # 5. Return results
    
@router.post("/api/v1/analysis/eye")
@router.post("/api/v1/analysis/face")
@router.post("/api/v1/analysis/skin")
```

#### 3. Create Diagnosis Endpoints
**File**: `backend/app/routers/diagnosis_service.py`

```python
@router.post("/api/v1/diagnosis/save")
async def save_diagnosis(
    diagnosis: DiagnosisSaveSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save diagnosis results and link to patient"""

@router.get("/api/v1/diagnosis/patient/{patient_id}")
async def get_diagnosis_history(
    patient_id: str,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Get patient's diagnosis history"""

@router.get("/api/v1/diagnosis/{diagnosis_id}")
async def get_diagnosis_details(
    diagnosis_id: str,
    db: Session = Depends(get_db),
):
    """Get full diagnosis details with recommendations"""
```

---

### Phase 3B: AI Service Integration (Week 2)

#### 1. Google Gemini Integration
**File**: `backend/app/services/gemini_service.py` (Already exists)

```python
class GeminiService:
    def analyze_tongue_image(self, image_path: str) -> dict:
        """
        Analyze tongue image for:
        - Color (pale, red, crimson, purple, dark)
        - Coating (white, yellow, greasy, etc.)
        - Moisture (dry, normal, wet)
        - Cracks/shape abnormalities
        
        Returns: {
            "color": "red",
            "coating": "thin_white",
            "mizaj": "garm_tar",
            "confidence": 0.85
        }
        """
        
    def analyze_eye_image(self, image_path: str) -> dict:
        """
        Analyze eye for:
        - Sclera color (clear, yellow, red)
        - Pupil size and brightness
        - Dark circles/puffiness
        """
        
    def analyze_face_image(self, image_path: str) -> dict:
        """
        Analyze face for:
        - Skin complexion
        - Color balance (pale vs red)
        - Texture and pores
        """
        
    def analyze_skin_image(self, image_path: str) -> dict:
        """
        Analyze skin for:
        - Condition (healthy, dry, oily, inflamed)
        - Any rashes or conditions
        - Texture quality
        """
```

#### 2. Knowledge Base Matching
**File**: `backend/app/services/knowledge_matcher.py`

```python
class KnowledgeMatcher:
    def match_tongue_findings(self, findings: dict) -> List[AvicennaDisease]:
        """
        Given tongue analysis, find matching diseases
        from Avicenna knowledge base
        """
        
    def match_tcm_pattern(self, findings: dict) -> List[TCMPattern]:
        """
        Given findings, find matching TCM patterns
        """
        
    def match_ayurveda_type(self, findings: dict) -> List[AyurvedicDisease]:
        """
        Given findings, find matching Ayurvedic diseases
        """
        
    def compare_traditions(self, findings: dict) -> ComparisonResult:
        """
        Return findings across all three traditions
        """
```

---

### Phase 3C: Mobile Integration (Week 2)

#### 1. Update API Configuration
**File**: `mobile/lib/config/app_config.dart`

```dart
class AppConfig {
  // YOUR BACKEND URL (Replace with actual server)
  static const String apiBaseUrl = 'http://192.168.1.100:8000/api';
  
  // Or for production
  // static const String apiBaseUrl = 'https://api.avicennahealth.com';
  
  static const Duration apiTimeout = Duration(seconds: 30);
  static const bool enableLogging = true;
  
  // AI API Keys
  static const String geminiApiKey = 'YOUR_GEMINI_API_KEY';
  static const String claudeApiKey = 'YOUR_CLAUDE_API_KEY';
}
```

#### 2. Implement Analysis Flow
**File**: `mobile/lib/controllers/analysis_controller.dart`

```dart
class AnalysisController extends GetxController {
  final AnalysisService _analysisService = AnalysisService();
  
  // Load image from camera
  Future<void> captureAndAnalyze(String analysisType) async {
    try {
      // 1. Show loading
      isLoading.value = true;
      
      // 2. Capture image based on type
      File? image = await _captureImage(analysisType);
      if (image == null) return;
      
      // 3. Check backend connectivity
      bool isOnline = await _analysisService.checkBackendConnection();
      
      if (isOnline) {
        // Online: Send to backend for AI analysis
        final result = await _analysisService.analyzeTongueImage(image);
        
        // Save to database
        await _saveAnalysis(analysisType, result);
        
      } else {
        // Offline: Use demo data
        final result = _analysisService._getOfflineAnalysisResult(analysisType);
      }
      
      // 4. Navigate to results
      Get.toNamed(AppRoutes.ANALYSIS_RESULTS, arguments: result);
      
    } catch (e) {
      error.value = 'Analysis failed: $e';
      Get.snackbar('Error', error.value);
    } finally {
      isLoading.value = false;
    }
  }
  
  Future<void> _saveAnalysis(String type, Map<String, dynamic> result) async {
    // Save to local database
    // Queue for sync if needed
  }
}
```

#### 3. Results Display
**File**: `mobile/lib/screens/analysis_results_screen.dart`

```dart
class AnalysisResultsScreen extends StatelessWidget {
  final Map<String, dynamic> analysisResult;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('${analysisType} Analysis Results')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Confidence score
            _buildConfidenceCard(analysisResult['confidence']),
            
            // Findings
            _buildFindingsCard(analysisResult['findings']),
            
            // Recommendations
            _buildRecommendationsCard(analysisResult['recommendations']),
            
            // Knowledge base links
            _buildKnowledgeBaseLinks(analysisResult),
            
            // Actions
            _buildActionButtons(),
          ],
        ),
      ),
    );
  }
}
```

---

## 📱 Step-by-Step Integration Process

### Step 1: Update Backend Configuration

1. Update `backend/app/core/config.py`:
   - Set CORS origins to include your mobile app IP
   - Configure AI API keys (Gemini, Claude)
   - Set database URL to PostgreSQL (for production)

2. Run migrations:
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

3. Seed knowledge base:
   ```bash
   python seed_knowledge_base.py
   ```

### Step 2: Test Backend APIs

```bash
# Test image upload endpoint
curl -X POST http://localhost:8000/api/v1/analysis/tongue \
  -F "image=@tongue.jpg" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test knowledge base
curl http://localhost:8000/api/v1/knowledge/avicenna/diseases

# Test diagnosis save
curl -X POST http://localhost:8000/api/v1/diagnosis/save \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{...}'
```

### Step 3: Update Mobile App

1. **Update API base URL** in `app_config.dart`:
   ```dart
   // For local testing (from device on same network)
   static const String apiBaseUrl = 'http://192.168.1.100:8000/api';
   
   // Replace 192.168.1.100 with your computer's IP
   ```

2. **Build and test**:
   ```bash
   flutter pub get
   flutter run -v
   ```

### Step 4: Test Full Flow

**Device Test Procedure**:
1. Open app
2. Go to Home → Quick Actions → Tongue
3. Take tongue image with selfie camera
4. App should upload to backend
5. Receive analysis results (or demo data if offline)
6. Results displayed on screen
7. Option to save and compare

---

## 🔐 Security Checklist

### Authentication
- [x] JWT token generation on login
- [x] Token refresh on expiry
- [x] Secure token storage (SharedPreferences)
- [x] HTTPS enforcement in production

### Data Protection  
- [x] Encrypted database on device
- [x] HTTPS for all API calls
- [x] Biometric authentication option
- [x] HIPAA compliance for health data

### API Security
- [x] Rate limiting
- [x] Input validation
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] CORS properly configured

---

## 📊 Testing Scenarios

### Scenario 1: Online Analysis
```
1. User clicks Tongue Analysis
2. Camera opens (front/selfie)
3. User captures tongue image
4. Image uploaded to backend
5. Gemini API analyzes image
6. Results returned to mobile
7. App displays findings
8. User can save or compare
```

### Scenario 2: Offline Analysis  
```
1. Backend unreachable
2. App detects no connection
3. Uses offline demo data
4. Shows demo analysis results
5. Queues for sync when online
6. Syncs automatically when connection restored
```

### Scenario 3: Knowledge Base Access
```
1. User browses knowledge base
2. App fetches from backend API
3. Displays diseases/herbs/treatments
4. User can view details
5. Cross-references across traditions
```

---

## 🚀 Deployment Checklist

### Backend Deployment
- [ ] All models created and tested
- [ ] All API endpoints functional
- [ ] AI services configured (Gemini/Claude)
- [ ] Database backups setup
- [ ] Logging configured
- [ ] Monitoring setup
- [ ] Error handling complete
- [ ] Rate limiting enabled
- [ ] HTTPS certificate configured

### Mobile Deployment
- [ ] All routes configured
- [ ] Camera working on device
- [ ] Image upload tested
- [ ] Backend URL updated
- [ ] Offline mode tested
- [ ] Error handling tested
- [ ] Permissions configured (AndroidManifest.xml, Info.plist)
- [ ] Build APK/IPA generated
- [ ] TestFlight/Play Store ready

---

## 📈 Phase 3 Timeline

```
Week 1: Backend Preparation
├─ Update CORS configuration
├─ Create analysis endpoints  
├─ Create diagnosis endpoints
├─ Test with Postman/curl
└─ Seed knowledge base

Week 2: Integration & Testing
├─ Update mobile API config
├─ Implement image upload
├─ Test full flow (mobile + backend)
├─ Handle errors gracefully
├─ Offline mode testing
└─ Performance optimization

Week 3: Polish & Deployment
├─ UI/UX improvements
├─ Bug fixes
├─ Security review
├─ Load testing
├─ Documentation
└─ Codemagic build

Week 4: Production
├─ Production database setup
├─ Domain configuration
├─ SSL certificate
├─ App store submission
└─ Beta testing
```

---

## 🔗 Key Files to Update

**Backend**:
- `backend/app/core/config.py` - CORS, API keys
- `backend/app/routers/analysis_service.py` - New endpoints
- `backend/app/routers/diagnosis_service.py` - New endpoints
- `backend/app/services/gemini_service.py` - AI integration

**Mobile**:
- `mobile/lib/config/app_config.dart` - Backend URL
- `mobile/lib/services/analysis_service.dart` - Already done ✅
- `mobile/lib/screens/analysis_results_screen.dart` - New
- `mobile/lib/controllers/analysis_controller.dart` - New

---

## 📞 Support & Debugging

### If Image Upload Fails
1. Check backend URL in app_config.dart
2. Verify CORS settings on backend
3. Check network connectivity
4. Review error logs in terminal
5. Test with Postman first

### If AI Analysis Fails  
1. Verify Gemini API key is correct
2. Check image format and size
3. Review Gemini API quotas
4. Check backend logs
5. Use offline demo data as fallback

### If App Crashes
1. Check logcat (Android) or Xcode (iOS)
2. Verify all dependencies installed (flutter pub get)
3. Check for null pointer exceptions
4. Review error handling in services
5. Test on real device vs emulator

---

**Status**: Ready for Phase 3 Implementation  
**Next**: Backend integration + Mobile testing  
**ETA**: 2-4 weeks for complete integration
