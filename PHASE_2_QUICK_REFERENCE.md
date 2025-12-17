# 📱 Phase 2 Quick Start Reference
## All Copy-Paste Code Ready to Go!

---

## 🚀 First 30 Minutes Setup

### Step 1: Get Latest Dependencies
```bash
cd mobile/
flutter pub get
```

### Step 2: Create Directory Structure
```bash
mkdir -p lib/services lib/controllers lib/screens/health lib/database lib/utils lib/widgets lib/models
```

### Step 3: Update Android Permissions
Add to `android/app/src/main/AndroidManifest.xml` (inside `<manifest>` tag):

```xml
<!-- Camera & Microphone -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Bluetooth -->
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />

<!-- Sensors -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.BODY_SENSORS" />

<!-- Storage & Network -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

### Step 4: Update iOS Permissions
Add to `ios/Runner/Info.plist` (inside `<dict>` tag):

```xml
<key>NSCameraUsageDescription</key>
<string>We need camera access to analyze your health using AI.</string>
<key>NSMicrophoneUsageDescription</key>
<string>We need microphone to record heart and breathing sounds.</string>
<key>NSBluetoothPeripheralUsageDescription</key>
<string>We need Bluetooth to connect to your wearable devices.</string>
<key>NSBluetoothAlwaysAndWhenInUseUsageDescription</key>
<string>Bluetooth is needed to sync your health data continuously.</string>
```

---

## 📝 File Creation Checklist

Use this to track which files you've created:

### Week 1: Camera
- [ ] `lib/services/camera_service.dart` - Camera controller
- [ ] `lib/models/image_analysis.dart` - Image data model
- [ ] `lib/screens/health/camera_preview_screen.dart` - Camera UI
- [ ] `lib/utils/image_validator.dart` - Image validation

### Week 2: Sensors & Wearables
- [ ] `lib/services/sensor_service.dart` - Phone sensors (audio, tremor)
- [ ] `lib/services/wearable_service.dart` - Bluetooth wearables
- [ ] `lib/database/app_database.dart` - SQLite setup
- [ ] `lib/services/sync_service.dart` - Backend sync

### Week 3: UI & Integration
- [ ] `lib/screens/health/health_dashboard.dart` - Main dashboard
- [ ] `lib/controllers/health_controller.dart` - GetX controller
- [ ] `lib/widgets/vital_signs_card.dart` - Reusable card widget
- [ ] Testing & integration complete

---

## 💡 Quick Code Snippets

### Initialize Camera on App Start

```dart
// In your main.dart or app startup
import 'lib/services/camera_service.dart';

final cameraService = CameraService();
await cameraService.initializeCamera();
```

### Capture Tongue Image

```dart
File? tongueImage = await cameraService.captureTongueImage();
if (tongueImage != null) {
  print('✅ Image saved: ${tongueImage.path}');
}
```

### Record Heart Sound

```dart
import 'lib/services/sensor_service.dart';

final sensorService = SensorService();
File? audioFile = await sensorService.recordHeartSound(
  duration: Duration(seconds: 30),
);
```

### Get Wearable Health Data

```dart
import 'lib/services/wearable_service.dart';

final wearableService = WearableService();
final healthData = await wearableService.getHealthData();
print('❤️ Heart Rate: ${healthData?.heartRate}');
print('🫁 SpO2: ${healthData?.spo2}%');
```

### Save to Local Database

```dart
import 'lib/database/app_database.dart';

final db = AppDatabase();

// Save vital signs
await db.insertVitalSigns(
  heartRate: 72.0,
  spo2: 98.0,
  temperature: 37.0,
  systolicBP: 120.0,
  diastolicBP: 80.0,
);
```

### Sync All Data

```dart
import 'lib/services/sync_service.dart';

final syncService = SyncService();
final result = await syncService.syncAllData(patientId: 1);

if (result.success) {
  print('✅ Synced ${result.imagesSynced} images');
}
```

### Display Health Dashboard

```dart
// In your router
GetPage(
  name: '/health-dashboard',
  page: () => HealthDashboardScreen(),
),
```

---

## 🔧 Troubleshooting

### Camera Permission Denied
**Problem**: `Camera initialization error: Permission denied`

**Solution**:
```dart
// Add permission check
import 'package:permission_handler/permission_handler.dart';

if (await Permission.camera.isDenied) {
  await Permission.camera.request();
}
```

### Bluetooth Not Found
**Problem**: No devices found during scan

**Solution**:
```dart
// Check Bluetooth is enabled
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

bool isBluetoothOn = await FlutterBluePlus.instance.isOn;
if (!isBluetoothOn) {
  print('❌ Enable Bluetooth on your phone');
}
```

### Database Error: Table Already Exists
**Problem**: `Database table already exists`

**Solution**:
```dart
// Safely drop and recreate (dev only)
await db.database.execute('DROP TABLE IF EXISTS images');
```

### Image Upload Fails
**Problem**: `Error uploading to backend`

**Solution**:
```dart
// Check backend is running
// Check patient_id is correct
// Check image file exists
print('Image path: ${image.path}');
print('File exists: ${await File(image.path).exists()}');
```

---

## 📊 Expected Results After Phase 2

### Camera Module
```
✅ Capture 4 image types (tongue, eye, face, skin)
✅ Validate image quality (brightness, resolution)
✅ Store locally with metadata
✅ Upload to backend with analysis
```

### Sensors Module
```
✅ Record audio (heart & breathing sounds)
✅ Analyze tremor via gyroscope
✅ Capture accelerometer data
✅ All data saved locally
```

### Wearable Integration
```
✅ Scan for Bluetooth devices
✅ Connect to smartwatch/fitness band
✅ Fetch real-time health metrics
✅ Continuous background sync
```

### Data Management
```
✅ 1000+ local records stored
✅ Automatic offline-first saving
✅ Batch sync when online
✅ 100% data integrity
```

---

## 🎯 Daily Goals Template

Copy this to track daily progress:

```
📅 DAY [X] - [DATE]

Morning Tasks:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

Afternoon Tasks:
- [ ] Task 4
- [ ] Task 5

Testing:
- [ ] Tested on device
- [ ] No crashes
- [ ] Data saves correctly

✅ Day Complete: [TIME] hours

Notes:
[Add any blockers or notes]
```

---

## 🚨 Critical Dependencies

**Must have these packages:**

```yaml
dependencies:
  camera: ^0.10.8              # Camera capture
  flutter_blue_plus: ^1.30.0   # Bluetooth
  sensors_plus: ^2.0.0         # Phone sensors
  record: ^5.0.1               # Audio recording
  health: ^9.0.0               # Health data
  sqflite: ^2.3.0              # Local database
  dio: ^5.3.1                  # API uploads
  permission_handler: ^11.4.3  # Permissions
```

**Check with:**
```bash
flutter pub get
flutter doctor
```

---

## 📞 Quick Support

### Backend API Endpoints (Reference)

```
POST /api/v1/analysis/TONGUE       # Upload tongue image
POST /api/v1/analysis/EYE          # Upload eye image
POST /api/v1/analysis/FACE         # Upload face image
POST /api/v1/analysis/SKIN         # Upload skin image
POST /api/v1/sensor-data/upload    # Upload sensor readings
POST /api/v1/audio/heartbeat       # Upload heart sound
POST /api/v1/vital-signs/record    # Record vital signs
POST /api/v1/wearable/sync         # Sync wearable data
```

### Common Backend URLs
- Local Dev: `http://localhost:8000/api/v1`
- Staging: `https://staging-api.avicenna.com/api/v1`
- Production: `https://api.avicenna.com/api/v1`

---

## 🎓 Learning Resources

- [Flutter Camera Plugin](https://pub.dev/packages/camera)
- [Flutter Bluetooth](https://pub.dev/packages/flutter_blue_plus)
- [Sensors Plus](https://pub.dev/packages/sensors_plus)
- [SQLite Flutter](https://pub.dev/packages/sqflite)
- [Dio HTTP Client](https://pub.dev/packages/dio)

---

## ✅ Sign Off Checklist

- [ ] All permissions added to Android
- [ ] All permissions added to iOS
- [ ] Dependencies installed (`flutter pub get`)
- [ ] First test run successful
- [ ] Camera working
- [ ] Sensor data collecting
- [ ] Local database storing data
- [ ] Sync uploading to backend
- [ ] UI showing health data
- [ ] No crashes in 1-hour usage

---

**You're ready to build! Start with the Day 1 setup.** 🚀
