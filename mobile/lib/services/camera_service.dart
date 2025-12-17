import 'package:camera/camera.dart';
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
  bool _isInitialized = false;
  CameraDescription? _currentCamera;
  
  /// Get available cameras on device
  Future<List<CameraDescription>> getAvailableCameras() async {
    if (cameras == null) {
      cameras = await availableCameras();
    }
    return cameras ?? [];
  }
  
  /// Initialize specific camera (front/rear)
  /// For TONGUE, EYE, FACE use front camera
  /// For SKIN use rear camera
  Future<void> initializeCameraForAnalysis(ImageAnalysisType analysisType) async {
    try {
      final availableCameras = await getAvailableCameras();
      
      if (availableCameras.isEmpty) {
        throw Exception('No cameras available on this device');
      }
      
      // Select camera based on analysis type
      CameraLensDirection direction;
      switch (analysisType) {
        case ImageAnalysisType.TONGUE:
        case ImageAnalysisType.EYE:
        case ImageAnalysisType.FACE:
          direction = CameraLensDirection.front; // Selfie camera
          break;
        case ImageAnalysisType.SKIN:
          direction = CameraLensDirection.back; // Rear camera
          break;
      }
      
      // Find camera with requested direction
      final camera = availableCameras.firstWhere(
        (cam) => cam.lensDirection == direction,
        orElse: () => availableCameras.first,
      );
      
      _currentCamera = camera;
      
      // Dispose old controller if exists
      if (_isInitialized) {
        await _controller.dispose();
      }
      
      _controller = CameraController(
        camera,
        ResolutionPreset.high,
        enableAudio: false,
      );
      
      await _controller.initialize();
      _isInitialized = true;
      
      print('✅ Camera initialized for ${analysisType.name}');
      print('   Direction: ${camera.lensDirection}');
      
    } catch (e) {
      print('❌ Camera initialization error: $e');
      rethrow;
    }
  }
  
  /// Initialize camera (legacy - defaults to front)
  Future<void> initializeCamera() async {
    await initializeCameraForAnalysis(ImageAnalysisType.TONGUE);
  }
  
  /// Capture tongue image (selfie camera)
  Future<File?> captureTongueImage() async {
    await initializeCameraForAnalysis(ImageAnalysisType.TONGUE);
    return _captureImage(
      imageType: ImageAnalysisType.TONGUE,
      hint: 'Show full tongue with good lighting',
    );
  }
  
  /// Capture eye image (selfie camera)
  Future<File?> captureEyeImage() async {
    await initializeCameraForAnalysis(ImageAnalysisType.EYE);
    return _captureImage(
      imageType: ImageAnalysisType.EYE,
      hint: 'Both eyes fully visible, front-facing',
    );
  }
  
  /// Capture face image (selfie camera)
  Future<File?> captureFaceImage() async {
    await initializeCameraForAnalysis(ImageAnalysisType.FACE);
    return _captureImage(
      imageType: ImageAnalysisType.FACE,
      hint: 'Full face, neutral expression, good lighting',
    );
  }
  
  /// Capture skin image (rear camera only!)
  Future<File?> captureSkinImage({required String bodyPart}) async {
    await initializeCameraForAnalysis(ImageAnalysisType.SKIN);
    return _captureImage(
      imageType: ImageAnalysisType.SKIN,
      hint: 'Close-up of $bodyPart with good lighting',
    );
  }
  
  /// Internal capture method
  Future<File?> _captureImage({
    required ImageAnalysisType imageType,
    required String hint,
  }) async {
    try {
      if (!_isInitialized) {
        await initializeCameraForAnalysis(imageType);
      }
      
      final image = await _controller.takePicture();
      final file = File(image.path);
      
      print('✅ Captured ${imageType.name} image: ${file.path}');
      print('   File size: ${file.lengthSync() / 1024 / 1024} MB');
      
      return file;
      
    } catch (e) {
      print('❌ Image capture error: $e');
      return null;
    }
  }
  
  /// Get controller for preview
  CameraController get controller {
    if (!_isInitialized) {
      throw Exception('Camera not initialized. Call initializeCamera() first.');
    }
    return _controller;
  }
  
  /// Check if camera is initialized
  bool get isInitialized => _isInitialized;
  
  /// Get current camera direction
  CameraLensDirection? get currentCameraDirection => _currentCamera?.lensDirection;
  
  /// Check if rear camera is available
  Future<bool> hasRearCamera() async {
    final availableCameras = await getAvailableCameras();
    return availableCameras.any((cam) => cam.lensDirection == CameraLensDirection.back);
  }
  
  /// Check if front camera is available
  Future<bool> hasFrontCamera() async {
    final availableCameras = await getAvailableCameras();
    return availableCameras.any((cam) => cam.lensDirection == CameraLensDirection.front);
  }
  
  /// Cleanup
  Future<void> dispose() async {
    if (_isInitialized) {
      await _controller.dispose();
      _isInitialized = false;
      _currentCamera = null;
      print('✅ Camera disposed');
    }
  }
}
