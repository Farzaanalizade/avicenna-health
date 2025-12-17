import 'dart:io';

class ImageValidator {
  /// Validate image quality
  static Future<ValidationResult> validateImage(
    File imageFile, {
    required String analysisType,
  }) async {
    try {
      // Check file size (50KB - 10MB)
      int fileSize = await imageFile.length();
      if (fileSize < 50000) {
        return ValidationResult(
          isValid: false,
          reason: 'Image too small (minimum 50KB)',
        );
      }
      
      if (fileSize > 10000000) {
        return ValidationResult(
          isValid: false,
          reason: 'Image too large (maximum 10MB)',
        );
      }
      
      // Image format check (basic)
      String path = imageFile.path.toLowerCase();
      if (!path.endsWith('.jpg') && !path.endsWith('.jpeg') && !path.endsWith('.png')) {
        return ValidationResult(
          isValid: false,
          reason: 'Invalid image format (use JPG or PNG)',
        );
      }
      
      return ValidationResult(isValid: true);
      
    } catch (e) {
      return ValidationResult(
        isValid: false,
        reason: 'Validation error: $e',
      );
    }
  }
  
  /// Check file exists
  static Future<bool> fileExists(String path) async {
    return await File(path).exists();
  }
  
  /// Get file size in MB
  static Future<double> getFileSizeInMB(File file) async {
    int bytes = await file.length();
    return bytes / (1024 * 1024);
  }
}

class ValidationResult {
  final bool isValid;
  final String? reason;
  
  ValidationResult({
    required this.isValid,
    this.reason,
  });
  
  @override
  String toString() => isValid 
    ? '✅ Valid' 
    : '❌ Invalid: $reason';
}
