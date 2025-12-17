import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../controllers/health_data_controller.dart';

class HealthDashboardScreen extends StatelessWidget {
  final controller = Get.put(HealthDataController());

  HealthDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Health Dashboard'),
        centerTitle: true,
        backgroundColor: Colors.green[700],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Health Status Cards
            _buildVitalCard(
              title: 'Heart Rate',
              unit: 'BPM',
              value: controller.heartRate,
              icon: Icons.favorite,
              color: Colors.red,
              normalRange: '60-100',
            ),
            const SizedBox(height: 12),
            _buildVitalCard(
              title: 'Blood Oxygen',
              unit: '%',
              value: controller.bloodOxygen,
              icon: Icons.air,
              color: Colors.blue,
              normalRange: '95-100',
            ),
            const SizedBox(height: 12),
            _buildVitalCard(
              title: 'Body Temperature',
              unit: '°C',
              value: controller.bodyTemperature,
              icon: Icons.thermostat,
              color: Colors.orange,
              normalRange: '36.5-37.5',
            ),
            const SizedBox(height: 24),
            // Audio Recording Section
            _buildSection(
              title: 'Audio Analysis',
              children: [
                _buildActionButton(
                  icon: Icons.favorite_border,
                  label: 'Record Heart Sound',
                  onPressed: controller.recordHeartSound,
                  isLoading: controller.isRecording,
                  color: Colors.red,
                ),
                const SizedBox(height: 12),
                _buildActionButton(
                  icon: Icons.air,
                  label: 'Record Breathing',
                  onPressed: controller.recordBreathingSound,
                  isLoading: controller.isRecording,
                  color: Colors.blue,
                ),
              ],
            ),
            const SizedBox(height: 24),
            // Tremor Analysis Section
            _buildSection(
              title: 'Tremor Analysis',
              children: [
                ElevatedButton.icon(
                  onPressed: controller.analyzeTremor,
                  icon: const Icon(Icons.analytics),
                  label: const Text('Analyze Tremor'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.purple,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
                const SizedBox(height: 12),
                Obx(() => Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.purple[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    'Severity: ${controller.tremorSeverity.value}',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.purple[700],
                    ),
                  ),
                )),
              ],
            ),
            const SizedBox(height: 24),
            // Wearable Section
            _buildSection(
              title: 'Wearable Device',
              children: [
                ElevatedButton.icon(
                  onPressed: controller.fetchWearableMetrics,
                  icon: const Icon(Icons.watch),
                  label: const Text('Sync Wearable Data'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.teal,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            // Sync Button
            ElevatedButton.icon(
              onPressed: controller.syncToBackend,
              icon: const Icon(Icons.cloud_upload),
              label: const Text('Sync All Data to Backend'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green[700],
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildVitalCard({
    required String title,
    required String unit,
    required RxDouble value,
    required IconData icon,
    required Color color,
    required String normalRange,
  }) {
    return Obx(() => Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withOpacity(0.2),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 32),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontSize: 14)),
                  const SizedBox(height: 4),
                  Text(
                    '${value.value.toStringAsFixed(1)} $unit',
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Normal: $normalRange',
                    style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ));
  }

  Widget _buildSection({
    required String title,
    required List<Widget> children,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        ...children,
      ],
    );
  }

  Widget _buildActionButton({
    required IconData icon,
    required String label,
    required VoidCallback onPressed,
    required RxBool isLoading,
    required Color color,
  }) {
    return Obx(() => ElevatedButton.icon(
      onPressed: isLoading.value ? null : onPressed,
      icon: isLoading.value
          ? const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Icon(icon),
      label: Text(label),
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        disabledBackgroundColor: Colors.grey,
        padding: const EdgeInsets.symmetric(vertical: 12),
      ),
    ));
  }
}
