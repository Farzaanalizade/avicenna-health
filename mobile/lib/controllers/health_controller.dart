import 'package:get/get.dart';

/// DEPRECATED: Use HealthDataController instead
/// This is a minimal stub kept for backward compatibility
class HealthController extends GetxController {
  final isLoading = false.obs;
  final errorMessage = Rx<String?>(null);
}
