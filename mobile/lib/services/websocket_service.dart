import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import 'dart:convert';
import 'package:get/get.dart';
import '../models/diagnostic_models.dart';

/// WebSocket service for real-time updates from backend
/// Handles connection management, message receiving, and reconnection logic
class WebSocketService extends GetxService {
  late WebSocketChannel _channel;
  final String _baseUrl = 'ws://localhost:8000'; // Change for production
  final int _reconnectMaxAttempts = 5;
  final int _reconnectDelayMs = 2000;

  // Observable streams
  final RxBool isConnected = false.obs;
  final RxInt reconnectAttempts = 0.obs;
  final RxList<dynamic> messageHistory = <dynamic>[].obs;
  final RxMap<String, dynamic> latestMetrics = <String, dynamic>{}.obs;

  // Callbacks for different message types
  Function(RecommendationUpdate)? onRecommendationUpdate;
  Function(EffectivenessUpdate)? onEffectivenessUpdate;
  Function(FeedbackUpdate)? onFeedbackUpdate;

  /// Connect to WebSocket with JWT authentication
  /// [diagnosisId] The diagnosis ID to connect to
  /// [token] JWT authentication token
  Future<bool> connect(int diagnosisId, String token) async {
    try {
      final wsUrl = Uri.parse(
        '$_baseUrl/ws/$diagnosisId?token=$token',
      );

      _channel = WebSocketChannel.connect(wsUrl);

      // Listen for messages
      _channel.stream.listen(
        (dynamic message) => _handleMessage(message),
        onError: (error) => _handleError(error),
        onDone: () => _handleConnectionClosed(),
      );

      isConnected.value = true;
      reconnectAttempts.value = 0;
      return true;
    } catch (e) {
      print('WebSocket connection failed: $e');
      return false;
    }
  }

  /// Handle incoming WebSocket messages
  void _handleMessage(dynamic message) {
    try {
      final data = jsonDecode(message as String) as Map<String, dynamic>;
      final messageType = data['type'] as String?;

      // Add to history
      messageHistory.add({
        'timestamp': DateTime.now(),
        'data': data,
      });

      // Route based on message type
      switch (messageType) {
        case 'recommendation_update':
          _handleRecommendationUpdate(data);
          break;
        case 'effectiveness_update':
          _handleEffectivenessUpdate(data);
          break;
        case 'feedback_update':
          _handleFeedbackUpdate(data);
          break;
        default:
          print('Unknown message type: $messageType');
      }

      // Store latest metrics
      latestMetrics.value = data;
    } catch (e) {
      print('Error handling WebSocket message: $e');
    }
  }

  /// Handle recommendation_update message
  /// Format: {
  ///   type: "recommendation_update",
  ///   diagnosis_id: int,
  ///   added_recommendations: [{id, herb_name, predicted_effectiveness}],
  ///   removed_recommendations: [{id, herb_name}],
  ///   timestamp: string
  /// }
  void _handleRecommendationUpdate(Map<String, dynamic> data) {
    try {
      final update = RecommendationUpdate.fromJson(data);
      onRecommendationUpdate?.call(update);
      print('Recommendation update received: ${update.addedRecommendations.length} added');
    } catch (e) {
      print('Error parsing recommendation update: $e');
    }
  }

  /// Handle effectiveness_update message
  /// Format: {
  ///   type: "effectiveness_update",
  ///   recommendation_id: int,
  ///   herb_name: string,
  ///   effectiveness_score: float,
  ///   confidence: float,
  ///   sample_size: int,
  ///   trend: "improving" | "stable" | "declining",
  ///   timestamp: string
  /// }
  void _handleEffectivenessUpdate(Map<String, dynamic> data) {
    try {
      final update = EffectivenessUpdate.fromJson(data);
      onEffectivenessUpdate?.call(update);
      print('Effectiveness update: ${update.herbName} = ${update.effectivenessScore}');
    } catch (e) {
      print('Error parsing effectiveness update: $e');
    }
  }

  /// Handle feedback_update message
  /// Format: {
  ///   type: "feedback_update",
  ///   recommendation_id: int,
  ///   average_rating: float,
  ///   improvement_score: float,
  ///   side_effects: [string],
  ///   sample_size: int,
  ///   timestamp: string
  /// }
  void _handleFeedbackUpdate(Map<String, dynamic> data) {
    try {
      final update = FeedbackUpdate.fromJson(data);
      onFeedbackUpdate?.call(update);
      print('Feedback update: ${update.recommendationId}');
    } catch (e) {
      print('Error parsing feedback update: $e');
    }
  }

  /// Handle connection errors
  void _handleError(dynamic error) {
    print('WebSocket error: $error');
    isConnected.value = false;
    _attemptReconnect();
  }

  /// Handle connection closed
  void _handleConnectionClosed() {
    print('WebSocket connection closed');
    isConnected.value = false;
    _attemptReconnect();
  }

  /// Attempt to reconnect with exponential backoff
  Future<void> _attemptReconnect() async {
    if (reconnectAttempts.value >= _reconnectMaxAttempts) {
      print('Max reconnection attempts reached');
      return;
    }

    reconnectAttempts.value++;
    final delayMs = _reconnectDelayMs * reconnectAttempts.value;

    print('Attempting to reconnect (attempt ${reconnectAttempts.value}/$_reconnectMaxAttempts) in ${delayMs}ms');
    await Future.delayed(Duration(milliseconds: delayMs));

    // Note: User should call connect() again - this is tracked in controller
  }

  /// Send message to server
  void sendMessage(Map<String, dynamic> message) {
    try {
      if (isConnected.value) {
        _channel.sink.add(jsonEncode(message));
      } else {
        print('WebSocket not connected');
      }
    } catch (e) {
      print('Error sending WebSocket message: $e');
    }
  }

  /// Disconnect from WebSocket
  Future<void> disconnect() async {
    try {
      await _channel.sink.close(status.goingAway);
      isConnected.value = false;
      print('WebSocket disconnected');
    } catch (e) {
      print('Error disconnecting WebSocket: $e');
    }
  }

  /// Get connection status
  bool get isActive => isConnected.value;

  /// Get message history (last 50 messages)
  List<dynamic> getMessageHistory() {
    final history = messageHistory.value;
    return history.length > 50 ? history.sublist(history.length - 50) : history;
  }

  /// Clear message history
  void clearHistory() {
    messageHistory.clear();
  }

  @override
  void onClose() {
    disconnect();
    super.onClose();
  }
}

/// Model for recommendation_update message
class RecommendationUpdate {
  final int diagnosisId;
  final List<RecommendationScore> addedRecommendations;
  final List<int> removedRecommendationIds;
  final DateTime timestamp;

  RecommendationUpdate({
    required this.diagnosisId,
    required this.addedRecommendations,
    required this.removedRecommendationIds,
    required this.timestamp,
  });

  factory RecommendationUpdate.fromJson(Map<String, dynamic> json) {
    return RecommendationUpdate(
      diagnosisId: json['diagnosis_id'] as int,
      addedRecommendations: (json['added_recommendations'] as List?)
              ?.map((r) => RecommendationScore.fromJson(r as Map<String, dynamic>))
              .toList() ??
          [],
      removedRecommendationIds: (json['removed_recommendations'] as List?)
              ?.map((r) => r['id'] as int)
              .toList() ??
          [],
      timestamp: DateTime.tryParse(json['timestamp'] as String? ?? '') ?? DateTime.now(),
    );
  }
}

/// Model for recommendation score
class RecommendationScore {
  final int recommendationId;
  final String herbName;
  final double predictedEffectiveness;
  final double confidence;
  final String reasoning;

  RecommendationScore({
    required this.recommendationId,
    required this.herbName,
    required this.predictedEffectiveness,
    required this.confidence,
    required this.reasoning,
  });

  factory RecommendationScore.fromJson(Map<String, dynamic> json) {
    return RecommendationScore(
      recommendationId: json['recommendation_id'] as int? ?? 0,
      herbName: json['herb_name'] as String? ?? 'Unknown',
      predictedEffectiveness: (json['predicted_effectiveness'] as num? ?? 0.0).toDouble(),
      confidence: (json['confidence'] as num? ?? 0.0).toDouble(),
      reasoning: json['reasoning'] as String? ?? '',
    );
  }
}

/// Model for effectiveness_update message
class EffectivenessUpdate {
  final int recommendationId;
  final String herbName;
  final double effectivenessScore;
  final double confidence;
  final int sampleSize;
  final String trend; // improving, stable, declining
  final DateTime timestamp;

  EffectivenessUpdate({
    required this.recommendationId,
    required this.herbName,
    required this.effectivenessScore,
    required this.confidence,
    required this.sampleSize,
    required this.trend,
    required this.timestamp,
  });

  factory EffectivenessUpdate.fromJson(Map<String, dynamic> json) {
    return EffectivenessUpdate(
      recommendationId: json['recommendation_id'] as int? ?? 0,
      herbName: json['herb_name'] as String? ?? 'Unknown',
      effectivenessScore: (json['effectiveness_score'] as num? ?? 0.0).toDouble(),
      confidence: (json['confidence'] as num? ?? 0.0).toDouble(),
      sampleSize: json['sample_size'] as int? ?? 0,
      trend: json['trend'] as String? ?? 'stable',
      timestamp: DateTime.tryParse(json['timestamp'] as String? ?? '') ?? DateTime.now(),
    );
  }
}

/// Model for feedback_update message
class FeedbackUpdate {
  final int recommendationId;
  final double averageRating;
  final double improvementScore;
  final List<String> sideEffects;
  final int sampleSize;
  final DateTime timestamp;

  FeedbackUpdate({
    required this.recommendationId,
    required this.averageRating,
    required this.improvementScore,
    required this.sideEffects,
    required this.sampleSize,
    required this.timestamp,
  });

  factory FeedbackUpdate.fromJson(Map<String, dynamic> json) {
    return FeedbackUpdate(
      recommendationId: json['recommendation_id'] as int? ?? 0,
      averageRating: (json['average_rating'] as num? ?? 0.0).toDouble(),
      improvementScore: (json['improvement_score'] as num? ?? 0.0).toDouble(),
      sideEffects: (json['side_effects'] as List?)?.map((e) => e as String).toList() ?? [],
      sampleSize: json['sample_size'] as int? ?? 0,
      timestamp: DateTime.tryParse(json['timestamp'] as String? ?? '') ?? DateTime.now(),
    );
  }
}
