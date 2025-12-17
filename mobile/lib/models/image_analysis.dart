enum AnalysisType { TONGUE, EYE, FACE, SKIN }

class ImageAnalysis {
  final String id;
  final String filePath;
  final AnalysisType type;
  final DateTime captureTime;
  final bool uploaded;
  final String? analysisResult;
  
  ImageAnalysis({
    required this.id,
    required this.filePath,
    required this.type,
    required this.captureTime,
    this.uploaded = false,
    this.analysisResult,
  });
  
  /// Convert to JSON for API
  Map<String, dynamic> toJson() => {
    'id': id,
    'file_path': filePath,
    'type': type.name,
    'capture_time': captureTime.toIso8601String(),
    'uploaded': uploaded,
    'analysis_result': analysisResult,
  };
  
  /// Create from JSON
  factory ImageAnalysis.fromJson(Map<String, dynamic> json) {
    return ImageAnalysis(
      id: json['id'],
      filePath: json['file_path'],
      type: AnalysisType.values.byName(json['type']),
      captureTime: DateTime.parse(json['capture_time']),
      uploaded: json['uploaded'] ?? false,
      analysisResult: json['analysis_result'],
    );
  }
  
  @override
  String toString() => 'ImageAnalysis(type: ${type.name}, uploaded: $uploaded)';
}
