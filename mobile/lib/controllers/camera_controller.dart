import 'package:get/get.dart';
import '../models/image_analysis.dart';
import '../services/camera_service.dart';
import '../services/sync_service.dart';
import '../database/app_database.dart';
import 'dart:io';

class CameraController extends GetxController {
  final _cameraService = CameraService();
  final _syncService = SyncService();
  final _database = AppDatabase();

  var capturedImages = <ImageAnalysis>[].obs;
  var isCapturing = false.obs;
  var syncStatus = 'Not synced'.obs;

  /// Capture image by type
  Future<void> captureImage(String imageType) async {
    isCapturing.value = true;
    try {
      File? imageFile;

      switch (imageType.toUpperCase()) {
        case 'TONGUE':
          imageFile = await _cameraService.captureTongueImage();
          break;
        case 'EYE':
          imageFile = await _cameraService.captureEyeImage();
          break;
        case 'FACE':
          imageFile = await _cameraService.captureFaceImage();
          break;
        case 'SKIN':
          imageFile = await _cameraService.captureSkinImage(bodyPart: 'arm');
          break;
        default:
          throw Exception('Unknown image type: $imageType');
      }

      if (imageFile != null) {
        final fileSize = await imageFile.length();

        // Save to database
        final id = await _database.insertImage(
          imageType,
          imageFile.path,
          fileSize,
        );

        // Add to local list
        final analysis = ImageAnalysis(
          id: id.toString(),
          filePath: imageFile.path,
          type: _getAnalysisType(imageType),
          captureTime: DateTime.now(),
          uploaded: false,
        );

        capturedImages.add(analysis);
        Get.snackbar('✅ Success', 'Image captured: $imageType');
      }
    } catch (e) {
      Get.snackbar('❌ Error', 'Capture failed: $e');
    } finally {
      isCapturing.value = false;
    }
  }

  /// Sync all captured images
  Future<void> syncAllImages() async {
    try {
      syncStatus.value = 'Syncing...';

      // Use patient ID from auth (hardcoded for now)
      const int patientId = 1;

      final result = await _syncService.syncAllData(patientId);

      if (result.success) {
        syncStatus.value =
            'Synced ${result.imagesSynced} images, ${result.sensorsSynced} sensors';
        Get.snackbar('✅ Success', syncStatus.value);

        // Clear local list
        capturedImages.clear();
      } else {
        syncStatus.value = 'Sync failed: ${result.error}';
        Get.snackbar('❌ Error', syncStatus.value);
      }
    } catch (e) {
      syncStatus.value = 'Sync error: $e';
      Get.snackbar('❌ Error', syncStatus.value);
    }
  }

  AnalysisType _getAnalysisType(String type) {
    switch (type.toUpperCase()) {
      case 'TONGUE':
        return AnalysisType.TONGUE;
      case 'EYE':
        return AnalysisType.EYE;
      case 'FACE':
        return AnalysisType.FACE;
      case 'SKIN':
        return AnalysisType.SKIN;
      default:
        return AnalysisType.TONGUE;
    }
  }

  @override
  void onClose() {
    _cameraService.dispose();
    super.onClose();
  }
}
