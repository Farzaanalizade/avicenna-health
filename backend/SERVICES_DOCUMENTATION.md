# سرویس‌های تحلیل و توصیه - مستندات کامل

## مقدمه

این سرویس‌ها برای ارائه تحلیل خودکار و توصیه‌های شخصی‌شده براساس اصول تعاليم ابوعلی سینا طراحی شده‌اند.

## سرویس‌های اصلی

### 1. AvicennaAnalysisEngine - موتور تحلیل

#### تحلیل نبض
```python
analysis = AvicennaAnalysisEngine.analyze_pulse(pulse_object, db)
```

**خروجی:**
- `scores`: امتیازات مزاج‌ها (garm, sard, tar, khoshk)
- `dominant_mizaj`: مزاج غالب
- `confidence`: درجه اطمینان (0-1)
- `assessment`: ارزیابی وضعیت

**نقاط تجزیه تحلیلی:**
- نوع نبض (بزرگ، کوچک، سریع، آهسته)
- قوت و ریتم
- دما
- عمق و عرض
- مکان

#### تحلیل ادرار
```python
analysis = AvicennaAnalysisEngine.analyze_urine(urine_object, db)
```

**خروجی:**
- `scores`: امتیازات مزاج‌ها
- `dominant_mizaj`: مزاج غالب
- `health_status`: وضعیت سلامت

**نقاط تجزیه تحلیلی:**
- رنگ (زرد = گرم، سفید = سرد)
- چگالی (سنگین = گرم، سبک = سرد)
- شفافیت و رسوب
- پروتئین و قند

#### تحلیل زبان
```python
analysis = AvicennaAnalysisEngine.analyze_tongue(tongue_object, db)
```

**خروجی:**
- `scores`: امتیازات مزاج‌ها
- `dominant_mizaj`: مزاج غالب
- `organ_indicators`: نشانگرهای اعضا

**نقاط تجزیه تحلیلی:**
- رنگ (قرمز = گرم، رنگ‌پریده = سرد)
- پوشش (زرد = گرم، سفید = سرد)
- رطوبت
- ترک‌ها و نوک‌ها

#### ترکیب نتایج
```python
diagnosis = AvicennaAnalysisEngine.synthesize_diagnosis(
    pulse_analysis,
    urine_analysis,
    tongue_analysis
)
```

**خروجی:**
- `primary_mizaj`: مزاج اولیه
- `secondary_mizaj`: مزاج ثانویه
- `overall_confidence`: درجه اطمینان کلی

### 2. ImageAnalysisService - تحلیل تصاویر

#### تحلیل تصویر زبان
```python
analysis = ImageAnalysisService.analyze_tongue_image(image_path)
```

**خروجی:**
```json
{
  "color": "pink",
  "coating": "none",
  "moisture": "normal",
  "texture": "smooth",
  "cracks_detected": false,
  "confidence_score": 0.85,
  "potential_conditions": [],
  "recommendation": "وضعیت طبیعی و سالم"
}
```

#### تحلیل تصویر چشم
```python
analysis = ImageAnalysisService.analyze_eye_image(image_path)
```

**خروجی:**
```json
{
  "redness_level": 2,
  "yellowness_detected": false,
  "pupil_size": "normal",
  "clarity": "clear",
  "confidence_score": 0.82,
  "potential_conditions": [],
  "recommendation": "وضعیت طبیعی و سالم"
}
```

#### شناسایی غیرعادی‌ها
```python
abnormalities = ImageAnalysisService.detect_tongue_abnormalities(analysis)
```

**مثال خروجی:**
```json
[
  {
    "type": "رنگ قرمز",
    "severity": "متوسط",
    "meaning": "نشانگر گرما"
  }
]
```

### 3. PersonalizedRecommendationService - توصیه‌های شخصی‌شده

#### تولید برنامه درمانی
```python
plan = PersonalizedRecommendationService.generate_personalized_plan(patient, db)
```

**خروجی:**
- **مرحله ۱: تطهیر (۱۰ روز)** - تطهیر بدن از اخلاط اضافی
- **مرحله ۲: تعادل (۲۰ روز)** - تعادل‌سازی مزاج
- **مرحله ۳: نگهداری (۳۰ روز)** - حفظ تعادل

#### برنامه هفتگی
```python
schedule = PersonalizedRecommendationService.generate_weekly_schedule(patient, db)
```

**شامل:**
- صبح: بیدار شدن، ورزش، شنا و دوش
- بعدازظهر: ناهار، استراحت، قدم‌زنی
- عصر: شام، چای، مدیتیشن
- شب: خواب منظم

#### برنامه غذایی ماهانه
```python
dietary_plan = PersonalizedRecommendationService.generate_monthly_dietary_plan(
    patient, mizaj, db
)
```

**شامل:**
- صبحانه
- ناهار
- شام
- میان‌وعده‌ها
- غذاهای ممنوع

#### راهنمای خود مراقبتی
```python
guide = PersonalizedRecommendationService.generate_self_monitoring_guide(patient, db)
```

**شامل:**
- بررسی‌های روزانه
- علائم هشداری
- زمان تماس با پزشک

## API Endpoints

### تحلیل جامع
```
POST /api/v1/analysis/comprehensive/{patient_id}
Content-Type: application/json

{
  "pulse_data": {
    "pulse_rate": 72,
    "primary_type": "motavasseta",
    "strength": "قوی",
    "rhythm": "منتظم",
    "temperature": 37.0
  },
  "urine_data": {
    "color": "zard",
    "density": "motavasseta",
    "clarity": "شفاف"
  },
  "tongue_data": {
    "body_color": "pink",
    "coating_color": "none",
    "moisture_level": "normal"
  }
}
```

### تحلیل تصویر زبان
```
POST /api/v1/analysis/analyze-tongue-image/{patient_id}
Content-Type: multipart/form-data

file: <تصویر زبان>
```

### تحلیل تصویر چشم
```
POST /api/v1/analysis/analyze-eye-image/{patient_id}
Content-Type: multipart/form-data

file: <تصویر چشم>
```

### برنامه درمانی شخصی‌شده
```
GET /api/v1/analysis/personalized-plan/{patient_id}
```

### برنامه هفتگی
```
GET /api/v1/analysis/weekly-schedule/{patient_id}
```

### برنامه غذایی
```
GET /api/v1/analysis/dietary-plan/{patient_id}?mizaj=garm
```

### راهنمای خود مراقبتی
```
GET /api/v1/analysis/self-monitoring-guide/{patient_id}
```

### توصیه‌های تصویری
```
POST /api/v1/analysis/image-recommendations/{patient_id}
Content-Type: multipart/form-data

tongue_file: <تصویر زبان> (اختیاری)
eye_file: <تصویر چشم> (اختیاری)
```

### گزارش جامع
```
GET /api/v1/analysis/full-report/{patient_id}
```

## مثال استفاده - Flutter

### بارگذاری تصاویر
```dart
Future<void> uploadImage() async {
  final picker = ImagePicker();
  final image = await picker.pickImage(source: ImageSource.camera);
  
  if (image != null) {
    final uri = Uri.parse(
      'http://your-server/api/v1/analysis/analyze-tongue-image/1'
    );
    
    final request = MultipartRequest('POST', uri);
    request.files.add(
      await MultipartFile.fromPath('file', image.path)
    );
    
    final response = await request.send();
    final result = await response.stream.bytesToString();
    
    final json = jsonDecode(result);
    print(json['analysis']);
  }
}
```

### دریافت برنامه درمانی
```dart
Future<void> getPersonalizedPlan() async {
  final response = await http.get(
    Uri.parse('http://your-server/api/v1/analysis/personalized-plan/1'),
  );
  
  if (response.statusCode == 200) {
    final plan = jsonDecode(response.body);
    setState(() {
      this.plan = plan;
    });
  }
}
```

## فایل‌های مرتبط

- `app/services/avicenna_analysis.py` - موتور تحلیل
- `app/services/image_analysis.py` - تحلیل تصاویر
- `app/services/personalized_recommendations.py` - توصیه‌های شخصی‌شده
- `app/routers/analysis_service.py` - API روتر
- `mobile/lib/screens/diagnostic_screen.dart` - صفحه تشخیصی
- `mobile/lib/screens/personalized_plan_screen.dart` - صفحه برنامه درمانی

## نکات مهم

1. **دقت**: تمام تحلیل‌ها براساس اصول سینا انجام می‌شود
2. **محرمانگی**: تمام داده‌های بیمار محفوظ است
3. **پیگیری**: بیماران می‌توانند پیشرفت خود را ردیابی کنند
4. **تخصیص**: هر برنامه براساس مزاج و شرایط خاص بیمار است
