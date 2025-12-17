import 'package:get/get.dart';
import '../services/api_service.dart';

class DiagnosticController extends GetxController {
  final _apiService = ApiService();

  // Pulse Analysis
  final pulseRate = 72.obs;
  final pulseType = 'daqiq'.obs;
  final pulseRhythm = 'montazem'.obs;
  final pulseStrength = 'motavassset'.obs;
  final temperatureSensation = 'normal'.obs;
  final pulseDepth = 'surface'.obs;
  final pulseWidth = 'normal'.obs;

  // Urine Analysis
  final urineColor = 'zard'.obs;
  final urineDensity = 'motavassset'.obs;
  final urineClarity = 'roshan'.obs;
  final hasSediment = false.obs;
  final hasCrystal = false.obs;
  final hasBlood = false.obs;

  // Tongue Analysis
  final tongueBodyColor = 'pink'.obs;
  final tongueCoatingColor = 'white'.obs;
  final tongueCoatingThickness = 'thin'.obs;
  final tongueMoisture = 'normal'.obs;
  final tongueTexture = 'smooth'.obs;

  // Results
  final isLoading = false.obs;
  final errorMessage = Rx<String?>(null);
  final analysisResults = Rx<Map<String, dynamic>?>(null);
  final dominantMizaj = Rx<String?>(null);
  final healthStatus = Rx<String?>(null);
  final recommendedRemedies = <String>[].obs;
  final lifestyleRecommendations = <String>[].obs;
  final dietaryRecommendations = <String>[].obs;

  int patientId = 1; // Should come from auth

  // Step tracking
  final currentStep = 0.obs;
  final totalSteps = 3.obs;

  /// Submit pulse analysis
  Future<void> submitPulseAnalysis() async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      await _apiService.post(
        '/diagnosis/pulse',
        {
          'patient_id': patientId,
          'pulse_rate': pulseRate.value,
          'type': pulseType.value,
          'rhythm': pulseRhythm.value,
          'strength': pulseStrength.value,
          'temperature_sensation': temperatureSensation.value,
          'depth': pulseDepth.value,
          'width': pulseWidth.value,
        },
      );

      Get.snackbar('موفقیت', 'نبض ثبت شد',
          snackPosition: SnackPosition.BOTTOM);
      currentStep.value = 1;
        } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', 'خطا در ثبت نبض: $e',
          snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  /// Submit urine analysis
  Future<void> submitUrineAnalysis() async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      await _apiService.post(
        '/diagnosis/urine',
        {
          'patient_id': patientId,
          'color': urineColor.value,
          'density': urineDensity.value,
          'clarity': urineClarity.value,
          'sediment': hasSediment.value,
          'crystal': hasCrystal.value,
          'blood': hasBlood.value,
        },
      );

      Get.snackbar('موفقیت', 'ادرار ثبت شد',
          snackPosition: SnackPosition.BOTTOM);
      currentStep.value = 2;
        } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', 'خطا در ثبت ادرار: $e',
          snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  /// Submit tongue analysis
  Future<void> submitTongueAnalysis() async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      await _apiService.post(
        '/diagnosis/tongue',
        {
          'patient_id': patientId,
          'body_color': tongueBodyColor.value,
          'coating_color': tongueCoatingColor.value,
          'coating_thickness': tongueCoatingThickness.value,
          'moisture': tongueMoisture.value,
          'texture': tongueTexture.value,
        },
      );

      Get.snackbar('موفقیت', 'زبان ثبت شد',
          snackPosition: SnackPosition.BOTTOM);
      currentStep.value = 3;
        } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', 'خطا در ثبت زبان: $e',
          snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  /// Get comprehensive analysis
  Future<void> getComprehensiveAnalysis() async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.post(
        '/analysis/comprehensive/$patientId',
        {
          'pulse_data': {
            'pulse_rate': pulseRate.value,
            'type': pulseType.value,
            'rhythm': pulseRhythm.value,
            'strength': pulseStrength.value,
            'temperature_sensation': temperatureSensation.value,
            'depth': pulseDepth.value,
            'width': pulseWidth.value,
          },
          'urine_data': {
            'color': urineColor.value,
            'density': urineDensity.value,
            'clarity': urineClarity.value,
            'sediment': hasSediment.value,
            'crystal': hasCrystal.value,
            'blood': hasBlood.value,
          },
          'tongue_data': {
            'body_color': tongueBodyColor.value,
            'coating_color': tongueCoatingColor.value,
            'coating_thickness': tongueCoatingThickness.value,
            'moisture': tongueMoisture.value,
            'texture': tongueTexture.value,
          },
        },
      );

      analysisResults.value = response;
      dominantMizaj.value = response['dominant_mizaj'];
      healthStatus.value = response['health_status'];
      
      if (response['recommended_remedies'] is List) {
        recommendedRemedies.value = List<String>.from(
          response['recommended_remedies'] as List,
        );
      }
      if (response['lifestyle_recommendations'] is List) {
        lifestyleRecommendations.value = List<String>.from(
          response['lifestyle_recommendations'] as List,
        );
      }
      if (response['dietary_recommendations'] is List) {
        dietaryRecommendations.value = List<String>.from(
          response['dietary_recommendations'] as List,
        );
      }

      Get.snackbar('موفقیت', 'تحلیل جامع انجام شد',
          snackPosition: SnackPosition.BOTTOM);
        } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', 'خطا در تحلیل: $e',
          snackPosition: SnackPosition.BOTTOM);
    } finally {
      isLoading.value = false;
    }
  }

  /// Reset form
  void resetForm() {
    pulseRate.value = 72;
    pulseType.value = 'daqiq';
    pulseRhythm.value = 'montazem';
    pulseStrength.value = 'motavassset';
    temperatureSensation.value = 'normal';
    pulseDepth.value = 'surface';
    pulseWidth.value = 'normal';

    urineColor.value = 'zard';
    urineDensity.value = 'motavassset';
    urineClarity.value = 'roshan';
    hasSediment.value = false;
    hasCrystal.value = false;
    hasBlood.value = false;

    tongueBodyColor.value = 'pink';
    tongueCoatingColor.value = 'white';
    tongueCoatingThickness.value = 'thin';
    tongueMoisture.value = 'normal';
    tongueTexture.value = 'smooth';

    currentStep.value = 0;
    analysisResults.value = null;
    dominantMizaj.value = null;
    healthStatus.value = null;
    recommendedRemedies.clear();
    lifestyleRecommendations.clear();
    dietaryRecommendations.clear();
  }
}
