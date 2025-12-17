# 📱 Phase 2 - Mobile App Implementation Guide
## Complete Mobile Sensor Integration & Data Collection

**Duration**: 2-3 weeks  
**Priority**: HIGH  
**Status**: Ready to Begin  
**Target**: Full sensor integration + real-time data collection

---

## 🎯 Phase 2 Objectives

```
✅ Camera Module (4 image types)
  ├─ Tongue capture & analysis
  ├─ Eye capture & analysis
  ├─ Face capture & analysis
  └─ Skin capture & analysis

✅ Wearable Integration (Bluetooth)
  ├─ Apple Watch connection
  ├─ Fitbit sync
  ├─ Xiaomi Mi Band
  └─ Generic Wear OS devices

✅ Phone Sensors
  ├─ Gyroscope (tremor detection)
  ├─ Accelerometer (movement)
  ├─ Microphone (heart/breathing sounds)
  └─ Thermometer (if available)

✅ Data Management
  ├─ Local storage (SQLite)
  ├─ Offline validation
  ├─ Batch sync to backend
  └─ Real-time sync capability

✅ User Interface
  ├─ Camera preview
  ├─ Health data dashboard
  ├─ Wearable status
  ├─ Analysis results display
  └─ Navigation between modules
```

---

## 📋 Week-by-Week Breakdown

### Week 1: Camera & File Handling

#### Day 1: Setup & Dependencies
- [ ] Add camera packages to pubspec.yaml
- [ ] Add permissions (Android & iOS)
- [ ] Create camera service structure
- [ ] Test camera access

#### Day 2-3: Camera Service
- [ ] Create `camera_service.dart`
- [ ] Implement `captureTongueImage()`
- [ ] Implement `captureEyeImage()`
- [ ] Implement `captureFaceImage()`
- [ ] Implement `captureSkinImage()`

#### Day 4: Camera UI
- [ ] Create camera preview screen
- [ ] Create image capture controls
- [ ] Add image quality indicators
- [ ] Add feedback & instructions

#### Day 5: Image Validation
- [ ] Create image validation logic
- [ ] Verify image quality (brightness, focus)
- [ ] Verify image contains required elements
- [ ] Create retake mechanism

---

### Week 2: Wearables & Phone Sensors

#### Day 1-2: Wearable Integration
- [ ] Create `wearable_service.dart`
- [ ] Implement Bluetooth discovery
- [ ] Implement device pairing
- [ ] Test with real wearable (if available)

#### Day 3-4: Phone Sensors
- [ ] Create `sensor_service.dart` for phone sensors
- [ ] Implement gyroscope reading (tremor)
- [ ] Implement accelerometer (movement)
- [ ] Implement microphone access

#### Day 5: Audio Recording
- [ ] Create audio recording service
- [ ] Record heart sounds (15-30 seconds)
- [ ] Record breathing sounds
- [ ] Audio quality validation

---

### Week 3: Data Sync & Integration

#### Day 1-2: Local Storage
- [ ] Create SQLite database structure
- [ ] Implement local data persistence
- [ ] Create sync mechanism
- [ ] Test offline functionality

#### Day 3-4: API Integration
- [ ] Connect to backend APIs
- [ ] Batch upload sensor data
- [ ] Batch upload images
- [ ] Handle sync errors & retries

#### Day 5: Testing & Polish
- [ ] Full integration testing
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Documentation

---

## 🔧 Implementation Details

### New Dependencies for pubspec.yaml

```yaml
dependencies:
  # Camera & Image Processing
  camera: ^0.10.8
  image_picker: ^1.0.4
  image: ^4.0.17
  flutter_vision: ^0.7.0
  
  # Sensors & Device Data
  sensors_plus: ^2.0.0           # Accelerometer, Gyroscope
  health: ^9.0.0                 # Health data (heart rate, steps)
  flutter_blue_plus: ^1.30.0     # Bluetooth for wearables
  
  # Audio Processing
  record: ^5.0.1                 # Audio recording
  audio_waveforms: ^1.0.4        # Waveform visualization
  flutter_sound: ^9.2.13
  
  # Real-time Capabilities
  web_socket_channel: ^2.4.0
  
  # Data Visualization
  fl_chart: ^0.65.0
  syncfusion_flutter_charts: ^25.1.35
  
  # Storage & Database (Already present)
  sqflite: ^2.3.0
  
  # Serialization (Already present)
  json_serializable: ^6.7.1
  
  # Permissions
  permission_handler: ^11.4.3
  
  # Device Info
  device_info_plus: ^9.0.0
```

---

## 📱 New Mobile Architecture

### Directory Structure to Create

```
mobile/lib/
├── services/
│   ├── camera_service.dart              # NEW
│   ├── sensor_service.dart              # NEW
│   ├── wearable_service.dart            # NEW
│   ├── audio_service.dart               # NEW
│   ├── bluetooth_manager.dart           # NEW
│   ├── storage_service.dart             # NEW
│   └── sync_service.dart                # NEW
│
├── controllers/
│   ├── camera_controller.dart           # NEW
│   ├── health_controller.dart           # NEW
│   ├── sensor_controller.dart           # NEW
│   ├── wearable_controller.dart         # NEW
│   └── sync_controller.dart             # NEW
│
├── screens/
│   └── health/
│       ├── tongue_analysis_screen.dart  # NEW
│       ├── eye_analysis_screen.dart     # NEW
│       ├── face_analysis_screen.dart    # NEW
│       ├── skin_analysis_screen.dart    # NEW
│       ├── vital_signs_screen.dart      # NEW
│       ├── audio_analysis_screen.dart   # NEW
│       ├── wearable_status_screen.dart  # NEW
│       ├── camera_preview_screen.dart   # NEW
│       └── health_dashboard.dart        # NEW
│
├── models/
│   ├── sensor_data.dart                 # NEW
│   ├── image_analysis.dart              # NEW
│   ├── vital_signs.dart                 # NEW
│   ├── audio_data.dart                  # NEW
│   ├── wearable_device.dart             # NEW
│   └── diagnosis_result.dart            # NEW
│
├── widgets/
│   ├── camera_preview_widget.dart       # NEW
│   ├── sensor_chart_widget.dart         # NEW
│   ├── vital_signs_card.dart            # NEW
│   ├── wearable_status_widget.dart      # NEW
│   ├── permission_request_widget.dart   # NEW
│   └── analysis_result_widget.dart      # NEW
│
├── database/
│   ├── app_database.dart                # NEW
│   ├── sensor_dao.dart                  # NEW
│   ├── image_dao.dart                   # NEW
│   └── vital_signs_dao.dart             # NEW
│
├── utils/
│   ├── image_validator.dart             # NEW
│   ├── permission_helper.dart           # NEW
│   ├── sensor_processor.dart            # NEW
│   └── audio_processor.dart             # NEW
│
└── [existing files]
```

---

## 🎥 Camera Service Implementation

```dart
// mobile/lib/services/camera_service.dart

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'dart:io';

enum ImageAnalysisType { TONGUE, EYE, FACE, SKIN }

class CameraService {
  static final CameraService _instance = CameraService._internal();
  
  factory CameraService() {
    return _instance;
  }
  
  CameraService._internal();
  
  late CameraController _controller;
  List<CameraDescription>? cameras;
  
  /// Initialize camera
  Future<void> initializeCamera() async {
    try {
      cameras = await availableCameras();
      if (cameras!.isNotEmpty) {
        _controller = CameraController(
          cameras![0], // Front camera
          ResolutionPreset.high,
        );
        await _controller.initialize();
      }
    } catch (e) {
      print('Camera initialization error: $e');
      rethrow;
    }
  }
  
  /// Capture tongue image
  Future<File?> captureTongueImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.TONGUE,
      instructions: 'পুরো জিহ্বা দৃশ্যমান রাখুন\nTake clear image of entire tongue\nEnsure good lighting',
    );
  }
  
  /// Capture eye image
  Future<File?> captureEyeImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.EYE,
      instructions: 'Both eyes fully visible\nTake clear, front-facing image\nNatural lighting preferred',
    );
  }
  
  /// Capture face image
  Future<File?> captureFaceImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.FACE,
      instructions: 'Full frontal face view\nNeutral expression\nGood lighting, no shadows',
    );
  }
  
  /// Capture skin image
  Future<File?> captureSkinImage({required String bodyPart}) async {
    return _captureImage(
      imageType: ImageAnalysisType.SKIN,
      instructions: 'Close-up of $bodyPart\nGood lighting\nClear skin surface visible',
    );
  }
  
  Future<File?> _captureImage({
    required ImageAnalysisType imageType,
    required String instructions,
  }) async {
    try {
      if (!_controller.value.isInitialized) {
        await initializeCamera();
      }
      
      final image = await _controller.takePicture();
      
      // Validate image quality
      bool isValid = await _validateImageQuality(File(image.path), imageType);
      
      if (!isValid) {
        // Show error - image not suitable
        throw Exception('Image quality not sufficient. Please retake.');
      }
      
      return File(image.path);
    } catch (e) {
      print('Image capture error: $e');
      rethrow;
    }
  }
  
  /// Validate image quality
  Future<bool> _validateImageQuality(File imageFile, ImageAnalysisType type) async {
    try {
      // Check file size (100KB - 10MB)
      int fileSize = await imageFile.length();
      if (fileSize < 100000 || fileSize > 10000000) {
        return false;
      }
      
      // Check image dimensions using Image package
      final imageBytes = await imageFile.readAsBytes();
      // Additional validations can be added
      
      return true;
    } catch (e) {
      print('Image validation error: $e');
      return false;
    }
  }
  
  CameraController get controller => _controller;
  
  Future<void> dispose() async {
    await _controller.dispose();
  }
}
```

---

## 📊 Sensor Service Implementation

```dart
// mobile/lib/services/sensor_service.dart

import 'package:sensors_plus/sensors_plus.dart';
import 'package:record/record.dart';

class SensorService {
  static final SensorService _instance = SensorService._internal();
  
  factory SensorService() {
    return _instance;
  }
  
  SensorService._internal();
  
  final _record = AudioRecorder();
  
  /// Monitor tremor using gyroscope
  Future<void> monitorTremor({
    required Duration duration,
    required Function(TremorData) onData,
  }) async {
    try {
      final stopwatch = Stopwatch()..start();
      final tremorReadings = <double>[];
      
      gyroscopeEvents.listen((GyroscopeEvent event) {
        // Calculate magnitude of angular velocity
        double magnitude = (event.x.abs() + event.y.abs() + event.z.abs()) / 3;
        tremorReadings.add(magnitude);
        
        if (stopwatch.elapsed >= duration) {
          stopwatch.stop();
          
          // Analyze tremor data
          TremorData data = _analyzeTremor(tremorReadings);
          onData(data);
        }
      });
    } catch (e) {
      print('Tremor monitoring error: $e');
    }
  }
  
  /// Record heart sounds
  Future<File?> recordHeartSound({required Duration duration}) async {
    try {
      if (await _record.hasPermission()) {
        final String path = '/path/to/heart_sound_${DateTime.now().millisecondsSinceEpoch}.wav';
        
        await _record.start(
          path: path,
          encoder: AudioEncoder.wav,
        );
        
        await Future.delayed(duration);
        await _record.stop();
        
        return File(path);
      }
    } catch (e) {
      print('Heart sound recording error: $e');
    }
    return null;
  }
  
  /// Record breathing sounds
  Future<File?> recordBreathingSound({required Duration duration}) async {
    try {
      if (await _record.hasPermission()) {
        final String path = '/path/to/breathing_sound_${DateTime.now().millisecondsSinceEpoch}.wav';
        
        await _record.start(
          path: path,
          encoder: AudioEncoder.wav,
        );
        
        await Future.delayed(duration);
        await _record.stop();
        
        return File(path);
      }
    } catch (e) {
      print('Breathing sound recording error: $e');
    }
    return null;
  }
  
  /// Analyze tremor data
  TremorData _analyzeTremor(List<double> readings) {
    if (readings.isEmpty) return TremorData(severity: 'none', confidence: 0.0);
    
    double average = readings.reduce((a, b) => a + b) / readings.length;
    double maxValue = readings.reduce((a, b) => a > b ? a : b);
    
    String severity;
    if (average < 0.1) severity = 'none';
    else if (average < 0.5) severity = 'mild';
    else if (average < 1.0) severity = 'moderate';
    else severity = 'severe';
    
    return TremorData(severity: severity, confidence: 0.85);
  }
}

class TremorData {
  final String severity;
  final double confidence;
  
  TremorData({required this.severity, required this.confidence});
}
```

---

## 📡 Wearable Integration Service

```dart
// mobile/lib/services/wearable_service.dart

import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:health/health.dart';

class WearableService {
  static final WearableService _instance = WearableService._internal();
  
  factory WearableService() {
    return _instance;
  }
  
  WearableService._internal();
  
  final FlutterBluePlus _flutterBlue = FlutterBluePlus.instance;
  Health health = Health();
  
  List<HealthDataType> get _types => [
    HealthDataType.HEART_RATE,
    HealthDataType.BLOOD_OXYGEN,
    HealthDataType.BLOOD_PRESSURE_SYSTOLIC,
    HealthDataType.BLOOD_PRESSURE_DIASTOLIC,
    HealthDataType.BODY_TEMPERATURE,
  ];
  
  /// Scan for wearable devices
  Future<List<ScanResult>> scanForDevices() async {
    try {
      await _flutterBlue.startScan(timeout: Duration(seconds: 4));
      
      List<ScanResult> results = [];
      _flutterBlue.scanResults.listen((result) {
        results.add(result);
      });
      
      await Future.delayed(Duration(seconds: 5));
      await _flutterBlue.stopScan();
      
      return results;
    } catch (e) {
      print('Scan error: $e');
      rethrow;
    }
  }
  
  /// Connect to wearable device
  Future<bool> connectToDevice(BluetoothDevice device) async {
    try {
      await device.connect();
      return true;
    } catch (e) {
      print('Connection error: $e');
      return false;
    }
  }
  
  /// Get health data from wearable
  Future<VitalSignsData?> getHealthData() async {
    try {
      final results = await health.getHealthDataFromTypes(
        types: _types,
        startTime: DateTime.now().subtract(Duration(hours: 24)),
        endTime: DateTime.now(),
      );
      
      if (results.isEmpty) return null;
      
      return _parseHealthData(results);
    } catch (e) {
      print('Health data fetch error: $e');
      return null;
    }
  }
  
  VitalSignsData _parseHealthData(List<HealthDataPoint> data) {
    return VitalSignsData(
      heartRate: _extractValue(data, 'HEART_RATE'),
      spo2: _extractValue(data, 'BLOOD_OXYGEN'),
      systolicBP: _extractValue(data, 'BLOOD_PRESSURE_SYSTOLIC'),
      diastolicBP: _extractValue(data, 'BLOOD_PRESSURE_DIASTOLIC'),
      temperature: _extractValue(data, 'BODY_TEMPERATURE'),
      timestamp: DateTime.now(),
    );
  }
  
  double _extractValue(List<HealthDataPoint> data, String type) {
    try {
      final item = data.firstWhere((d) => d.typeString == type);
      return item.value.toDouble();
    } catch (e) {
      return 0.0;
    }
  }
}

class VitalSignsData {
  final double heartRate;
  final double spo2;
  final double systolicBP;
  final double diastolicBP;
  final double temperature;
  final DateTime timestamp;
  
  VitalSignsData({
    required this.heartRate,
    required this.spo2,
    required this.systolicBP,
    required this.diastolicBP,
    required this.temperature,
    required this.timestamp,
  });
}
```

---

## 💾 Local Storage (SQLite)

```dart
// mobile/lib/database/app_database.dart

import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class AppDatabase {
  static final AppDatabase _instance = AppDatabase._internal();
  static Database? _database;
  
  factory AppDatabase() {
    return _instance;
  }
  
  AppDatabase._internal();
  
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }
  
  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'avicenna_health.db');
    
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }
  
  Future<void> _onCreate(Database db, int version) async {
    // Sensor Data
    await db.execute('''
      CREATE TABLE sensor_data (
        id INTEGER PRIMARY KEY,
        sensor_type TEXT,
        raw_value TEXT,
        timestamp INTEGER,
        synced INTEGER DEFAULT 0
      )
    ''');
    
    // Image Data
    await db.execute('''
      CREATE TABLE images (
        id INTEGER PRIMARY KEY,
        image_type TEXT,
        image_path TEXT,
        timestamp INTEGER,
        analysis_status TEXT,
        synced INTEGER DEFAULT 0
      )
    ''');
    
    // Vital Signs
    await db.execute('''
      CREATE TABLE vital_signs (
        id INTEGER PRIMARY KEY,
        heart_rate REAL,
        spo2 REAL,
        body_temp REAL,
        systolic_bp REAL,
        diastolic_bp REAL,
        timestamp INTEGER,
        synced INTEGER DEFAULT 0
      )
    ''');
    
    // Audio Data
    await db.execute('''
      CREATE TABLE audio_data (
        id INTEGER PRIMARY KEY,
        audio_type TEXT,
        audio_path TEXT,
        timestamp INTEGER,
        synced INTEGER DEFAULT 0
      )
    ''');
  }
}
```

---

## 🔄 Sync Service

```dart
// mobile/lib/services/sync_service.dart

import 'package:dio/dio.dart';

class SyncService {
  final Dio _dio = Dio();
  static const String BASE_URL = 'http://your-backend.com/api/v1';
  
  /// Sync all offline data to backend
  Future<bool> syncAllData(int patientId) async {
    try {
      // Get all unsync data
      final sensorData = await _getSensorData();
      final images = await _getImages();
      final vitals = await _getVitals();
      
      // Upload sensor data
      if (sensorData.isNotEmpty) {
        await _uploadSensorData(patientId, sensorData);
      }
      
      // Upload images
      if (images.isNotEmpty) {
        await _uploadImages(patientId, images);
      }
      
      // Upload vital signs
      if (vitals.isNotEmpty) {
        await _uploadVitals(patientId, vitals);
      }
      
      return true;
    } catch (e) {
      print('Sync error: $e');
      return false;
    }
  }
  
  Future<void> _uploadSensorData(int patientId, List data) async {
    await _dio.post(
      '$BASE_URL/sensor-data/upload',
      data: {
        'patient_id': patientId,
        'sensor_readings': data,
      },
    );
  }
  
  Future<void> _uploadImages(int patientId, List images) async {
    for (var image in images) {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'image_type': image['type'],
        'file': await MultipartFile.fromFile(image['path']),
      });
      
      await _dio.post('$BASE_URL/analysis/${image['type']}', data: formData);
    }
  }
  
  Future<void> _uploadVitals(int patientId, List vitals) async {
    await _dio.post(
      '$BASE_URL/vital-signs/record',
      data: {
        'patient_id': patientId,
        'vitals': vitals,
      },
    );
  }
  
  Future<List> _getSensorData() async {
    // Query unsynced sensor data from database
    return [];
  }
  
  Future<List> _getImages() async {
    // Query unsynced images from database
    return [];
  }
  
  Future<List> _getVitals() async {
    // Query unsynced vitals from database
    return [];
  }
}
```

---

## 🎨 Camera Preview Screen

```dart
// mobile/lib/screens/health/camera_preview_screen.dart

import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:get/get.dart';
import '../../controllers/camera_controller.dart';

class CameraPreviewScreen extends StatefulWidget {
  final String analysisType; // tongue, eye, face, skin
  
  const CameraPreviewScreen({required this.analysisType});
  
  @override
  State<CameraPreviewScreen> createState() => _CameraPreviewScreenState();
}

class _CameraPreviewScreenState extends State<CameraPreviewScreen> {
  final CameraControllerX controller = Get.put(CameraControllerX());
  
  @override
  void initState() {
    super.initState();
    controller.initializeCamera();
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Capture ${widget.analysisType.capitalizeFirst}'),
        backgroundColor: Colors.green[700],
      ),
      body: Stack(
        children: [
          // Camera Preview
          FutureBuilder<void>(
            future: controller.initializeCamera(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                return CameraPreview(controller.cameraService.controller);
              }
              return Center(child: CircularProgressIndicator());
            },
          ),
          
          // Instructions
          Positioned(
            top: 20,
            left: 20,
            right: 20,
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black54,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                _getInstructions(),
                style: TextStyle(color: Colors.white, fontSize: 14),
                textAlign: TextAlign.center,
              ),
            ),
          ),
          
          // Capture Button
          Positioned(
            bottom: 30,
            left: 0,
            right: 0,
            child: Center(
              child: ElevatedButton.icon(
                onPressed: () => controller.captureImage(widget.analysisType),
                icon: Icon(Icons.camera_alt),
                label: Text('Capture'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green,
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  String _getInstructions() {
    switch (widget.analysisType.toLowerCase()) {
      case 'tongue':
        return 'Show full tongue\nGood lighting required\nKeep mouth wide open';
      case 'eye':
        return 'Both eyes visible\nFront-facing view\nNatural expression';
      case 'face':
        return 'Full face visible\nNeutral expression\nGood lighting';
      case 'skin':
        return 'Close-up of skin area\nClear surface visible\nGood lighting';
      default:
        return 'Take clear image';
    }
  }
}
```

---

## 📊 Health Dashboard Screen

```dart
// mobile/lib/screens/health/health_dashboard.dart

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../controllers/health_controller.dart';
import '../../widgets/vital_signs_card.dart';

class HealthDashboardScreen extends StatefulWidget {
  @override
  State<HealthDashboardScreen> createState() => _HealthDashboardScreenState();
}

class _HealthDashboardScreenState extends State<HealthDashboardScreen> {
  final HealthController controller = Get.put(HealthController());
  
  @override
  void initState() {
    super.initState();
    controller.loadDashboardData();
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Health Dashboard'),
        backgroundColor: Colors.green[700],
        actions: [
          IconButton(
            icon: Icon(Icons.sync),
            onPressed: controller.syncData,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => controller.loadDashboardData(),
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Vital Signs Cards
              Text('Current Vitals', style: Theme.of(context).textTheme.headlineSmall),
              SizedBox(height: 12),
              Obx(() => GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                shrinkWrap: true,
                physics: NeverScrollableScrollPhysics(),
                children: [
                  VitalSignsCard(
                    title: 'Heart Rate',
                    value: '${controller.vitals.value?.heartRate.toStringAsFixed(0) ?? '--'}',
                    unit: 'bpm',
                    icon: Icons.favorite,
                    color: Colors.red,
                  ),
                  VitalSignsCard(
                    title: 'SpO2',
                    value: '${controller.vitals.value?.spo2.toStringAsFixed(0) ?? '--'}',
                    unit: '%',
                    icon: Icons.air,
                    color: Colors.blue,
                  ),
                  VitalSignsCard(
                    title: 'Temperature',
                    value: '${controller.vitals.value?.temperature.toStringAsFixed(1) ?? '--'}',
                    unit: '°C',
                    icon: Icons.local_fire_department,
                    color: Colors.orange,
                  ),
                  VitalSignsCard(
                    title: 'Blood Pressure',
                    value: '${controller.vitals.value?.systolicBP.toStringAsFixed(0) ?? '--'}/${controller.vitals.value?.diastolicBP.toStringAsFixed(0) ?? '--'}',
                    unit: 'mmHg',
                    icon: Icons.pulse_checker,
                    color: Colors.purple,
                  ),
                ],
              )),
              
              SizedBox(height: 24),
              
              // Heart Rate Chart
              Text('Heart Rate Trend (24h)', style: Theme.of(context).textTheme.headlineSmall),
              SizedBox(height: 12),
              _buildHeartRateChart(),
              
              SizedBox(height: 24),
              
              // Analysis Buttons
              Text('Health Analysis', style: Theme.of(context).textTheme.headlineSmall),
              SizedBox(height: 12),
              _buildAnalysisButtons(context),
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _buildHeartRateChart() {
    return Container(
      height: 200,
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: LineChart(
        LineChartData(
          lineBarsData: [
            LineChartBarData(
              spots: [
                FlSpot(0, 72),
                FlSpot(1, 75),
                FlSpot(2, 70),
                FlSpot(3, 78),
                FlSpot(4, 80),
                FlSpot(5, 76),
              ],
              isCurved: true,
              color: Colors.red,
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildAnalysisButtons(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _buildAnalysisButton('Tongue', Icons.image, () {
              Get.toNamed('/tongue_analysis');
            }),
            _buildAnalysisButton('Eye', Icons.remove_red_eye, () {
              Get.toNamed('/eye_analysis');
            }),
          ],
        ),
        SizedBox(height: 12),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _buildAnalysisButton('Face', Icons.face, () {
              Get.toNamed('/face_analysis');
            }),
            _buildAnalysisButton('Skin', Icons.healing, () {
              Get.toNamed('/skin_analysis');
            }),
          ],
        ),
      ],
    );
  }
  
  Widget _buildAnalysisButton(String title, IconData icon, VoidCallback onTap) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: EdgeInsets.all(16),
          margin: EdgeInsets.symmetric(horizontal: 6),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8),
            color: Colors.green[50],
            border: Border.all(color: Colors.green),
          ),
          child: Column(
            children: [
              Icon(icon, size: 32, color: Colors.green),
              SizedBox(height: 8),
              Text(title, style: TextStyle(fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

## 🗂️ Controllers Structure

```dart
// mobile/lib/controllers/health_controller.dart

import 'package:get/get.dart';
import '../models/vital_signs.dart';
import '../services/wearable_service.dart';
import '../services/sync_service.dart';

class HealthController extends GetxController {
  final WearableService wearableService = WearableService();
  final SyncService syncService = SyncService();
  
  var vitals = Rxn<VitalSignsData>();
  var isLoading = false.obs;
  
  /// Load dashboard data
  Future<void> loadDashboardData() async {
    try {
      isLoading.value = true;
      
      // Get latest vitals from wearable
      final data = await wearableService.getHealthData();
      if (data != null) {
        vitals.value = data;
      }
    } catch (e) {
      print('Error loading data: $e');
      Get.snackbar('Error', 'Failed to load health data');
    } finally {
      isLoading.value = false;
    }
  }
  
  /// Sync all data to backend
  Future<void> syncData() async {
    try {
      isLoading.value = true;
      int patientId = 1; // Get from auth
      
      bool success = await syncService.syncAllData(patientId);
      
      if (success) {
        Get.snackbar('Success', 'Data synced successfully');
      }
    } catch (e) {
      Get.snackbar('Error', 'Failed to sync data');
    } finally {
      isLoading.value = false;
    }
  }
}
```

---

## ✅ Phase 2 Checklist

### Week 1: Camera
- [ ] Add camera package
- [ ] Request camera permissions
- [ ] Create camera service
- [ ] Implement capture functions
- [ ] Add image validation
- [ ] Create camera UI

### Week 2: Sensors
- [ ] Add health package
- [ ] Add bluetooth package
- [ ] Create wearable service
- [ ] Create sensor service
- [ ] Implement audio recording
- [ ] Add permission handlers

### Week 3: Integration
- [ ] Create SQLite database
- [ ] Create sync service
- [ ] Implement batch upload
- [ ] Create health dashboard
- [ ] Test full workflow
- [ ] Performance optimization

---

## 🎯 Success Criteria

✅ Camera captures all 4 image types
✅ Images upload to backend within 5 seconds
✅ Wearable connects and syncs data
✅ Phone sensors collect data in background
✅ Local storage works offline
✅ Batch sync on network available
✅ UI is responsive
✅ No crashes during normal usage
✅ All permissions working
✅ User can view dashboard

---

**Ready to start Phase 2? Let's build!** 🚀
