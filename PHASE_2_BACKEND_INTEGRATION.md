# 🔗 Phase 2 - Backend Integration Guide
## How to Connect Mobile App to Your Existing Backend

Your backend (Phase 1) is already complete and tested! Now let's connect Phase 2 mobile to use it.

---

## 📡 Backend API Endpoints Reference

Your backend provides these endpoints (from Phase 1):

### Image Analysis Endpoints

```
POST /api/v1/analysis/TONGUE
Content-Type: multipart/form-data
Body:
  - image: <binary file>
  - patient_id: integer
Response: { analysis_result, mizaj_type, confidence }

POST /api/v1/analysis/EYE
Content-Type: multipart/form-data
Body:
  - image: <binary file>
  - patient_id: integer
Response: { eye_color, clarity, moisture_level, diagnosis }

POST /api/v1/analysis/FACE
Content-Type: multipart/form-data
Body:
  - image: <binary file>
  - patient_id: integer
Response: { complexion, wrinkles, age_estimate, health_score }

POST /api/v1/analysis/SKIN
Content-Type: multipart/form-data
Body:
  - image: <binary file>
  - patient_id: integer
Response: { skin_type, conditions, recommendations }
```

### Sensor Data Endpoints

```
POST /api/v1/sensor-data/upload
Content-Type: application/json
Body:
{
  "patient_id": 1,
  "sensor_readings": [
    {
      "sensor_type": "GYROSCOPE",
      "value": 0.45,
      "timestamp": 1704067200000
    },
    {
      "sensor_type": "ACCELEROMETER",
      "value": 9.81,
      "timestamp": 1704067205000
    }
  ]
}
Response: { success, ingested_count }
```

### Vital Signs Endpoints

```
POST /api/v1/vital-signs/record
Content-Type: application/json
Body:
{
  "patient_id": 1,
  "vitals": [
    {
      "heart_rate": 72.0,
      "blood_oxygen": 98.0,
      "body_temp": 37.0,
      "systolic_bp": 120,
      "diastolic_bp": 80,
      "timestamp": 1704067200000
    }
  ]
}
Response: { success, recorded_count }
```

### Audio Analysis Endpoints

```
POST /api/v1/audio/heartbeat
Content-Type: multipart/form-data
Body:
  - audio_file: <binary WAV file>
  - patient_id: integer
Response: { rhythm_type, bpm_detected, abnormalities }

POST /api/v1/audio/breathing
Content-Type: multipart/form-data
Body:
  - audio_file: <binary WAV file>
  - patient_id: integer
Response: { respiratory_rate, pattern, abnormalities }
```

### Diagnosis Endpoints

```
POST /api/v1/diagnosis/generate
Content-Type: application/json
Body:
{
  "patient_id": 1,
  "data_types": ["TONGUE", "EYE", "VITAL_SIGNS", "AUDIO"],
  "analysis_ids": [123, 124, 125, 126]
}
Response: {
  "diagnosis_id": "uuid",
  "mizaj_type": "string",
  "recommendations": "string",
  "modern_diagnosis": "string",
  "confidence": 0.85
}

GET /api/v1/diagnosis/{diagnosis_id}
Response: {
  "id": "uuid",
  "patient_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "mizaj_analysis": {...},
  "recommendations": [...]
}
```

---

## 🔌 How to Update Mobile Code for Your Backend

### Step 1: Update Base URL

In `lib/services/sync_service.dart` or create `lib/config/api_config.dart`:

```dart
// lib/config/api_config.dart

class ApiConfig {
  // Development
  static const String DEV_BASE_URL = 'http://192.168.1.100:8000/api/v1';
  
  // Staging
  static const String STAGING_BASE_URL = 'https://staging-api.example.com/api/v1';
  
  // Production
  static const String PROD_BASE_URL = 'https://api.example.com/api/v1';
  
  // Select based on environment
  static String get baseURL {
    const String environment = String.fromEnvironment('ENV', defaultValue: 'dev');
    
    switch (environment) {
      case 'prod':
        return PROD_BASE_URL;
      case 'staging':
        return STAGING_BASE_URL;
      default:
        return DEV_BASE_URL;
    }
  }
}
```

### Step 2: Update Sync Service

```dart
// lib/services/sync_service.dart

import 'package:dio/dio.dart';
import '../config/api_config.dart';
import '../database/app_database.dart';

class SyncService {
  final Dio _dio = Dio();
  final AppDatabase db = AppDatabase();
  
  String get baseURL => ApiConfig.baseURL;
  
  /// Sync tongue image to backend
  Future<Map?> uploadTongueImage(
    int patientId,
    File imageFile,
  ) async {
    try {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'file': await MultipartFile.fromFile(
          imageFile.path,
          filename: 'tongue_${DateTime.now().millisecondsSinceEpoch}.jpg',
        ),
      });
      
      Response response = await _dio.post(
        '$baseURL/analysis/TONGUE',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
          sendTimeout: Duration(seconds: 60),
        ),
      );
      
      print('✅ Tongue analysis: ${response.data}');
      return response.data;
    } catch (e) {
      print('❌ Tongue upload error: $e');
      return null;
    }
  }
  
  /// Sync eye image
  Future<Map?> uploadEyeImage(int patientId, File imageFile) async {
    return _uploadImageToBackend(patientId, imageFile, 'EYE');
  }
  
  /// Sync face image
  Future<Map?> uploadFaceImage(int patientId, File imageFile) async {
    return _uploadImageToBackend(patientId, imageFile, 'FACE');
  }
  
  /// Sync skin image
  Future<Map?> uploadSkinImage(int patientId, File imageFile) async {
    return _uploadImageToBackend(patientId, imageFile, 'SKIN');
  }
  
  /// Generic image upload
  Future<Map?> _uploadImageToBackend(
    int patientId,
    File imageFile,
    String analysisType,
  ) async {
    try {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'file': await MultipartFile.fromFile(
          imageFile.path,
          filename: '${analysisType.toLowerCase()}_${DateTime.now().millisecondsSinceEpoch}.jpg',
        ),
      });
      
      Response response = await _dio.post(
        '$baseURL/analysis/$analysisType',
        data: formData,
      );
      
      print('✅ $analysisType analysis complete');
      return response.data;
    } catch (e) {
      print('❌ $analysisType upload error: $e');
      return null;
    }
  }
  
  /// Upload vital signs to backend
  Future<bool> uploadVitalSigns(
    int patientId,
    double heartRate,
    double spo2,
    double temperature,
    double systolicBP,
    double diastolicBP,
  ) async {
    try {
      Response response = await _dio.post(
        '$baseURL/vital-signs/record',
        data: {
          'patient_id': patientId,
          'vitals': [
            {
              'heart_rate': heartRate,
              'blood_oxygen': spo2,
              'body_temp': temperature,
              'systolic_bp': systolicBP,
              'diastolic_bp': diastolicBP,
              'timestamp': DateTime.now().millisecondsSinceEpoch,
            }
          ],
        },
      );
      
      print('✅ Vital signs recorded');
      return response.data['success'] ?? false;
    } catch (e) {
      print('❌ Vital signs upload error: $e');
      return false;
    }
  }
  
  /// Upload sensor data to backend
  Future<bool> uploadSensorData(
    int patientId,
    List<Map<String, dynamic>> sensorReadings,
  ) async {
    try {
      Response response = await _dio.post(
        '$baseURL/sensor-data/upload',
        data: {
          'patient_id': patientId,
          'sensor_readings': sensorReadings,
        },
      );
      
      print('✅ ${sensorReadings.length} sensor readings uploaded');
      return response.data['success'] ?? false;
    } catch (e) {
      print('❌ Sensor data upload error: $e');
      return false;
    }
  }
  
  /// Upload heart sound to backend
  Future<Map?> uploadHeartSound(int patientId, File audioFile) async {
    try {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'audio_file': await MultipartFile.fromFile(
          audioFile.path,
          filename: 'heart_${DateTime.now().millisecondsSinceEpoch}.wav',
        ),
      });
      
      Response response = await _dio.post(
        '$baseURL/audio/heartbeat',
        data: formData,
      );
      
      print('✅ Heart sound analysis: ${response.data}');
      return response.data;
    } catch (e) {
      print('❌ Heart sound upload error: $e');
      return null;
    }
  }
  
  /// Upload breathing sound
  Future<Map?> uploadBreathingSound(int patientId, File audioFile) async {
    try {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'audio_file': await MultipartFile.fromFile(
          audioFile.path,
          filename: 'breathing_${DateTime.now().millisecondsSinceEpoch}.wav',
        ),
      });
      
      Response response = await _dio.post(
        '$baseURL/audio/breathing',
        data: formData,
      );
      
      print('✅ Breathing analysis: ${response.data}');
      return response.data;
    } catch (e) {
      print('❌ Breathing upload error: $e');
      return null;
    }
  }
  
  /// Generate diagnosis from all collected data
  Future<Map?> generateDiagnosis(
    int patientId,
    List<String> dataTypes,
    List<int> analysisIds,
  ) async {
    try {
      Response response = await _dio.post(
        '$baseURL/diagnosis/generate',
        data: {
          'patient_id': patientId,
          'data_types': dataTypes,
          'analysis_ids': analysisIds,
        },
      );
      
      print('✅ Diagnosis generated: ${response.data['mizaj_type']}');
      return response.data;
    } catch (e) {
      print('❌ Diagnosis generation error: $e');
      return null;
    }
  }
}
```

### Step 3: Update Controllers to Use Backend

```dart
// lib/controllers/health_controller.dart

import 'package:get/get.dart';
import '../services/sync_service.dart';
import '../services/camera_service.dart';
import '../services/wearable_service.dart';

class HealthController extends GetxController {
  final SyncService syncService = SyncService();
  final CameraService cameraService = CameraService();
  final WearableService wearableService = WearableService();
  
  var vitals = Rxn<HealthMetrics>();
  var analysisResults = Rxn<Map>();
  var isLoading = false.obs;
  
  int get patientId => 1; // Get from auth controller
  
  /// Capture and analyze tongue
  Future<void> captureTongueAnalysis() async {
    try {
      isLoading.value = true;
      
      // Capture image
      File? image = await cameraService.captureTongueImage();
      if (image == null) throw Exception('Image capture failed');
      
      // Upload to backend
      Map? result = await syncService.uploadTongueImage(patientId, image);
      
      if (result != null) {
        analysisResults.value = result;
        Get.snackbar('Success', 'Tongue analysis complete');
      }
    } finally {
      isLoading.value = false;
    }
  }
  
  /// Capture and analyze eye
  Future<void> captureEyeAnalysis() async {
    try {
      isLoading.value = true;
      
      File? image = await cameraService.captureEyeImage();
      if (image == null) throw Exception('Image capture failed');
      
      Map? result = await syncService.uploadEyeImage(patientId, image);
      
      if (result != null) {
        analysisResults.value = result;
        Get.snackbar('Success', 'Eye analysis complete');
      }
    } finally {
      isLoading.value = false;
    }
  }
  
  /// Record and sync vital signs
  Future<void> syncVitalSigns() async {
    try {
      isLoading.value = true;
      
      // Get vitals from wearable
      HealthMetrics? data = await wearableService.getHealthData();
      if (data == null) throw Exception('No vital signs available');
      
      vitals.value = data;
      
      // Upload to backend
      bool success = await syncService.uploadVitalSigns(
        patientId,
        data.heartRate,
        data.spo2,
        data.temperature,
        data.systolicBP,
        data.diastolicBP,
      );
      
      if (success) {
        Get.snackbar('Success', 'Vital signs synced');
      }
    } finally {
      isLoading.value = false;
    }
  }
  
  /// Record heart sound and analyze
  Future<void> recordHeartSound() async {
    try {
      isLoading.value = true;
      
      File? audioFile = await sensorService.recordHeartSound(
        duration: Duration(seconds: 30),
      );
      if (audioFile == null) throw Exception('Audio recording failed');
      
      Map? result = await syncService.uploadHeartSound(patientId, audioFile);
      
      if (result != null) {
        analysisResults.value = result;
        Get.snackbar('Success', 'Heart sound analyzed');
      }
    } finally {
      isLoading.value = false;
    }
  }
}
```

---

## 🧪 Testing Connection to Backend

### Test 1: Verify Backend is Running

```bash
# From backend directory
cd backend/
python run.py

# You should see:
# ✅ Backend running at http://localhost:8000
```

### Test 2: Test API Endpoint

```bash
# Test tongue analysis endpoint
curl -X POST http://localhost:8000/api/v1/analysis/TONGUE \
  -F "patient_id=1" \
  -F "file=@tongue_image.jpg"

# Should return:
# { "analysis_result": "...", "mizaj_type": "..." }
```

### Test 3: Test from Mobile App

```dart
// In your mobile app debug code
void testBackendConnection() async {
  final syncService = SyncService();
  
  // Test vital signs upload
  bool success = await syncService.uploadVitalSigns(
    1,      // patientId
    72.0,   // heartRate
    98.0,   // spo2
    37.0,   // temperature
    120.0,  // systolicBP
    80.0,   // diastolicBP
  );
  
  print(success ? '✅ Backend connection OK' : '❌ Backend connection failed');
}
```

---

## 🚀 Deployment Configuration

### Development (Local)
```dart
// lib/config/api_config.dart - USE THIS for testing
static const String DEV_BASE_URL = 'http://192.168.1.100:8000/api/v1';
```

### Production
```dart
// Update to your actual backend URL
static const String PROD_BASE_URL = 'https://api.avicenna-health.com/api/v1';
```

### Build with Environment

```bash
# Development build
flutter build apk --dart-define=ENV=dev

# Production build
flutter build apk --dart-define=ENV=prod
```

---

## ✅ Checklist: Backend Integration

- [ ] Backend is running and tested (Phase 1 complete)
- [ ] Backend API endpoints are documented
- [ ] Mobile app has API config file with correct URL
- [ ] Sync service is implemented with all upload functions
- [ ] Controllers call sync service after data collection
- [ ] Tested connection from mobile to backend
- [ ] Tested image upload works end-to-end
- [ ] Tested vital signs upload works
- [ ] Tested audio upload works
- [ ] Tested diagnosis generation works
- [ ] Error handling implemented for all API calls
- [ ] Offline queue and retry logic working
- [ ] Production URL configured
- [ ] SSL certificate handling (if https)

---

**Your Phase 2 mobile is now ready to talk to Phase 1 backend!** 🚀
