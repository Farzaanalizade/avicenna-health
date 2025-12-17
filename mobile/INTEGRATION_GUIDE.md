# راهنمای Integration Mobile-Backend

## نقشه Screens و Endpoints

### Diagnostic Screen
```
┌─────────────────────────────┐
│  Diagnostic Screen          │
├─────────────────────────────┤
│ [Pulse] [Urine] [Tongue]   │
├─────────────────────────────┤
│                             │
│ Pulse Tab:                  │
│ - Rate: 60-150 bpm          │
│ - Type: [دقیق/نرم/...]     │
│ - Rhythm: [منتظم/نامنتظم]  │
│                             │
│ [Submit] → POST /diagnosis  │
│                             │
└─────────────────────────────┘
```

**API Endpoint**:
```
POST /api/v1/diagnosis/pulse
POST /api/v1/diagnosis/urine
POST /api/v1/diagnosis/tongue
```

### Results Screen
```
┌─────────────────────────────┐
│  Analysis Results           │
├─────────────────────────────┤
│ Mizaj: [Garm-Khoshk]        │
│ Status: [Salamat/Bemari]    │
│                             │
│ Remedies:                   │
│ - [Remedy 1]                │
│ - [Remedy 2]                │
│                             │
│ Lifestyle:                  │
│ - [Advice 1]                │
│ - [Advice 2]                │
│                             │
│ [View Details] → GET /report│
│                             │
└─────────────────────────────┘
```

**API Endpoint**:
```
GET /api/v1/analysis/comprehensive/{patient_id}
GET /api/v1/diagnosis/report/patient/{patient_id}
```

### Personalized Plan Screen
```
┌─────────────────────────────┐
│  3-Phase Treatment Plan     │
├─────────────────────────────┤
│ Phase 1: [========] 10 days │
│ - Cleansing                 │
│                             │
│ Phase 2: [======] 20 days   │
│ - Balancing                 │
│                             │
│ Phase 3: [====] 30 days     │
│ - Maintenance               │
│                             │
│ [Get Details]               │
│                             │
└─────────────────────────────┘
```

**API Endpoint**:
```
GET /api/v1/analysis/personalized-plan/{patient_id}
```

### Weekly Schedule Screen
```
┌─────────────────────────────┐
│  Weekly Routine             │
├─────────────────────────────┤
│ Saturday:                   │
│ ┌─────────────────────────┐ │
│ │ Morning: [Routine 1]    │ │
│ │ Midday: [Routine 2]     │ │
│ │ Evening: [Routine 3]    │ │
│ │ Night: [Routine 4]      │ │
│ └─────────────────────────┘ │
│                             │
│ [Sunday] [Monday] ...       │
│                             │
└─────────────────────────────┘
```

**API Endpoint**:
```
GET /api/v1/analysis/weekly-schedule/{patient_id}
```

---

## Flutter Code Examples

### 1. API Service Class

```dart
// lib/services/api_service.dart

import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  // Diagnostic Endpoints
  static Future<Map<String, dynamic>> submitPulseAnalysis(
    int patientId,
    Map<String, dynamic> pulseData,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/diagnosis/pulse'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'patient_id': patientId,
        ...pulseData,
      }),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit pulse analysis');
    }
  }

  static Future<Map<String, dynamic>> submitUrineAnalysis(
    int patientId,
    Map<String, dynamic> urineData,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/diagnosis/urine'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'patient_id': patientId,
        ...urineData,
      }),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit urine analysis');
    }
  }

  static Future<Map<String, dynamic>> submitTongueAnalysis(
    int patientId,
    Map<String, dynamic> tongueData,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/diagnosis/tongue'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'patient_id': patientId,
        ...tongueData,
      }),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit tongue analysis');
    }
  }

  // Analysis Endpoints
  static Future<Map<String, dynamic>> getComprehensiveAnalysis(
    int patientId,
  ) async {
    final response = await http.get(
      Uri.parse('$baseUrl/analysis/comprehensive/$patientId'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get analysis');
    }
  }

  static Future<Map<String, dynamic>> getPersonalizedPlan(
    int patientId,
  ) async {
    final response = await http.get(
      Uri.parse('$baseUrl/analysis/personalized-plan/$patientId'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get personalized plan');
    }
  }

  static Future<Map<String, dynamic>> getWeeklySchedule(
    int patientId,
  ) async {
    final response = await http.get(
      Uri.parse('$baseUrl/analysis/weekly-schedule/$patientId'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get weekly schedule');
    }
  }

  static Future<Map<String, dynamic>> getDietaryPlan(
    int patientId,
  ) async {
    final response = await http.get(
      Uri.parse('$baseUrl/analysis/dietary-plan/$patientId'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get dietary plan');
    }
  }

  static Future<Map<String, dynamic>> getFullReport(
    int patientId,
  ) async {
    final response = await http.get(
      Uri.parse('$baseUrl/analysis/full-report/$patientId'),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to get full report');
    }
  }
}
```

### 2. Diagnostic Controller

```dart
// lib/controllers/diagnostic_controller.dart

import 'package:get/get.dart';
import 'package:avicenna/services/api_service.dart';

class DiagnosticController extends GetxController {
  // Observable variables
  var pulseRate = 72.obs;
  var urineColor = 'zard'.obs;
  var tongueColor = 'pink'.obs;
  var mizajResult = ''.obs;
  var isLoading = false.obs;
  var errorMessage = ''.obs;

  int patientId = 1; // Should come from auth/patient selection

  // Submit pulse analysis
  Future<void> submitPulseAnalysis(String pulseType, String rhythm) async {
    try {
      isLoading.value = true;
      await ApiService.submitPulseAnalysis(
        patientId,
        {
          'pulse_rate': pulseRate.value,
          'type': pulseType,
          'rhythm': rhythm,
        },
      );
      Get.snackbar('موفقیت', 'نبض ثبت شد');
    } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', e.toString());
    } finally {
      isLoading.value = false;
    }
  }

  // Submit urine analysis
  Future<void> submitUrineAnalysis(String clarity) async {
    try {
      isLoading.value = true;
      await ApiService.submitUrineAnalysis(
        patientId,
        {
          'color': urineColor.value,
          'clarity': clarity,
        },
      );
      Get.snackbar('موفقیت', 'ادرار ثبت شد');
    } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', e.toString());
    } finally {
      isLoading.value = false;
    }
  }

  // Submit tongue analysis
  Future<void> submitTongueAnalysis(String coating) async {
    try {
      isLoading.value = true;
      await ApiService.submitTongueAnalysis(
        patientId,
        {
          'body_color': tongueColor.value,
          'coating_thickness': coating,
        },
      );
      Get.snackbar('موفقیت', 'زبان ثبت شد');
    } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', e.toString());
    } finally {
      isLoading.value = false;
    }
  }

  // Get comprehensive analysis
  Future<void> getComprehensiveAnalysis() async {
    try {
      isLoading.value = true;
      final result = await ApiService.getComprehensiveAnalysis(patientId);
      mizajResult.value = result['dominant_mizaj'] ?? 'نامعلوم';
      Get.snackbar('موفقیت', 'تحلیل انجام شد');
    } catch (e) {
      errorMessage.value = e.toString();
      Get.snackbar('خطا', e.toString());
    } finally {
      isLoading.value = false;
    }
  }
}
```

### 3. Diagnostic Screen Integration

```dart
// Update lib/screens/diagnostic_screen.dart

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:avicenna/controllers/diagnostic_controller.dart';

class DiagnosticScreen extends StatelessWidget {
  final controller = Get.put(DiagnosticController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('تشخیص طبی'),
      ),
      body: Obx(
        () => controller.isLoading.value
            ? Center(child: CircularProgressIndicator())
            : SingleChildScrollView(
                child: Padding(
                  padding: EdgeInsets.all(16),
                  child: Column(
                    children: [
                      // Pulse Tab
                      _buildPulseSection(context),
                      SizedBox(height: 20),
                      
                      // Urine Tab
                      _buildUrineSection(context),
                      SizedBox(height: 20),
                      
                      // Tongue Tab
                      _buildTongueSection(context),
                      SizedBox(height: 20),
                      
                      // Submit Button
                      ElevatedButton(
                        onPressed: () async {
                          await controller.getComprehensiveAnalysis();
                        },
                        child: Text('تحلیل جامع'),
                      ),
                      
                      // Results
                      if (controller.mizajResult.value.isNotEmpty)
                        Padding(
                          padding: EdgeInsets.only(top: 20),
                          child: Card(
                            child: Padding(
                              padding: EdgeInsets.all(16),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text('نتیجه تشخیص:'),
                                  SizedBox(height: 10),
                                  Text(controller.mizajResult.value,
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                      )),
                                ],
                              ),
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
      ),
    );
  }

  Widget _buildPulseSection(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('تحلیل نبض', style: TextStyle(fontSize: 18)),
            SizedBox(height: 10),
            Slider(
              value: controller.pulseRate.value.toDouble(),
              min: 40,
              max: 150,
              onChanged: (value) {
                controller.pulseRate.value = value.toInt();
              },
            ),
            Text('نبض: ${controller.pulseRate.value} bpm'),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                controller.submitPulseAnalysis('daqiq', 'montazem');
              },
              child: Text('ثبت نبض'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUrineSection(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('تحلیل ادرار', style: TextStyle(fontSize: 18)),
            SizedBox(height: 10),
            DropdownButton<String>(
              value: controller.urineColor.value,
              onChanged: (value) {
                controller.urineColor.value = value!;
              },
              items: ['zard', 'ghermez', 'siyah', 'roshan']
                  .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                  .toList(),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                controller.submitUrineAnalysis('roshan');
              },
              child: Text('ثبت ادرار'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTongueSection(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('تحلیل زبان', style: TextStyle(fontSize: 18)),
            SizedBox(height: 10),
            DropdownButton<String>(
              value: controller.tongueColor.value,
              onChanged: (value) {
                controller.tongueColor.value = value!;
              },
              items: ['pink', 'sorkh', 'safid']
                  .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                  .toList(),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                controller.submitTongueAnalysis('nazar');
              },
              child: Text('ثبت زبان'),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## Configuration

### app_config.dart
```dart
class AppConfig {
  // API Configuration
  static const String apiBaseUrl = 'http://localhost:8000/api/v1';
  static const int apiTimeoutSeconds = 30;
  
  // Patient Configuration
  static const int defaultPatientId = 1;
  
  // UI Configuration
  static const bool isDebugMode = true;
  
  // Languages
  static const List<String> supportedLanguages = ['fa', 'en'];
}
```

---

## Testing Integration

### Test Diagnostic Flow
```dart
void main() {
  test('Submit pulse and get analysis', () async {
    // 1. Submit pulse
    var pulseResult = await ApiService.submitPulseAnalysis(1, {
      'pulse_rate': 72,
      'type': 'daqiq',
      'rhythm': 'montazem',
    });
    expect(pulseResult['id'], isNotNull);

    // 2. Get analysis
    var analysis = await ApiService.getComprehensiveAnalysis(1);
    expect(analysis['dominant_mizaj'], isNotEmpty);
  });
}
```

---

## استقرار و بهینه‌سازی

### Backend Server چک‌لیست
- [ ] Database اولیه‌سازی شده
- [ ] Seed Data اجرا شده
- [ ] API Endpoints تست شده
- [ ] CORS تنظیم شده

### Mobile App چک‌لیست
- [ ] API Service تنظیم شده
- [ ] Controllers ایجاد شده
- [ ] Screens UI تنظیم شده
- [ ] Data Flow تست شده

---

## دیباگینگ و مشکل‌یابی

### API Connection Issues
```dart
// Check API connectivity
Future<bool> checkApiConnection() async {
  try {
    final response = await http.get(
      Uri.parse('${ApiService.baseUrl}/diseases'),
    ).timeout(Duration(seconds: 5));
    return response.statusCode == 200;
  } catch (e) {
    print('Connection error: $e');
    return false;
  }
}
```

### Logging
```dart
// Enable debug logs
import 'package:logger/logger.dart';

final logger = Logger();

logger.d('Debug message');
logger.i('Info message');
logger.w('Warning message');
logger.e('Error message');
```

---

## منابع

- [Flutter HTTP Package](https://pub.dev/packages/http)
- [GetX State Management](https://github.com/jonataslaw/getx)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
