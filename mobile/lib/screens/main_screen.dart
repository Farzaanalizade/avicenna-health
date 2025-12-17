import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/camera_controller.dart';
import '../config/routes.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final CameraController controller = Get.put(CameraController());
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🏥 Avicenna Health'),
        centerTitle: true,
        backgroundColor: Colors.green[700],
        elevation: 0,
      ),
      body: _buildBody(),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() => _selectedIndex = index);
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.camera_alt),
            label: 'Diagnosis',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.favorite),
            label: 'Health',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.sync),
            label: 'Sync',
          ),
        ],
      ),
    );
  }

  Widget _buildBody() {
    switch (_selectedIndex) {
      case 0:
        return _buildHomeScreen();
      case 1:
        return _buildDiagnosisScreen();
      case 2:
        return _buildHealthScreen();
      case 3:
        return _buildSyncScreen();
      default:
        return _buildHomeScreen();
    }
  }

  Widget _buildHomeScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Card(
            color: Colors.green[50],
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Welcome to Avicenna',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                      color: Colors.green[900],
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Your personal AI health assistant powered by Persian, Chinese & Indian medicine',
                    style: TextStyle(fontSize: 14),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 32),
          
          // Quick Actions
          Text(
            'Quick Actions',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          _buildQuickActionGrid(context),
          const SizedBox(height: 32),
          
          // Recent Activity
          Text(
            'Recent Activity',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Obx(() => controller.capturedImages.isEmpty
              ? Container(
                  padding: const EdgeInsets.symmetric(vertical: 24),
                  child: Center(
                    child: Column(
                      children: [
                        Icon(Icons.history, size: 48, color: Colors.grey[400]),
                        const SizedBox(height: 16),
                        Text(
                          'No recent activity',
                          style: TextStyle(color: Colors.grey[600]),
                        ),
                      ],
                    ),
                  ),
                )
              : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.capturedImages.length,
                  itemBuilder: (context, index) {
                    final image = controller.capturedImages[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: Icon(
                          _getAnalysisIcon(image.type.toString()),
                          color: Colors.green[700],
                        ),
                        title: Text('${image.type.name} Analysis'),
                        subtitle: Text(image.captureTime.toString()),
                        trailing: image.uploaded
                            ? const Icon(Icons.cloud_done, color: Colors.green)
                            : const Icon(Icons.cloud_off, color: Colors.grey),
                      ),
                    );
                  },
                )),
        ],
      ),
    );
  }

  Widget _buildQuickActionGrid(BuildContext context) {
    return GridView.count(
      crossAxisCount: 2,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      children: [
        _buildQuickActionCard(
          icon: Icons.tongue,
          label: 'Tongue',
          color: Colors.red,
          onTap: () => Get.toNamed(AppRoutes.TONGUE_ANALYSIS),
        ),
        _buildQuickActionCard(
          icon: Icons.visibility,
          label: 'Eyes',
          color: Colors.blue,
          onTap: () => Get.toNamed(AppRoutes.EYE_ANALYSIS),
        ),
        _buildQuickActionCard(
          icon: Icons.face,
          label: 'Face',
          color: Colors.orange,
          onTap: () => Get.toNamed(AppRoutes.FACE_ANALYSIS),
        ),
        _buildQuickActionCard(
          icon: Icons.hand_sanitizer,
          label: 'Skin',
          color: Colors.purple,
          onTap: () => Get.toNamed(AppRoutes.SKIN_ANALYSIS),
        ),
      ],
    );
  }

  Widget _buildQuickActionCard({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [color.withOpacity(0.3), color.withOpacity(0.1)],
            ),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 48, color: color),
              const SizedBox(height: 12),
              Text(
                label,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: color,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDiagnosisScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Health Analysis',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          
          // Analysis Grid
          GridView.count(
            crossAxisCount: 2,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            children: [
              _buildAnalysisCard(
                icon: Icons.tongue,
                title: 'Tongue',
                subtitle: 'Visual Analysis',
                onTap: () => Get.toNamed(AppRoutes.TONGUE_ANALYSIS),
              ),
              _buildAnalysisCard(
                icon: Icons.visibility,
                title: 'Eyes',
                subtitle: 'Eye Diagnosis',
                onTap: () => Get.toNamed(AppRoutes.EYE_ANALYSIS),
              ),
              _buildAnalysisCard(
                icon: Icons.face,
                title: 'Face',
                subtitle: 'Face Analysis',
                onTap: () => Get.toNamed(AppRoutes.FACE_ANALYSIS),
              ),
              _buildAnalysisCard(
                icon: Icons.hand_sanitizer,
                title: 'Skin',
                subtitle: 'Skin Condition',
                onTap: () => Get.toNamed(AppRoutes.SKIN_ANALYSIS),
              ),
            ],
          ),
          
          const SizedBox(height: 32),
          Text(
            'Captured Images',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Obx(() => controller.capturedImages.isEmpty
              ? Center(
                  child: Column(
                    children: [
                      Icon(Icons.image, size: 48, color: Colors.grey[400]),
                      const SizedBox(height: 16),
                      const Text('No images captured yet'),
                    ],
                  ),
                )
              : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.capturedImages.length,
                  itemBuilder: (context, index) {
                    final image = controller.capturedImages[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: const Icon(Icons.image),
                        title: Text('${image.type.name} Image'),
                        subtitle: Text(image.captureTime.toString()),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete),
                          onPressed: () {
                            // Delete functionality
                          },
                        ),
                      ),
                    );
                  },
                )),
        ],
      ),
    );
  }

  Widget _buildAnalysisCard({
    required IconData icon,
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            color: Colors.white,
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: Colors.green[700]),
              const SizedBox(height: 12),
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                subtitle,
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHealthScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Health Dashboard',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Overall Health Status',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 16),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: LinearProgressIndicator(
                      value: 0.75,
                      minHeight: 10,
                      backgroundColor: Colors.grey[300],
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.green[700]!),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Good Health Status',
                    style: TextStyle(color: Colors.green[700]),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Text(
            'Recent Analyses',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 16),
          _buildHealthInfoCard(
            title: 'Tongue Analysis',
            subtitle: '2 hours ago',
            status: 'Normal',
            icon: Icons.check_circle,
          ),
          _buildHealthInfoCard(
            title: 'Eye Analysis',
            subtitle: '1 day ago',
            status: 'Needs Attention',
            icon: Icons.warning,
          ),
          _buildHealthInfoCard(
            title: 'Skin Analysis',
            subtitle: '3 days ago',
            status: 'Good',
            icon: Icons.check_circle,
          ),
        ],
      ),
    );
  }

  Widget _buildHealthInfoCard({
    required String title,
    required String subtitle,
    required String status,
    required IconData icon,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(icon, color: Colors.green[700]),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: Text(
          status,
          style: TextStyle(
            color: status == 'Good' || status == 'Normal'
                ? Colors.green[700]
                : Colors.orange[700],
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  Widget _buildSyncScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Data Sync',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Obx(() => Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Sync Status',
                            style: Theme.of(context).textTheme.titleSmall,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            controller.syncStatus.value,
                            style: TextStyle(
                              fontSize: 16,
                              color: Colors.green[700],
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                      Icon(
                        Icons.cloud_done,
                        size: 40,
                        color: Colors.green[700],
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: controller.syncAllImages,
                      icon: const Icon(Icons.cloud_upload),
                      label: const Text('Sync All Data'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green[700],
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          )),
          const SizedBox(height: 24),
          Text(
            'Sync History',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 16),
          _buildSyncHistoryCard('Patient Data', '2 hours ago', true),
          _buildSyncHistoryCard('Analysis Results', '1 day ago', true),
          _buildSyncHistoryCard('Health Records', 'Pending', false),
        ],
      ),
    );
  }

  Widget _buildSyncHistoryCard(String title, String time, bool synced) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(
          synced ? Icons.check_circle : Icons.schedule,
          color: synced ? Colors.green : Colors.orange,
        ),
        title: Text(title),
        subtitle: Text(time),
      ),
    );
  }

  IconData _getAnalysisIcon(String type) {
    if (type.contains('TONGUE')) return Icons.tongue;
    if (type.contains('EYE')) return Icons.visibility;
    if (type.contains('FACE')) return Icons.face;
    if (type.contains('SKIN')) return Icons.hand_sanitizer;
    return Icons.image;
  }
            'Pending Sync',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 12),
          Obx(() => Text(
              '${controller.capturedImages.length} images waiting to sync')),
        ],
      ),
    );
  }

  Widget _buildQuickActionGrid() {
    return GridView.count(
      crossAxisCount: 2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      children: [
        _buildQuickActionCard(
          title: 'Tongue',
          icon: Icons.image,
          color: Colors.red,
          onTap: () => _captureAndNavigate('TONGUE'),
        ),
        _buildQuickActionCard(
          title: 'Eyes',
          icon: Icons.remove_red_eye,
          color: Colors.blue,
          onTap: () => _captureAndNavigate('EYE'),
        ),
        _buildQuickActionCard(
          title: 'Face',
          icon: Icons.face,
          color: Colors.orange,
          onTap: () => _captureAndNavigate('FACE'),
        ),
        _buildQuickActionCard(
          title: 'Skin',
          icon: Icons.healing,
          color: Colors.purple,
          onTap: () => _captureAndNavigate('SKIN'),
        ),
      ],
    );
  }

  Widget _buildAnalysisGrid() {
    return GridView.count(
      crossAxisCount: 2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      children: [
        _buildAnalysisCard(
          title: 'Tongue',
          icon: Icons.image,
          color: Colors.red,
          onTap: () => _captureAndNavigate('TONGUE'),
        ),
        _buildAnalysisCard(
          title: 'Eyes',
          icon: Icons.remove_red_eye,
          color: Colors.blue,
          onTap: () => _captureAndNavigate('EYE'),
        ),
        _buildAnalysisCard(
          title: 'Face',
          icon: Icons.face,
          color: Colors.orange,
          onTap: () => _captureAndNavigate('FACE'),
        ),
        _buildAnalysisCard(
          title: 'Skin',
          icon: Icons.healing,
          color: Colors.purple,
          onTap: () => _captureAndNavigate('SKIN'),
        ),
      ],
    );
  }

  void _captureAndNavigate(String imageType) {
    Get.to(
      () => CameraPreviewScreen(analysisType: imageType),
    );
  }

  Widget _buildQuickActionCard({
    required String title,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [color.withOpacity(0.1), color.withOpacity(0.05)],
            ),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: color, size: 40),
              const SizedBox(height: 12),
              Text(
                title,
                style: TextStyle(
                  fontWeight: FontWeight.w600,
                  color: color,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAnalysisCard({
    required String title,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color, width: 2),
          color: color.withOpacity(0.05),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 44),
            const SizedBox(height: 12),
            Text(
              'Analyze $title',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontWeight: FontWeight.w600,
                color: color,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
