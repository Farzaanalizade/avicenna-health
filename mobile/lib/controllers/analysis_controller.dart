import 'package:get/get.dart';
import '../services/api_service.dart';

class AnalysisController extends GetxController {
  final _apiService = ApiService();

  // State
  final isLoading = false.obs;
  final errorMessage = Rx<String?>(null);

  /// دریافت تطابق‌های دانایی پزشکی
  /// Get knowledge matches for a diagnosis
  Future<dynamic> getKnowledgeMatches(int diagnosisId) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.get(
        '/analysis/$diagnosisId/match',
      );

      if (response != null && response['success'] == true) {
        return response;
      } else {
        throw Exception(response?['detail'] ?? 'خطا در دریافت تطابق‌ها');
      }
    } catch (e) {
      errorMessage.value = e.toString();
      rethrow;
    } finally {
      isLoading.value = false;
    }
  }

  /// دریافت توصیه‌های درمانی
  /// Get treatment recommendations
  Future<dynamic> getRecommendations(int diagnosisId, {String? tradition}) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final params = tradition != null ? '?tradition=$tradition' : '';
      final response = await _apiService.get(
        '/analysis/$diagnosisId/recommendations$params',
      );

      if (response != null && response['success'] == true) {
        return response;
      } else {
        throw Exception(response?['detail'] ?? 'خطا در دریافت توصیه‌ها');
      }
    } catch (e) {
      errorMessage.value = e.toString();
      rethrow;
    } finally {
      isLoading.value = false;
    }
  }

  /// مقایسه دیدگاه سنت‌های مختلف
  /// Compare different medical traditions
  Future<dynamic> compareTraditions(int diagnosisId) async {
    try {
      isLoading.value = true;
      errorMessage.value = null;

      final response = await _apiService.get(
        '/analysis/$diagnosisId/compare',
      );

      if (response != null && response['success'] == true) {
        return response;
      } else {
        throw Exception(response?['detail'] ?? 'خطا در مقایسه سنت‌ها');
      }
    } catch (e) {
      errorMessage.value = e.toString();
      rethrow;
    } finally {
      isLoading.value = false;
    }
  }
}
