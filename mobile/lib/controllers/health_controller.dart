import 'package:get/get.dart';
import '../services/api_service.dart';
import '../models/health_record.dart';

class HealthController extends GetxController {
  // Observables
  final healthRecords = <HealthRecord>[].obs;
  final isLoading = false.obs;
  final errorMessage = Rx<String?>(null);
  final currentAnalysisType = Rx<String?>(null);
  
  // Analysis results
  final tongueAnalysis = Rx<Map<String, dynamic>?>(null);
  final eyeAnalysis = Rx<Map<String, dynamic>?>(null);
  final vitalsAnalysis = Rx<Map<String, dynamic>?>(null);
  final quickCheckResult = Rx<Map<String, dynamic>?>(null);

  final _apiService = ApiService();

  @override
  void onInit() {
    super.onInit();
    getHealthRecords();
  }

  /// Get all health records
  Future<void> getHealthRecords({int skip = 0, int limit = 20}) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.get(
        '/health/records?skip=$skip&limit=$limit',
      );

      if (response['items'] != null) {
        final records = (response['items'] as List)
            .map((r) => HealthRecord.fromJson(r))
            .toList();
        healthRecords.addAll(records);
      }
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
    }
  }

  /// Analyze tongue image
  Future<void> analyzeTongue({
    required String imageBase64,
    String? moisture,
    String? coating,
    String? color,
  }) async {
    try {
      isLoading.value = true;
      currentAnalysisType.value = 'tongue';
      errorMessage.value = null;

      final response = await _apiService.post(
        '/health/analyze/tongue',
        {
          'image_base64': imageBase64,
          'moisture': moisture ?? 'normal',
          'coating': coating ?? 'none',
          'color': color ?? 'normal',
        },
      );

      tongueAnalysis.value = response;

      // Add to records
      if (response['analysis_id'] != null) {
        final record = HealthRecord(
          id: response['analysis_id'],
          recordType: 'tongue',
          analysisResults: response,
          recordedAt: DateTime.now(),
        );
        healthRecords.insert(0, record);
      }
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
      currentAnalysisType.value = null;
    }
  }

  /// Analyze eye image
  Future<void> analyzeEye({
    required String imageBase64,
    String? brightness,
    String? clarity,
    String? color,
  }) async {
    try {
      isLoading.value = true;
      currentAnalysisType.value = 'eye';
      errorMessage.value = null;

      final response = await _apiService.post(
        '/health/analyze/eye',
        {
          'image_base64': imageBase64,
          'brightness': brightness ?? 'normal',
          'clarity': clarity ?? 'clear',
          'color': color,
        },
      );

      eyeAnalysis.value = response;

      if (response['analysis_id'] != null) {
        final record = HealthRecord(
          id: response['analysis_id'],
          recordType: 'eye',
          analysisResults: response,
          recordedAt: DateTime.now(),
        );
        healthRecords.insert(0, record);
      }
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
      currentAnalysisType.value = null;
    }
  }

  /// Analyze vital signs
  Future<void> analyzeVitals({
    required int heartRate,
    required int bloodPressureSystolic,
    required int bloodPressureDiastolic,
    required double temperature,
    required int oxygenSaturation,
    int? respiratoryRate,
  }) async {
    try {
      isLoading.value = true;
      currentAnalysisType.value = 'vitals';
      errorMessage.value = null;

      final response = await _apiService.post(
        '/health/analyze/vitals',
        {
          'heart_rate': heartRate,
          'blood_pressure_systolic': bloodPressureSystolic,
          'blood_pressure_diastolic': bloodPressureDiastolic,
          'temperature': temperature,
          'oxygen_saturation': oxygenSaturation,
          'respiratory_rate': respiratoryRate ?? 16,
        },
      );

      vitalsAnalysis.value = response;

      if (response['analysis_id'] != null) {
        final record = HealthRecord(
          id: response['analysis_id'],
          recordType: 'vitals',
          analysisResults: response,
          recordedAt: DateTime.now(),
        );
        healthRecords.insert(0, record);
      }
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
      currentAnalysisType.value = null;
    }
  }

  /// Quick health check
  Future<void> quickHealthCheck({
    required List<String> symptoms,
    required int durationDays,
    required String severity,
  }) async {
    try {
      isLoading.value = true;
      currentAnalysisType.value = 'quick-check';
      errorMessage.value = null;

      final response = await _apiService.post(
        '/health/quick-check',
        {
          'symptoms': symptoms,
          'duration_days': durationDays,
          'severity': severity,
        },
      );

      quickCheckResult.value = response;

      if (response['analysis_id'] != null) {
        final record = HealthRecord(
          id: response['analysis_id'],
          recordType: 'quick_check',
          analysisResults: response,
          recordedAt: DateTime.now(),
        );
        healthRecords.insert(0, record);
      }
    } catch (e) {
      errorMessage.value = e.toString();
    } finally {
      isLoading.value = false;
      currentAnalysisType.value = null;
    }
  }

  /// Delete health record
  Future<bool> deleteRecord(int recordId) async {
    try {
      await _apiService.delete('/health/records/$recordId');

      // Remove from list
      healthRecords.removeWhere((r) => r.id == recordId);
      return true;
    } catch (e) {
      errorMessage.value = e.toString();
      return false;
    }
  }

  /// Clear error message
  void clearError() {
    errorMessage.value = null;
  }

  /// Clear all analysis results
  void clearAnalysis() {
    tongueAnalysis.value = null;
    eyeAnalysis.value = null;
    vitalsAnalysis.value = null;
    quickCheckResult.value = null;
  }
}
