import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/realtime_dashboard_controller.dart';
import '../services/websocket_service.dart';

/// Real-time dashboard screen showing live updates from backend
/// Displays current recommendations, effectiveness metrics, and recent events
class RealTimeDashboardScreen extends StatefulWidget {
  final int diagnosisId;

  const RealTimeDashboardScreen({
    required this.diagnosisId,
    Key? key,
  }) : super(key: key);

  @override
  State<RealTimeDashboardScreen> createState() => _RealTimeDashboardScreenState();
}

class _RealTimeDashboardScreenState extends State<RealTimeDashboardScreen> {
  late RealTimeDashboardController controller;

  @override
  void initState() {
    super.initState();
    controller = Get.put(RealTimeDashboardController());
    // Initialize with JWT token from storage
    _initializeDashboard();
  }

  Future<void> _initializeDashboard() async {
    // Get JWT token from secure storage
    const token = 'YOUR_JWT_TOKEN'; // Should be fetched from secure storage
    await controller.initializeDashboard(widget.diagnosisId, token);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Real-time Dashboard'),
        elevation: 0,
        actions: [
          Obx(
            () => Padding(
              padding: const EdgeInsets.all(16.0),
              child: Center(
                child: Chip(
                  avatar: controller.isConnected.value
                      ? const CircleAvatar(
                          backgroundColor: Colors.green,
                          child: Icon(Icons.check, color: Colors.white, size: 12),
                        )
                      : const CircleAvatar(
                          backgroundColor: Colors.red,
                          child: Icon(Icons.close, color: Colors.white, size: 12),
                        ),
                  label: Obx(() => Text(controller.connectionStatus.value)),
                ),
              ),
            ),
          ),
        ],
      ),
      body: Obx(
        () => controller.isLoadingInitialData.value
            ? const Center(child: CircularProgressIndicator())
            : RefreshIndicator(
                onRefresh: () => controller.refreshData(),
                child: SingleChildScrollView(
                  physics: const AlwaysScrollableScrollPhysics(),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Overall Effectiveness Card
                        _buildEffectivenessCard(),
                        const SizedBox(height: 16),

                        // Statistics Row
                        _buildStatisticsRow(),
                        const SizedBox(height: 16),

                        // Current Recommendations
                        _buildRecommendationsSection(),
                        const SizedBox(height: 16),

                        // Effectiveness Metrics
                        _buildEffectivenessMetricsSection(),
                        const SizedBox(height: 16),

                        // Recent Events
                        _buildRecentEventsSection(),
                        const SizedBox(height: 32),
                      ],
                    ),
                  ),
                ),
              ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => controller.refreshData(),
        tooltip: 'Refresh',
        child: const Icon(Icons.refresh),
      ),
    );
  }

  /// Build overall effectiveness card
  Widget _buildEffectivenessCard() {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Overall Effectiveness',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 12),
            Obx(
              () => Column(
                children: [
                  LinearProgressIndicator(
                    value: controller.overallEffectiveness.value,
                    minHeight: 8,
                    backgroundColor: Colors.grey[300],
                    valueColor: AlwaysStoppedAnimation<Color>(
                      _getEffectivenessColor(controller.overallEffectiveness.value),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '${(controller.overallEffectiveness.value * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Build statistics row with key metrics
  Widget _buildStatisticsRow() {
    return Obx(
      () => Row(
        children: [
          Expanded(
            child: _buildStatCard(
              title: 'Updates',
              value: controller.updateCount.value.toString(),
              icon: Icons.update,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: _buildStatCard(
              title: 'Changes',
              value: (controller.statistics['recommendation_changes'] ?? 0).toString(),
              icon: Icons.change_circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: _buildStatCard(
              title: 'Improvements',
              value: (controller.statistics['effectiveness_improvements'] ?? 0).toString(),
              icon: Icons.trending_up,
            ),
          ),
        ],
      ),
    );
  }

  /// Build individual stat card
  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          children: [
            Icon(icon, size: 20, color: Colors.blue),
            const SizedBox(height: 4),
            Text(
              value,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
      ),
    );
  }

  /// Build recommendations section
  Widget _buildRecommendationsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'Recommendations',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
            Obx(
              () => Chip(
                label: Text('${controller.currentRecommendations.length} active'),
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Obx(
          () => controller.currentRecommendations.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Text(
                      'No recommendations yet',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ),
                )
              : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.currentRecommendations.length,
                  itemBuilder: (context, index) {
                    final rec = controller.currentRecommendations[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    rec.herbName,
                                    style: const TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ),
                                Chip(
                                  label: Text(
                                    '${(rec.predictedEffectiveness * 100).toStringAsFixed(0)}%',
                                    style: const TextStyle(color: Colors.white),
                                  ),
                                  backgroundColor: _getEffectivenessColor(rec.predictedEffectiveness),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            LinearProgressIndicator(
                              value: rec.predictedEffectiveness,
                              backgroundColor: Colors.grey[300],
                              valueColor: AlwaysStoppedAnimation<Color>(
                                _getEffectivenessColor(rec.predictedEffectiveness),
                              ),
                            ),
                            const SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  'Confidence: ${(rec.confidence * 100).toStringAsFixed(0)}%',
                                  style: TextStyle(fontSize: 12, color: Colors.grey[700]),
                                ),
                                Obx(
                                  () => Text(
                                    controller.getTrendIndicator(rec.recommendationId),
                                    style: const TextStyle(fontSize: 16),
                                  ),
                                ),
                              ],
                            ),
                            if (rec.reasoning.isNotEmpty) ...[
                              const SizedBox(height: 8),
                              Text(
                                rec.reasoning,
                                style: TextStyle(
                                  fontSize: 12,
                                  fontStyle: FontStyle.italic,
                                  color: Colors.grey[700],
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }

  /// Build effectiveness metrics section
  Widget _buildEffectivenessMetricsSection() {
    return Obx(
      () => controller.effectivenessMetrics.isEmpty
          ? const SizedBox.shrink()
          : Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Effectiveness Metrics',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                    ),
                    Chip(
                      label: Text('${controller.effectivenessMetrics.length} tracked'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.effectivenessMetrics.length,
                  itemBuilder: (context, index) {
                    final metric = controller.effectivenessMetrics[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      color: Colors.blue[50],
                      child: Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    metric.herbName,
                                    style: const TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ),
                                Text(
                                  controller.getTrendIndicator(metric.recommendationId),
                                  style: const TextStyle(fontSize: 16),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text('Effectiveness: ${(metric.effectivenessScore * 100).toStringAsFixed(1)}%'),
                                Text('Samples: ${metric.sampleSize}'),
                              ],
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Confidence: ${(metric.confidence * 100).toStringAsFixed(1)}%',
                              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ],
            ),
    );
  }

  /// Build recent events section
  Widget _buildRecentEventsSection() {
    return Obx(
      () => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'Recent Events',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
              ),
              GestureDetector(
                onTap: () => controller.recentEvents.clear(),
                child: const Chip(label: Text('Clear')),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Container(
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey[300]!),
              borderRadius: BorderRadius.circular(8),
            ),
            child: controller.recentEvents.isEmpty
                ? const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Center(child: Text('No events yet')),
                  )
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: controller.recentEvents.length,
                    itemBuilder: (context, index) {
                      final event = controller.recentEvents[index];
                      return Column(
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(12.0),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '●',
                                  style: TextStyle(color: Colors.blue[400]),
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    event,
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          if (index < controller.recentEvents.length - 1)
                            Divider(height: 1, color: Colors.grey[200]),
                        ],
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  /// Get color based on effectiveness score
  Color _getEffectivenessColor(double score) {
    if (score >= 0.75) return Colors.green;
    if (score >= 0.5) return Colors.amber;
    if (score >= 0.25) return Colors.orange;
    return Colors.red;
  }

  @override
  void dispose() {
    Get.delete<RealTimeDashboardController>();
    super.dispose();
  }
}
