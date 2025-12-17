import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/camera_controller.dart';
import '../screens/health/camera_preview_screen.dart';

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
            label: 'Camera',
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
        return _buildCameraScreen();
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
          Text(
            'Welcome to Avicenna',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          const Text(
            'Your personal AI health assistant powered by Persian medicine',
          ),
          const SizedBox(height: 32),
          Text(
            'Quick Actions',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          _buildQuickActionGrid(),
          const SizedBox(height: 32),
          Text(
            'Recent Activity',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Obx(() => controller.capturedImages.isEmpty
              ? const Text('No recent activity')
              : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.capturedImages.length,
                  itemBuilder: (context, index) {
                    final image = controller.capturedImages[index];
                    return ListTile(
                      title: Text('${image.type.name} captured'),
                      subtitle: Text(image.captureTime.toString()),
                      trailing:
                          image.uploaded ? const Icon(Icons.check) : null,
                    );
                  },
                )),
        ],
      ),
    );
  }

  Widget _buildCameraScreen() {
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
          _buildAnalysisGrid(),
          const SizedBox(height: 32),
          Text(
            'Captured Images',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 16),
          Obx(() => controller.capturedImages.isEmpty
              ? const Text('No images captured yet')
              : ListView.builder(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: controller.capturedImages.length,
                  itemBuilder: (context, index) {
                    final image = controller.capturedImages[index];
                    return Card(
                      child: ListTile(
                        leading: const Icon(Icons.image),
                        title: Text('${image.type.name} Image'),
                        subtitle: Text(image.captureTime.toString()),
                      ),
                    );
                  },
                )),
        ],
      ),
    );
  }

  Widget _buildHealthScreen() {
    return const Center(
      child: Text('Health Dashboard (Coming Soon)'),
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
                  Text('Status: ${controller.syncStatus.value}'),
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
