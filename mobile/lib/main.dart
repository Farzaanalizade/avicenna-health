import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'lib/config/theme.dart';
import 'lib/config/routes.dart';
import 'lib/config/app_config.dart';
import 'lib/controllers/auth_controller.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize AppConfig
  await AppConfig.init();
  
  // Initialize GetX controllers
  Get.put(AuthController());
  
  runApp(const AvicentaApp());
}

class AvicentaApp extends StatelessWidget {
  const AvicentaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Avicenna Health',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      
      // RTL Support
      locale: const Locale('fa'),
      fallbackLocale: const Locale('en'),
      
      // Routes
      initialRoute: '/splash',
      getPages: AppRoutes.pages,
      
      // Settings
      debugShowCheckedModeBanner: false,
      enableLog: false,
    );
  }
}
