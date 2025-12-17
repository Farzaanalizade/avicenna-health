import 'package:get/get.dart';
import '../services/sensor_service.dart';
import '../services/wearable_service.dart';
import '../services/sync_service.dart';
import '../database/app_database.dart';

class HealthDataController extends GetxController {
  final _sensorService = SensorService();
  final _wearableService = WearableService();
  final _syncService = SyncService();
  final _database = AppDatabase();

  // Observable data
  var tremorSeverity = 'none'.obs;
  var heartRate = 0.0.obs;
  var bloodOxygen = 0.0.obs;
  var bodyTemperature = 0.0.obs;
  var isRecording = false.obs;
  var lastSyncTime = Rxn<DateTime>();
  var syncStatus = 'Not synced'.obs;

  /// Record heart sound
  Future<void> recordHeartSound() async {
    isRecording.value = true;
    try {
      final file = await _sensorService.recordHeartSound();
      if (file != null) {
        await _database.insertAudioRecord('heart', file.path, 30);
        Get.snackbar('✅ Success', 'Heart sound recorded');
      }
    } catch (e) {
      Get.snackbar('❌ Error', 'Failed to record: $e');
    } finally {
      isRecording.value = false;
    }
  }

  /// Record breathing sound
  Future<void> recordBreathingSound() async {
    isRecording.value = true;
    try {
      final file = await _sensorService.recordBreathingSound();
      if (file != null) {
        await _database.insertAudioRecord('breathing', file.path, 20);
        Get.snackbar('✅ Success', 'Breathing sound recorded');
      }
    } catch (e) {
      Get.snackbar('❌ Error', 'Failed to record: $e');
    } finally {
      isRecording.value = false;
    }
  }

  /// Analyze tremor
  Future<void> analyzeTremor() async {
    try {
      final analysis = await _sensorService.analyzeTremor();
      tremorSeverity.value = analysis.severity;
      await _database.insertSensorData(
        'tremor',
        analysis.averageMagnitude,
        DateTime.now().millisecondsSinceEpoch,
      );
    } catch (e) {
      Get.snackbar('❌ Error', 'Tremor analysis failed: $e');
    }
  }

  /// Get health metrics from wearable
  Future<void> fetchWearableMetrics() async {
    try {
      final metrics = await _wearableService.getHealthData();
      if (metrics != null) {
        heartRate.value = metrics.heartRate;
        bloodOxygen.value = metrics.spo2;
        bodyTemperature.value = metrics.temperature;

        await _database.insertVitalSigns(
          heartRate: metrics.heartRate,
          bpSystolic: metrics.systolicBP,
          bpDiastolic: metrics.diastolicBP,
          spo2: metrics.spo2,
          temperature: metrics.temperature,
        );

        Get.snackbar('✅ Success', 'Wearable data synced');
      }
    } catch (e) {
      Get.snackbar('❌ Error', 'Failed to fetch wearable data: $e');
    }
  }

  /// Sync data to backend
  Future<void> syncToBackend() async {
    try {
      syncStatus.value = 'Syncing...';

      // Use patient ID from auth (hardcoded for now)
      const int patientId = 1;

      final result = await _syncService.syncAllData(patientId);

      if (result.success) {
        lastSyncTime.value = DateTime.now();
        syncStatus.value =
            'Synced ${result.imagesSynced} images, ${result.sensorsSynced} sensors';
        Get.snackbar('✅ Success', syncStatus.value);
      } else {
        syncStatus.value = 'Sync failed: ${result.error}';
        Get.snackbar('❌ Error', syncStatus.value);
      }
    } catch (e) {
      syncStatus.value = 'Sync error: $e';
      Get.snackbar('❌ Error', syncStatus.value);
    }
  }
}

