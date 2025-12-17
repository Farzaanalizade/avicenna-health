import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class WearableService {
  static final WearableService _instance = WearableService._internal();

  factory WearableService() => _instance;

  WearableService._internal();

  /// Scan for Bluetooth wearables
  Future<List<BluetoothDevice>> scanForDevices(
      {Duration timeout = const Duration(seconds: 10)}) async {
    try {
      print('🔍 Scanning for Bluetooth devices...');

      // Initialize scan
      await FlutterBluePlus.startScan(timeout: timeout);

      List<BluetoothDevice> devices = [];

      // Collect scan results
      print('✅ Scan complete.');

      return devices;
    } catch (e) {
      print('❌ Scan error: $e');
      return [];
    }
  }

  /// Connect to device
  Future<bool> connectToDevice(BluetoothDevice device) async {
    try {
      print('🔗 Connecting to ${device.name}...');
      await device.connect();
      print('✅ Connected to ${device.name}');
      return true;
    } catch (e) {
      print('❌ Connection error: $e');
      return false;
    }
  }

  /// Get health data stub
  Future<HealthMetrics?> getHealthData() async {
    try {
      return HealthMetrics(
        heartRate: 75,
        spo2: 98,
        systolicBP: 120,
        diastolicBP: 80,
        temperature: 37.0,
        timestamp: DateTime.now(),
      );
    } catch (e) {
      print('❌ Health data error: $e');
      return null;
    }
  }
}

class HealthMetrics {
  final double heartRate;
  final double spo2;
  final double systolicBP;
  final double diastolicBP;
  final double temperature;
  final DateTime timestamp;

  HealthMetrics({
    required this.heartRate,
    required this.spo2,
    required this.systolicBP,
    required this.diastolicBP,
    required this.temperature,
    required this.timestamp,
  });

  bool get isHealthy {
    return heartRate >= 60 &&
        heartRate <= 100 &&
        spo2 >= 95 &&
        systolicBP >= 90 &&
        systolicBP <= 120 &&
        diastolicBP >= 60 &&
        diastolicBP <= 80 &&
        temperature >= 36.5 &&
        temperature <= 37.5;
  }
}
