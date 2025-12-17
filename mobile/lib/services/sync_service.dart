import 'package:dio/dio.dart';
import '../database/app_database.dart';

class SyncService {
  final Dio _dio = Dio();
  final AppDatabase db = AppDatabase();

  static const String BASE_URL = 'http://localhost:8000/api/v1';

  /// Sync all unsynced data
  Future<SyncResult> syncAllData(int patientId) async {
    try {
      print('🔄 Starting sync process...');

      int imagesSynced = 0;
      int sensorsSynced = 0;

      // Sync images
      final images = await db.getUnsyncedData('images');
      for (var image in images) {
        try {
          await _uploadImage(patientId, image);
          await db.markAsSynced('images', image['id']);
          imagesSynced++;
        } catch (e) {
          print('❌ Image sync failed: $e');
        }
      }

      // Sync sensor data
      final sensors = await db.getUnsyncedData('sensor_data');
      if (sensors.isNotEmpty) {
        try {
          await _uploadSensorData(patientId, sensors);
          for (var sensor in sensors) {
            await db.markAsSynced('sensor_data', sensor['id']);
          }
          sensorsSynced = sensors.length;
        } catch (e) {
          print('❌ Sensor sync failed: $e');
        }
      }

      // Sync vital signs
      final vitals = await db.getUnsyncedData('vital_signs');
      if (vitals.isNotEmpty) {
        try {
          await _uploadVitalSigns(patientId, vitals);
          for (var vital in vitals) {
            await db.markAsSynced('vital_signs', vital['id']);
          }
        } catch (e) {
          print('❌ Vital signs sync failed: $e');
        }
      }

      print('✅ Sync complete: $imagesSynced images, $sensorsSynced sensors');

      return SyncResult(
        success: true,
        imagesSynced: imagesSynced,
        sensorsSynced: sensorsSynced,
      );
    } catch (e) {
      print('❌ Sync error: $e');
      return SyncResult(success: false, error: e.toString());
    }
  }

  /// Upload image to backend
  Future<void> _uploadImage(int patientId, Map image) async {
    try {
      FormData formData = FormData.fromMap({
        'patient_id': patientId,
        'image_type': image['image_type'],
        'file': await MultipartFile.fromFile(
          image['image_path'],
          filename:
              '${image['image_type']}_${DateTime.now().millisecondsSinceEpoch}.jpg',
        ),
      });

      await _dio.post(
        '$BASE_URL/analysis/${image['image_type']}',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
          sendTimeout: const Duration(seconds: 60),
        ),
      );

      print('✅ Image uploaded: ${image['image_type']}');
    } catch (e) {
      print('❌ Upload error: $e');
      rethrow;
    }
  }

  /// Upload sensor data
  Future<void> _uploadSensorData(int patientId, List sensors) async {
    try {
      await _dio.post(
        '$BASE_URL/sensor-data/upload',
        data: {
          'patient_id': patientId,
          'sensor_readings': sensors
              .map((s) => {
                    'sensor_type': s['sensor_type'],
                    'value': s['value'],
                    'timestamp': s['timestamp'],
                  })
              .toList(),
        },
      );

      print('✅ ${sensors.length} sensor readings uploaded');
    } catch (e) {
      print('❌ Sensor upload error: $e');
      rethrow;
    }
  }

  /// Upload vital signs
  Future<void> _uploadVitalSigns(int patientId, List vitals) async {
    try {
      await _dio.post(
        '$BASE_URL/vital-signs/upload',
        data: {
          'patient_id': patientId,
          'vital_signs': vitals
              .map((v) => {
                    'heart_rate': v['heart_rate'],
                    'spo2': v['spo2'],
                    'temperature': v['temperature'],
                    'systolic_bp': v['blood_pressure_systolic'],
                    'diastolic_bp': v['blood_pressure_diastolic'],
                    'timestamp': v['timestamp'],
                  })
              .toList(),
        },
      );

      print('✅ ${vitals.length} vital signs uploaded');
    } catch (e) {
      print('❌ Vital signs upload error: $e');
      rethrow;
    }
  }
}

class SyncResult {
  final bool success;
  final int imagesSynced;
  final int sensorsSynced;
  final String? error;

  SyncResult({
    required this.success,
    this.imagesSynced = 0,
    this.sensorsSynced = 0,
    this.error,
  });
}
