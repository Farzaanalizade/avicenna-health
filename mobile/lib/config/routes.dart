import 'package:get/get.dart';
import '../screens/main_screen.dart';

class AppRoutes {
  static const String MAIN = '/main';

  static final pages = [
    GetPage(
      name: MAIN,
      page: () => const MainScreen(),
    ),
  ];
}
