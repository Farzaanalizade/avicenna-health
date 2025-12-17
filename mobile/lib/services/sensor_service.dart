import 'package:sensors_plus/sensors_plus.dart';
import 'dart:io';

class SensorService {
  static final SensorService _instance = SensorService._internal();

  factory SensorService() => _instance;

  SensorService._internal();

  /// Record heart sound (stub - returns mock data)
  Future<File?> recordHeartSound(
      {Duration duration = const Duration(seconds: 30)}) async {
    try {
      print('🔴 Recording heart sound...');
      await Future.delayed(duration);
      print('✅ Heart sound recorded');
      return null; // Stub implementation
    } catch (e) {
      print('❌ Heart sound recording error: $e');
      return null;
    }
  }

  /// Record breathing sound (stub)
  Future<File?> recordBreathingSound(
      {Duration duration = const Duration(seconds: 20)}) async {
    try {
      print('🔴 Recording breathing sound...');
      await Future.delayed(duration);
      print('✅ Breathing sound recorded');
      return null; // Stub implementation
    } catch (e) {
      print('❌ Breathing recording error: $e');
      return null;
    }
  }

  /// Monitor tremor via gyroscope
  Future<TremorAnalysis> analyzeTremor(
      {Duration duration = const Duration(seconds: 10)}) async {
    try {
      List<double> readings = [];
      final stopwatch = Stopwatch()..start();

      await for (final event in gyroscopeEvents) {
        if (stopwatch.elapsed >= duration) break;

        // Calculate magnitude
        double magnitude = (event.x.abs() + event.y.abs() + event.z.abs()) / 3;
        readings.add(magnitude);
      }

      stopwatch.stop();

      if (readings.isEmpty) {
        return TremorAnalysis(
          severity: 'none',
          confidence: 0.0,
          averageMagnitude: 0.0,
        );
      }

      double average = readings.reduce((a, b) => a + b) / readings.length;
      double max = readings.reduce((a, b) => a > b ? a : b);

      String severity;
      if (average < 0.1) {
        severity = 'none';
      } else if (average < 0.3)
        severity = 'mild';
      else if (average < 0.7)
        severity = 'moderate';
      else
        severity = 'severe';

      return TremorAnalysis(
        severity: severity,
        confidence: 0.85,
        averageMagnitude: average,
        maxMagnitude: max,
      );
    } catch (e) {
      print('❌ Tremor analysis error: $e');
      return TremorAnalysis(severity: 'error', confidence: 0.0);
    }
  }

  /// Get accelerometer data
  Future<AccelerometerData> getMovementData(
      {Duration duration = const Duration(seconds: 5)}) async {
    try {
      List<double> xValues = [];
      List<double> yValues = [];
      List<double> zValues = [];

      final stopwatch = Stopwatch()..start();

      await for (final event in accelerometerEvents) {
        if (stopwatch.elapsed >= duration) break;

        xValues.add(event.x);
        yValues.add(event.y);
        zValues.add(event.z);
      }

      return AccelerometerData(
        xAverage: xValues.isEmpty ? 0 : xValues.reduce((a, b) => a + b) / xValues.length,
        yAverage: yValues.isEmpty ? 0 : yValues.reduce((a, b) => a + b) / yValues.length,
        zAverage: zValues.isEmpty ? 0 : zValues.reduce((a, b) => a + b) / zValues.length,
      );
    } catch (e) {
      print('❌ Accelerometer error: $e');
      return AccelerometerData();
    }
  }
}

class TremorAnalysis {
  final String severity;
  final double confidence;
  final double averageMagnitude;
  final double? maxMagnitude;

  TremorAnalysis({
    required this.severity,
    required this.confidence,
    this.averageMagnitude = 0.0,
    this.maxMagnitude,
  });
}

class AccelerometerData {
  final double xAverage;
  final double yAverage;
  final double zAverage;

  AccelerometerData({
    this.xAverage = 0.0,
    this.yAverage = 0.0,
    this.zAverage = 0.0,
  });
}
