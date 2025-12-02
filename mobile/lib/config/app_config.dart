import 'package:flutter/material.dart';
import 'package:get_storage/get_storage.dart';

class AppConfig {
  static const String appName = 'Avicenna Health';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String apiBaseUrl = 'http://localhost:8000';
  static const Duration apiTimeout = Duration(seconds: 30);
  
  // App Settings
  static const bool debugMode = true;
  static const bool enableLogging = true;
  
  // Storage keys
  static const String storageBoxName = 'avicenna_health';

  static late GetStorage _storage;

  /// Initialize app configuration
  static Future<void> init() async {
    // Initialize GetStorage
    await GetStorage.init(storageBoxName);
    _storage = GetStorage(storageBoxName);

    if (debugMode) {
      debugPrint('✅ App Configuration Initialized');
      debugPrint('API Base URL: $apiBaseUrl');
      debugPrint('App Version: $appVersion');
    }
  }

  /// Get storage instance
  static GetStorage get storage => _storage;

  /// Save setting
  static Future<void> saveSetting(String key, dynamic value) async {
    await _storage.write(key, value);
    if (debugMode) {
      debugPrint('💾 Setting saved: $key = $value');
    }
  }

  /// Get setting
  static dynamic getSetting(String key, [dynamic defaultValue]) {
    return _storage.read(key) ?? defaultValue;
  }

  /// Remove setting
  static Future<void> removeSetting(String key) async {
    await _storage.remove(key);
  }

  /// Clear all settings
  static Future<void> clearAllSettings() async {
    await _storage.erase();
  }

  /// Get API URL for endpoint
  static String getApiUrl(String endpoint) {
    return '$apiBaseUrl$endpoint';
  }

  /// Get API headers
  static Map<String, String> getApiHeaders({String? token}) {
    final headers = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (token != null) {
      headers['Authorization'] = 'Bearer $token';
    }

    return headers;
  }
}
