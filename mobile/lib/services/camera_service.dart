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
  
  /// Initialize camera
  Future<void> initializeCamera() async {
    if (_isInitialized) return;
    
    try {
      cameras = await availableCameras();
      if (cameras!.isNotEmpty) {
        _controller = CameraController(
          cameras![0], // Front camera
          ResolutionPreset.high,
          enableAudio: false,
        );
        await _controller.initialize();
        _isInitialized = true;
        print('✅ Camera initialized successfully');
      }
    } catch (e) {
      print('❌ Camera initialization error: $e');
      rethrow;
    }
  }
  
  /// Capture tongue image
  Future<File?> captureTongueImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.TONGUE,
      hint: 'Show full tongue with good lighting',
    );
  }
  
  /// Capture eye image
  Future<File?> captureEyeImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.EYE,
      hint: 'Both eyes fully visible, front-facing',
    );
  }
  
  /// Capture face image
  Future<File?> captureFaceImage() async {
    return _captureImage(
      imageType: ImageAnalysisType.FACE,
      hint: 'Full face, neutral expression, good lighting',
    );
  }
  
  /// Capture skin image
  Future<File?> captureSkinImage({required String bodyPart}) async {
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
        await initializeCamera();
      }
      
      final image = await _controller.takePicture();
      final file = File(image.path);
      
      print('✅ Captured ${imageType.name} image: ${file.path}');
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
  
  /// Cleanup
  Future<void> dispose() async {
    if (_isInitialized) {
      await _controller.dispose();
      _isInitialized = false;
      print('✅ Camera disposed');
    }
  }
}
