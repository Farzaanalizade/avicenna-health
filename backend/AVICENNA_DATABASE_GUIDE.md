# Avicenna AI - پایگاه داده تشخیصی و درمانی بر اساس ابوعلی سینا

## مقدمه

این پایگاه داده بر اساس تعاليم و تجربیات طبابت ابوعلی سینا (ابن‌سینا) ساخته شده است. شامل اصول تشخیصی، بیماری‌ها، درمان‌های سنتی و مزاج‌شناسی می‌باشد.

## ساختار پایگاه داده

### 1. جداول تشخیصی (Diagnostic Tables)

#### PulseAnalysis - تحلیل نبض
تحلیل نبض بر اساس روش سینا:
- **نوع نبض**: kabir, saghir, tavil, qasir, sare_en, beth_in, montem_en, naamontem, qavi, zaeef, garm, sard
- **مشخصات**: قوت، ریتم، دما، عمق، عرض، محل
- **نشانگرهای سینایی**: نشان‌دهنده مزاج و وضعیت بدن

**فیلدهای اصلی:**
```
- pulse_rate: int (ضربات/دقیقه)
- primary_type: str (نوع اولیه)
- strength: str (قوت: ضعیف، متوسط، قوی)
- mizaj_indicator: str (نشان‌دهنده مزاج)
- condition_assessment: str (ارزیابی وضعیت)
```

#### UrineAnalysis - تحلیل ادرار
تحلیل ادرار بر اساس سنت سینا:
- **رنگ**: سفید، زرد، قرمز، قهوه‌ای، تیره
- **چگالی**: سبک، متوسط، سنگین
- **نشانگرهای سینایی**: نشان‌دهنده مزاج، گرما/سردی، رطوبت/خشکی

**فیلدهای اصلی:**
```
- color: enum (UrineColor)
- density: enum (UrineDensity)
- mizaj_indicator: str
- temperature_indication: str
- collection_time: str (صبح، بعد، شب)
```

#### TongueCoating - تحلیل زبان
تحلیل زبان و پوشش آن:
- **پوشش**: رنگ، ضخامت، پخش‌شدگی
- **بدن زبان**: رنگ، شکل، اندازه
- **نشانگرهای سینایی**: نشان‌دهنده مزاج و اعضای مختلف

**فیلدهای اصلی:**
```
- coating_color: str
- coating_thickness: str (نازک، متوسط، ضخیم)
- body_color: str
- moisture_level: str (خشک، طبیعی، مرطوب)
- mizaj_type: str
- organ_indicators: JSON
- disease_indicators: JSON
```

#### DiagnosticFinding - یافته‌های تشخیصی
خلاصه‌ی جمع‌بندی یافته‌های تشخیصی:
- **منابع**: ID‌های نبض، ادرار، زبان
- **نتیجه‌گیری**: مزاج اولیه و ثانویه، عدم‌تعادل‌ها
- **درمان**: توصیه‌های درمانی، غذایی، رفتاری

### 2. جداول بیماری و علائم

#### Disease - بیماری‌ها
بیماری‌های تصنیف‌شده:
- **دسته‌بندی**: عصبی، گوارشی، تنفسی، گردشی، تب، پوستی، مفصلی، روانی، متابولیکی
- **مزاج مرتبط**: لیستی از مزاج‌های مرتبط
- **اعضای تحت‌تأثیر**: عضو اول و ثانیه
- **علائم**: کلیدی و فرعی

**فیلدهای اصلی:**
```
- name_fa: str
- name_ar: str
- category: enum (DiseaseCategory)
- description: str
- avicenna_description: str (از متون سینا)
- key_symptoms: JSON
- related_mizaj: JSON
- primary_affected_organs: JSON
```

#### Symptom - علائم
علائم منفرد:
- **نوع**: سرگیجه، درد، تورم، الغری و...
- **شدت**: خفیف، متوسط، شدید
- **مزاج مرتبط**: مزاج‌های مرتبط
- **مناطق تحت‌تأثیر**

**فیلدهای اصلی:**
```
- name_fa: str
- symptom_type: str
- mizaj_related: JSON
- affected_areas: JSON
- when_observed: str (زمان مشاهده)
```

#### DiseaseSymptomRelation - رابطه بیماری-علامت
- **میزان ارتباط**: آیا علامت اولیه است
- **شیوع**: درصد شیوع
- **مرحله ظهور**: ابتدا، میانی، پایانی

### 3. جداول درمان

#### TraditionalRemedy - درمان‌های سنتی
درمان‌های سنتی بر اساس تعاليم سینا:
- **نوع درمان**: گیاهی، معدنی، غذایی، رفتاری، فیزیوتراپی، حجامت، ماساژ
- **اجزاء**: لیست اجزاء و مقادیر
- **موارد استفاده**: برای درمان کدام بیماری‌ها
- **خصوصیات سینایی**: ماهیت ترموتراپی و رطوبتی

**فیلدهای اصلی:**
```
- name_fa: str
- remedy_type: enum (TreatmentType)
- ingredients: JSON
- usage_method: str
- dosage: str
- temperature_nature: str (گرم/سرد)
- moisture_nature: str (تر/خشک)
- effect_on_mizaj: JSON
- safety_notes: str
- contraindications: JSON
```

#### DiseaseRemediRelation - رابطه بیماری-درمان
- **اثربخشی**: درصد اثربخشی
- **مرحله بیماری**: ابتدایی، متوسط، پیشرفته
- **درمان اولیه**: آیا این درمان اولیه است
- **اولویت**: ترتیب درمان

#### MizajBalanceTreatment - درمان برای تعادل مزاج
برنامه درمانی برای تعادل مزاج بیمار:
- **مزاج فعلی و هدف**
- **درمان‌های توصیه‌شده**
- **توصیه‌های غذایی و رفتاری**
- **برنامه درمانی تفصیلی**

**فیلدهای اصلی:**
```
- patient_id: int
- current_mizaj: str
- target_mizaj: str
- recommended_remedies: JSON
- dietary_recommendations: JSON
- lifestyle_changes: JSON
- expected_duration: str
- is_completed: bool
```

#### MedicalPlant - گیاهان دارویی
گیاهان دارویی بر اساس تعاليم سینا:
- **نام**: فارسی، عربی، لاتین
- **بخش استفاده‌شده**: ریشه، برگ، میوه، گل
- **ترکیبات فعال**
- **طبیعت سینایی**: ترموتراپی و رطوبتی
- **موارد استفاده و تعادل‌کنندگی مزاج**

## API Endpoints

### تشخیصی

#### نبض
```
POST   /api/v1/diagnosis/pulse              - ایجاد تحلیل نبض
GET    /api/v1/diagnosis/pulse/{pulse_id}  - دریافت تحلیل نبض
GET    /api/v1/diagnosis/pulse/patient/{patient_id}        - تمام نبض‌های بیمار
GET    /api/v1/diagnosis/pulse/patient/{patient_id}/latest - آخرین نبض
PUT    /api/v1/diagnosis/pulse/{pulse_id}  - به‌روزرسانی
DELETE /api/v1/diagnosis/pulse/{pulse_id}  - حذف
```

#### ادرار
```
POST   /api/v1/diagnosis/urine              - ایجاد تحلیل ادرار
GET    /api/v1/diagnosis/urine/{urine_id}  - دریافت
GET    /api/v1/diagnosis/urine/patient/{patient_id}        - تمام ادرار‌های بیمار
GET    /api/v1/diagnosis/urine/patient/{patient_id}/latest - آخرین ادرار
PUT    /api/v1/diagnosis/urine/{urine_id}  - به‌روزرسانی
```

#### زبان
```
POST   /api/v1/diagnosis/tongue               - ایجاد تحلیل زبان
GET    /api/v1/diagnosis/tongue/{tongue_id}  - دریافت
GET    /api/v1/diagnosis/tongue/patient/{patient_id}        - تمام زبان‌های بیمار
GET    /api/v1/diagnosis/tongue/patient/{patient_id}/latest - آخرین زبان
PUT    /api/v1/diagnosis/tongue/{tongue_id}  - به‌روزرسانی
```

#### یافته‌های تشخیصی
```
POST   /api/v1/diagnosis/findings                - ایجاد یافته
GET    /api/v1/diagnosis/findings/{finding_id}  - دریافت
GET    /api/v1/diagnosis/findings/patient/{patient_id}        - تمام یافته‌ها
GET    /api/v1/diagnosis/findings/patient/{patient_id}/latest - آخرین یافته
PUT    /api/v1/diagnosis/findings/{finding_id}  - به‌روزرسانی
GET    /api/v1/diagnosis/report/patient/{patient_id} - گزارش جامع
```

### بیماری‌ها و درمان

#### بیماری‌ها
```
POST   /api/v1/diseases                    - ایجاد بیماری
GET    /api/v1/diseases/{disease_id}      - دریافت
GET    /api/v1/diseases                   - لیست بیماری‌ها
GET    /api/v1/diseases/search/{name}     - جستجو
GET    /api/v1/diseases/category/{category} - بیماری‌های دسته
GET    /api/v1/diseases/mizaj/{mizaj}     - بیماری‌های مزاج
PUT    /api/v1/diseases/{disease_id}      - به‌روزرسانی
DELETE /api/v1/diseases/{disease_id}      - حذف
```

#### علائم
```
POST   /api/v1/symptoms                    - ایجاد علامت
GET    /api/v1/symptoms/{symptom_id}      - دریافت
GET    /api/v1/symptoms                   - لیست علائم
GET    /api/v1/symptoms/search/{name}     - جستجو
GET    /api/v1/symptoms/disease/{disease_id} - علائم بیماری
PUT    /api/v1/symptoms/{symptom_id}      - به‌روزرسانی
```

#### درمان‌های سنتی
```
POST   /api/v1/remedies                    - ایجاد درمان
GET    /api/v1/remedies/{remedy_id}       - دریافت
GET    /api/v1/remedies                   - لیست درمان‌ها
GET    /api/v1/remedies/search/{name}     - جستجو
GET    /api/v1/remedies/disease/{disease_id} - درمان‌های بیماری
GET    /api/v1/remedies/type/{remedy_type}   - درمان‌های نوع
GET    /api/v1/remedies/mizaj/{mizaj}     - درمان‌های مزاج
PUT    /api/v1/remedies/{remedy_id}       - به‌روزرسانی
```

#### درمان مزاج
```
POST   /api/v1/patients/{patient_id}/mizaj-treatments - ایجاد برنامه
GET    /api/v1/mizaj-treatments/{treatment_id}        - دریافت
GET    /api/v1/patients/{patient_id}/mizaj-treatments  - تمام برنامه‌ها
GET    /api/v1/patients/{patient_id}/mizaj-treatments/active - برنامه فعال
PUT    /api/v1/mizaj-treatments/{treatment_id}        - به‌روزرسانی
```

#### گیاهان دارویی
```
POST   /api/v1/medical-plants                  - ایجاد گیاه
GET    /api/v1/medical-plants/{plant_id}      - دریافت
GET    /api/v1/medical-plants                 - لیست گیاهان
GET    /api/v1/medical-plants/search/{name}   - جستجو
GET    /api/v1/medical-plants/disease/{disease_id} - گیاهان بیماری
GET    /api/v1/medical-plants/mizaj/{mizaj}   - گیاهان مزاج
PUT    /api/v1/medical-plants/{plant_id}      - به‌روزرسانی
```

## مثال‌های استفاده

### ایجاد تحلیل نبض
```json
POST /api/v1/diagnosis/pulse
{
  "patient_id": 1,
  "pulse_rate": 72,
  "primary_type": "motavasseta",
  "strength": "قوی",
  "rhythm": "منتظم",
  "temperature": 37.0,
  "mizaj_indicator": "motadel",
  "condition_assessment": "سلامت خوب"
}
```

### ایجاد تحلیل ادرار
```json
POST /api/v1/diagnosis/urine
{
  "patient_id": 1,
  "color": "zard",
  "density": "motavasseta",
  "clarity": "شفاف",
  "mizaj_indicator": "garm",
  "temperature_indication": "گرم",
  "collection_time": "صبح"
}
```

### دریافت درمان‌های بیماری
```
GET /api/v1/remedies/disease/1
```

### ایجاد برنامه درمانی برای تعادل مزاج
```json
POST /api/v1/patients/1/mizaj-treatments
{
  "current_mizaj": "garm_khoshk",
  "target_mizaj": "motadel",
  "recommended_remedies": [1, 2, 3],
  "dietary_recommendations": ["آب", "میوه‌های سرد"],
  "lifestyle_changes": ["کاهش فعالیت", "استراحت بیشتر"]
}
```

## نکات مهم

1. **مزاج‌ها**: تمام تحلیل‌ها بر اساس هشت مزاج سینایی (گرم، سرد، تر، خشک و ترکیب‌های آن‌ها) انجام می‌شود.

2. **اصول تشخیصی**: تحلیل‌های نبض، ادرار و زبان بر اساس متون سینا و روش‌های کلاسیکی طب ایرانی انجام می‌شود.

3. **درمان‌های سنتی**: تمام درمان‌ها طبق تعاليم ابوعلی سینا و کتب‌های قانون و دیگر آثار وی تصنیف شده‌اند.

4. **ترجمه و مراجع**: تمام متون فارسی شامل ترجمه‌های دقیق از متون عربی می‌باشند.

## فایل‌های مرتبط

- `app/models/avicenna_diagnosis.py` - مدل‌های تشخیصی
- `app/models/avicenna_diseases.py` - مدل‌های بیماری و درمان
- `app/schemas/avicenna_diagnosis.py` - Schema‌های تشخیصی
- `app/schemas/avicenna_diseases.py` - Schema‌های بیماری و درمان
- `app/crud/avicenna_diagnosis.py` - CRUD برای تشخیصی
- `app/crud/avicenna_diseases.py` - CRUD برای بیماری و درمان
- `app/routers/avicenna_diagnosis.py` - API روتر تشخیصی
- `app/routers/avicenna_diseases.py` - API روتر بیماری و درمان
- `seed_data.py` - داده‌های اولیه
