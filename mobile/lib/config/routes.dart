import 'package:get/get.dart';
import '../screens/main_screen.dart';
import '../screens/splash_screen.dart';
import '../screens/diagnostic_screen.dart';
import '../screens/health/health_dashboard_screen.dart';
import '../screens/health/camera_preview_screen.dart';
import '../screens/personalized_plan_screen.dart';
import '../screens/analysis_results_screen.dart';

/// Route names for app navigation
class AppRoutes {
  // Main navigation
  static const String SPLASH = '/';
  static const String MAIN = '/main';
  static const String HOME = '/home';
  
  // Diagnosis related
  static const String DIAGNOSIS = '/diagnosis';
  static const String TONGUE_ANALYSIS = '/diagnosis/tongue';
  static const String EYE_ANALYSIS = '/diagnosis/eye';
  static const String FACE_ANALYSIS = '/diagnosis/face';
  static const String SKIN_ANALYSIS = '/diagnosis/skin';
  static const String ANALYSIS_RESULTS = '/diagnosis/results';
  static const String ANALYSIS_DETAILED = '/diagnosis/detailed';
  
  // Health tracking
  static const String HEALTH_DASHBOARD = '/health';
  static const String CAMERA_PREVIEW = '/camera';
  
  // Knowledge base
  static const String KNOWLEDGE_BASE = '/knowledge';
  static const String KNOWLEDGE_DISEASES = '/knowledge/diseases';
  static const String KNOWLEDGE_TREATMENTS = '/knowledge/treatments';
  static const String KNOWLEDGE_HERBS = '/knowledge/herbs';
  
  // Settings
  static const String SETTINGS = '/settings';
  static const String PROFILE = '/settings/profile';
  static const String API_CONFIG = '/settings/api';
  
  // Plan
  static const String PERSONALIZED_PLAN = '/plan';
}

/// All app pages with navigation configuration
class AppPages {
  static final pages = [
    // Splash
    GetPage(
      name: AppRoutes.SPLASH,
      page: () => const SplashScreen(),
    ),
    
    // Main navigation hub
    GetPage(
      name: AppRoutes.MAIN,
      page: () => const MainScreen(),
    ),
    
    // Diagnosis pages
    GetPage(
      name: AppRoutes.DIAGNOSIS,
      page: () => const DiagnosticScreen(),
      transition: Transition.rightToLeft,
    ),
    
    GetPage(
      name: AppRoutes.TONGUE_ANALYSIS,
      page: () => const CameraPreviewScreen(
        analysisType: 'tongue',
        title: 'Tongue Analysis',
      ),
      transition: Transition.cupertino,
    ),
    
    GetPage(
      name: AppRoutes.EYE_ANALYSIS,
      page: () => const CameraPreviewScreen(
        analysisType: 'eye',
        title: 'Eye Analysis',
      ),
      transition: Transition.cupertino,
    ),
    
    GetPage(
      name: AppRoutes.FACE_ANALYSIS,
      page: () => const CameraPreviewScreen(
        analysisType: 'face',
        title: 'Face Analysis',
      ),
      transition: Transition.cupertino,
    ),
    
    GetPage(
      name: AppRoutes.SKIN_ANALYSIS,
      page: () => const CameraPreviewScreen(
        analysisType: 'skin',
        title: 'Skin Analysis',
      ),
      transition: Transition.cupertino,
    ),
    
    // Analysis Results Screen
    GetPage(
      name: AppRoutes.ANALYSIS_DETAILED,
      page: () {
        final diagnosisId = Get.arguments as int?;
        if (diagnosisId == null) {
          return const Scaffold(
            body: Center(child: Text('Invalid diagnosis ID')),
          );
        }
        return AnalysisResultsScreen(diagnosisId: diagnosisId);
      },
      transition: Transition.rightToLeft,
    ),
    
    // Health dashboard
    GetPage(
      name: AppRoutes.HEALTH_DASHBOARD,
      page: () => const HealthDashboardScreen(),
      transition: Transition.rightToLeft,
    ),
    
    // Camera preview
    GetPage(
      name: AppRoutes.CAMERA_PREVIEW,
      page: () => const CameraPreviewScreen(
        analysisType: 'general',
        title: 'Camera',
      ),
      transition: Transition.fadeIn,
    ),
    
    // Personalized plan
    GetPage(
      name: AppRoutes.PERSONALIZED_PLAN,
      page: () => const PersonalizedPlanScreen(),
      transition: Transition.rightToLeft,
    ),
  ];
}

/// Helper extension for easier navigation
extension NavigationHelper on GetxController {
  /// Navigate to tongue analysis
  void goToTongueAnalysis() => Get.toNamed(AppRoutes.TONGUE_ANALYSIS);
  
  /// Navigate to eye analysis
  void goToEyeAnalysis() => Get.toNamed(AppRoutes.EYE_ANALYSIS);
  
  /// Navigate to face analysis
  void goToFaceAnalysis() => Get.toNamed(AppRoutes.FACE_ANALYSIS);
  
  /// Navigate to skin analysis
  void goToSkinAnalysis() => Get.toNamed(AppRoutes.SKIN_ANALYSIS);
  
  /// Navigate to analysis results
  void goToAnalysisResults(int diagnosisId) => 
      Get.toNamed(AppRoutes.ANALYSIS_DETAILED, arguments: diagnosisId);
  
  /// Navigate to health dashboard
  void goToHealthDashboard() => Get.toNamed(AppRoutes.HEALTH_DASHBOARD);
  
  /// Navigate to personalized plan
  void goToPersonalizedPlan() => Get.toNamed(AppRoutes.PERSONALIZED_PLAN);
  
  /// Navigate back
  void goBack() => Get.back();
  
  /// Navigate to main
  void goToMain() => Get.offAllNamed(AppRoutes.MAIN);
}
