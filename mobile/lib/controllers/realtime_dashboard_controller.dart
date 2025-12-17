import 'package:get/get.dart';
import '../services/websocket_service.dart';
import '../services/api_service.dart';
import '../models/diagnostic_models.dart';

/// Controller for managing real-time dashboard state
/// Handles WebSocket connection, message routing, data aggregation
class RealTimeDashboardController extends GetxController {
  final WebSocketService _wsService = Get.find<WebSocketService>();
  final ApiService _apiService = Get.find<ApiService>();

  // Observables for UI binding
  final RxBool isConnected = false.obs;
  final RxInt diagnosisId = 0.obs;
  final RxList<RecommendationScore> currentRecommendations = <RecommendationScore>[].obs;
  final RxList<EffectivenessUpdate> effectivenessMetrics = <EffectivenessUpdate>[].obs;
  final RxList<FeedbackUpdate> feedbackMetrics = <FeedbackUpdate>[].obs;
  final RxDouble overallEffectiveness = 0.0.obs;
  final RxInt updateCount = 0.obs;
  final RxString lastUpdateTime = ''.obs;
  final RxList<String> recentEvents = <String>[].obs;
  final RxBool isLoadingInitialData = false.obs;
  final RxString connectionStatus = 'Disconnected'.obs;

  // Statistics
  final RxMap<String, dynamic> statistics = <String, dynamic>{
    'total_updates': 0,
    'recommendation_changes': 0,
    'effectiveness_improvements': 0,
    'feedback_submitted': 0,
  }.obs;

  @override
  void onInit() {
    super.onInit();
    _setupWebSocketCallbacks();
    _listenToConnectionStatus();
  }

  /// Setup WebSocket message callbacks
  void _setupWebSocketCallbacks() {
    _wsService.onRecommendationUpdate = (update) {
      _handleRecommendationUpdate(update);
    };

    _wsService.onEffectivenessUpdate = (update) {
      _handleEffectivenessUpdate(update);
    };

    _wsService.onFeedbackUpdate = (update) {
      _handleFeedbackUpdate(update);
    };
  }

  /// Listen to WebSocket connection status
  void _listenToConnectionStatus() {
    ever(_wsService.isConnected, (bool connected) {
      isConnected.value = connected;
      connectionStatus.value = connected ? 'Connected' : 'Disconnected';
      _addEvent(connected ? '✓ Connected to real-time updates' : '✗ Disconnected from updates');
    });
  }

  /// Initialize dashboard for diagnosis
  /// Fetches initial predictions and connects to WebSocket
  Future<void> initializeDashboard(int diagnosisIdValue, String token) async {
    try {
      isLoadingInitialData.value = true;
      diagnosisId.value = diagnosisIdValue;

      // Connect to WebSocket
      final connected = await _wsService.connect(diagnosisIdValue, token);
      if (!connected) {
        _addEvent('⚠ Failed to connect to WebSocket');
      }

      // Fetch initial predictions
      final predictions = await _apiService.getPredictions(diagnosisIdValue);
      if (predictions != null) {
        currentRecommendations.value = predictions['predicted_recommendations'] ?? [];
        _calculateOverallEffectiveness();
        _addEvent('📊 Loaded ${currentRecommendations.length} recommendations');
      }

      isLoadingInitialData.value = false;
    } catch (e) {
      print('Error initializing dashboard: $e');
      _addEvent('❌ Error initializing dashboard: $e');
      isLoadingInitialData.value = false;
    }
  }

  /// Handle recommendation_update from WebSocket
  void _handleRecommendationUpdate(RecommendationUpdate update) {
    // Update statistics
    statistics['recommendation_changes'] = (statistics['recommendation_changes'] ?? 0) + 1;
    statistics['total_updates'] = (statistics['total_updates'] ?? 0) + 1;
    statistics.refresh();

    // Add new recommendations
    for (final rec in update.addedRecommendations) {
      if (!currentRecommendations.any((r) => r.recommendationId == rec.recommendationId)) {
        currentRecommendations.add(rec);
        _addEvent('✨ New recommendation: ${rec.herbName} (${(rec.predictedEffectiveness * 100).toStringAsFixed(0)}%)');
      }
    }

    // Remove recommendations that are no longer relevant
    currentRecommendations.removeWhere(
      (rec) => update.removedRecommendationIds.contains(rec.recommendationId),
    );

    // Sort by effectiveness
    currentRecommendations.sort(
      (a, b) => b.predictedEffectiveness.compareTo(a.predictedEffectiveness),
    );

    _calculateOverallEffectiveness();
    updateCount.value++;
    lastUpdateTime.value = DateTime.now().toString();
  }

  /// Handle effectiveness_update from WebSocket
  void _handleEffectivenessUpdate(EffectivenessUpdate update) {
    // Track if this is an improvement
    final existingIndex = effectivenessMetrics.indexWhere(
      (m) => m.recommendationId == update.recommendationId,
    );

    if (existingIndex >= 0) {
      final existing = effectivenessMetrics[existingIndex];
      if (update.effectivenessScore > existing.effectivenessScore) {
        statistics['effectiveness_improvements'] = (statistics['effectiveness_improvements'] ?? 0) + 1;
        _addEvent('📈 ${update.herbName} effectiveness improved to ${(update.effectivenessScore * 100).toStringAsFixed(0)}%');
      }
      effectivenessMetrics[existingIndex] = update;
    } else {
      effectivenessMetrics.add(update);
    }

    statistics['total_updates'] = (statistics['total_updates'] ?? 0) + 1;
    statistics.refresh();

    _calculateOverallEffectiveness();
    updateCount.value++;
    lastUpdateTime.value = DateTime.now().toString();
  }

  /// Handle feedback_update from WebSocket
  void _handleFeedbackUpdate(FeedbackUpdate update) {
    // Track feedback
    statistics['feedback_submitted'] = (statistics['feedback_submitted'] ?? 0) + 1;
    statistics['total_updates'] = (statistics['total_updates'] ?? 0) + 1;
    statistics.refresh();

    // Update or add feedback metric
    final existingIndex = feedbackMetrics.indexWhere(
      (m) => m.recommendationId == update.recommendationId,
    );

    if (existingIndex >= 0) {
      feedbackMetrics[existingIndex] = update;
    } else {
      feedbackMetrics.add(update);
    }

    // Add event with rating
    final rating = (update.averageRating * 100).toStringAsFixed(0);
    _addEvent('💬 Feedback rating: $rating% for recommendation ${update.recommendationId}');

    updateCount.value++;
    lastUpdateTime.value = DateTime.now().toString();
  }

  /// Calculate overall effectiveness from current metrics
  void _calculateOverallEffectiveness() {
    if (effectivenessMetrics.isEmpty) {
      if (currentRecommendations.isNotEmpty) {
        final avgEffectiveness = currentRecommendations
                .fold(0.0, (sum, rec) => sum + rec.predictedEffectiveness) /
            currentRecommendations.length;
        overallEffectiveness.value = avgEffectiveness;
      }
    } else {
      final avgEffectiveness = effectivenessMetrics
              .fold(0.0, (sum, metric) => sum + metric.effectivenessScore) /
          effectivenessMetrics.length;
      overallEffectiveness.value = avgEffectiveness;
    }
  }

  /// Add event to recent events list (keep last 20)
  void _addEvent(String event) {
    recentEvents.insert(0, '[${DateTime.now().toString().split('.')[0]}] $event');
    if (recentEvents.length > 20) {
      recentEvents.removeAt(recentEvents.length - 1);
    }
  }

  /// Optimize recommendations for target effectiveness
  Future<void> optimizeRecommendations(double targetEffectiveness) async {
    try {
      _addEvent('⚙ Optimizing recommendations for ${(targetEffectiveness * 100).toStringAsFixed(0)}% effectiveness...');

      final optimized = await _apiService.optimizeRecommendations(
        diagnosisId.value,
        targetEffectiveness,
      );

      if (optimized != null) {
        currentRecommendations.value = optimized;
        _calculateOverallEffectiveness();
        _addEvent('✓ Recommendations optimized');
      }
    } catch (e) {
      _addEvent('❌ Error optimizing recommendations: $e');
    }
  }

  /// Get trend indicator for recommendation
  String getTrendIndicator(int recommendationId) {
    final effectiveness = effectivenessMetrics.firstWhereOrNull(
      (m) => m.recommendationId == recommendationId,
    );

    if (effectiveness == null) return '→';

    switch (effectiveness.trend) {
      case 'improving':
        return '📈';
      case 'declining':
        return '📉';
      default:
        return '→';
    }
  }

  /// Get color for effectiveness score
  String getEffectivenessColor(double score) {
    if (score >= 0.75) return '🟢'; // Green - excellent
    if (score >= 0.5) return '🟡'; // Yellow - good
    if (score >= 0.25) return '🟠'; // Orange - fair
    return '🔴'; // Red - poor
  }

  /// Get detailed statistics
  Map<String, dynamic> getDetailedStats() {
    return {
      'connected': isConnected.value,
      'connection_status': connectionStatus.value,
      'total_recommendations': currentRecommendations.length,
      'average_effectiveness': overallEffectiveness.value,
      'total_updates_received': updateCount.value,
      'recommendation_changes': statistics['recommendation_changes'] ?? 0,
      'effectiveness_improvements': statistics['effectiveness_improvements'] ?? 0,
      'feedback_submissions': statistics['feedback_submitted'] ?? 0,
      'last_update': lastUpdateTime.value,
      'recent_events': recentEvents.length,
    };
  }

  /// Refresh data by fetching latest predictions
  Future<void> refreshData() async {
    try {
      _addEvent('🔄 Refreshing data...');
      final predictions = await _apiService.getPredictions(diagnosisId.value);
      if (predictions != null) {
        currentRecommendations.value = predictions['predicted_recommendations'] ?? [];
        _calculateOverallEffectiveness();
        _addEvent('✓ Data refreshed');
      }
    } catch (e) {
      _addEvent('❌ Error refreshing data: $e');
    }
  }

  /// Disconnect from WebSocket
  Future<void> disconnect() async {
    await _wsService.disconnect();
    _addEvent('🔌 Disconnected from real-time updates');
  }

  @override
  void onClose() {
    disconnect();
    super.onClose();
  }
}
