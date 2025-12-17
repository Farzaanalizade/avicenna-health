import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:get/get.dart';
import '../../services/camera_service.dart';

class CameraPreviewScreen extends StatefulWidget {
  final String analysisType; // TONGUE, EYE, FACE, SKIN
  
  const CameraPreviewScreen({
    required this.analysisType,
    Key? key,
  }) : super(key: key);

  @override
  State<CameraPreviewScreen> createState() => _CameraPreviewScreenState();
}

class _CameraPreviewScreenState extends State<CameraPreviewScreen> {
  late CameraService _cameraService;
  CameraController? _cameraController;
  bool _isInitializing = true;
  bool _isCapturing = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _cameraService = CameraService();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      await _cameraService.initializeCamera();
      setState(() {
        _cameraController = _cameraService.controller;
        _isInitializing = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to initialize camera: $e';
        _isInitializing = false;
      });
    }
  }

  Future<void> _captureImage() async {
    if (_isCapturing) return;
    
    setState(() => _isCapturing = true);
    
    try {
      switch (widget.analysisType) {
        case 'TONGUE':
          await _cameraService.captureTongueImage();
          break;
        case 'EYE':
          await _cameraService.captureEyeImage();
          break;
        case 'FACE':
          await _cameraService.captureFaceImage();
          break;
        case 'SKIN':
          await _cameraService.captureSkinImage(bodyPart: 'arm');
          break;
      }
      
      Get.back(result: true);
      
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Capture failed: $e')),
      );
    } finally {
      setState(() => _isCapturing = false);
    }
  }

  String _getInstructions() {
    switch (widget.analysisType) {
      case 'TONGUE':
        return 'Stick out your tongue fully and keep it still';
      case 'EYE':
        return 'Position your eye in the center of the frame';
      case 'FACE':
        return 'Face the camera with good lighting';
      case 'SKIN':
        return 'Position the skin area to be examined';
      default:
        return 'Position the camera correctly';
    }
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    _cameraService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_isInitializing) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.analysisType} Capture')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (_errorMessage != null) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.analysisType} Capture')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text(_errorMessage!),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => Get.back(),
                child: const Text('Go Back'),
              ),
            ],
          ),
        ),
      );
    }

    if (_cameraController == null) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.analysisType} Capture')),
        body: const Center(child: Text('Camera not available')),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.analysisType} Capture'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // Camera Preview
          Expanded(
            child: Stack(
              children: [
                CameraPreview(_cameraController!),
                // Guide overlay
                Container(
                  decoration: BoxDecoration(
                    border: Border.all(
                      color: Colors.green,
                      width: 3,
                    ),
                  ),
                ),
              ],
            ),
          ),
          // Instructions and Buttons
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                // Instructions
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.shade50,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.info, color: Colors.blue),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          _getInstructions(),
                          style: const TextStyle(
                            color: Colors.blue,
                            fontSize: 14,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                // Capture Button
                SizedBox(
                  width: double.infinity,
                  height: 56,
                  child: ElevatedButton.icon(
                    onPressed: _isCapturing ? null : _captureImage,
                    icon: _isCapturing
                        ? const SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                            ),
                          )
                        : const Icon(Icons.camera_alt),
                    label: Text(
                      _isCapturing ? 'Capturing...' : 'Capture Image',
                    ),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
