import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'config/routes.dart';
import 'config/theme.dart';
import 'database/app_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize database
  await AppDatabase().database;

  runApp(const AvicentaApp());
}

class AvicentaApp extends StatelessWidget {
  const AvicentaApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: '🏥 Avicenna Health',
      theme: AppTheme.lightTheme,
      debugShowCheckedModeBanner: false,
      
      // Use named routes
      initialRoute: AppRoutes.SPLASH,
      getPages: AppPages.pages,
      
      // Global navigation settings
      navigatorObservers: [
        GetNavigatorObserver(),
      ],
    );
  }
}
