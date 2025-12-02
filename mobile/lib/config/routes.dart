import 'package:get/get.dart';
import '../screens/splash_screen.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/home/home_screen.dart';
import '../screens/capture/tongue_capture_screen.dart';
import '../screens/capture/eye_capture_screen.dart';
import '../screens/capture/vitals_input_screen.dart';
import '../screens/report/quick_check_screen.dart';
import '../screens/history/health_history_screen.dart';
import '../screens/device/device_connect_screen.dart';

class AppRoutes {
  static const String splash = '/splash';
  static const String login = '/login';
  static const String register = '/register';
  static const String home = '/home';
  static const String tonguCapture = '/tongue-capture';
  static const String eyeCapture = '/eye-capture';
  static const String vitalsInput = '/vitals-input';
  static const String quickCheck = '/quick-check';
  static const String healthHistory = '/health-history';
  static const String deviceConnect = '/device-connect';

  static final pages = [
    GetPage(
      name: splash,
      page: () => const SplashScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: login,
      page: () => const LoginScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: register,
      page: () => const RegisterScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: home,
      page: () => const HomeScreen(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: tonguCapture,
      page: () => const TongueCaptureScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: eyeCapture,
      page: () => const EyeCaptureScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: vitalsInput,
      page: () => const VitalsInputScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: quickCheck,
      page: () => const QuickCheckScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: healthHistory,
      page: () => const HealthHistoryScreen(),
      transition: Transition.rightToLeft,
    ),
    GetPage(
      name: deviceConnect,
      page: () => const DeviceConnectScreen(),
      transition: Transition.rightToLeft,
    ),
  ];
}
