# 📚 Knowledge Base Expansion - Complete Documentation

**Date**: December 17, 2025  
**Phase**: 1C - Knowledge Base Implementation  
**Status**: ✅ COMPLETE

---

## 🎯 Overview

تکمیل پایگاه دانش جامع برای سه سنت پزشکی:
- **طب سینایی** (Avicenna/Ibn Sina) - Persian Islamic Medicine
- **طب سنتی چینی** (TCM) - Traditional Chinese Medicine  
- **طب سنتی هندی** (Ayurveda) - Traditional Indian Medicine

---

## 📊 Models Created

### **1. Avicenna Knowledge Base** (7 Models)

#### AvicennaDisease
```
جدول: avicenna_diseases
- شناخت بیماری (persian_name, arabic_name, modern_equivalent)
- تصنیف (category, severity)
- مزاج و خلط‌ها (related_mizaj, involved_humors)
- علائم و نشانه‌ها (symptoms, tongue_signs, pulse_signs)
- درمان‌ها (treatments, dietary_recommendations, lifestyle_recommendations)
- منابع (source_books, reference_text)
```

**مثال**:
```
تب (Fever)
- مزاج: گرم و تر (garm_tar)
- خلط: خون (khoon)
- علائم: حرارت، خشکی دهان
- درمان: کاشنی، رژیم غذایی سرد
```

---

#### AvicennaTongueDiagnosis
```
جدول: avicenna_tongue_diagnosis
- رنگ زبان (color_category, color_mizaj)
- پوشش (coating_type, coating_color)
- بافت و شکل (texture, moisture, thickness)
- شکاف‌ها (cracks_present, cracks_pattern)
- معنی تشخیصی (related_mizaj, confidence)
```

**معیارهای تشخیصی**:
| رنگ زبان | معنی | مزاج |
|---------|------|------|
| Pale | ضعف و نقص | سرد و تر |
| Red | گرمی | گرم و تر |
| Crimson | گرمی شدید | گرم و خشک |
| Dark | سودای سیاه | سرد و خشک |

---

#### AvicennaPulseDiagnosis
```
جدول: avicenna_pulse_diagnosis
- ضربان (pulse_rate_range, pulse_rate_min/max)
- نوع نبض (pulse_rhythm, pulse_strength, pulse_depth)
- نرمی و سختی (pulse_texture)
- معنی تشخیصی (related_mizaj, confidence)
```

**انواع نبض**:
- Thready (نازک) - ضعف
- Bounding (قوی ضربانی) - گرمی
- Wiry (سیم‌مانند) - سردی
- Slippery (لغزشی) - رطوبت

---

#### AvicennaEyeDiagnosis
```
جدول: avicenna_eye_diagnosis
- رنگ چشم (eye_color_indicator, color_mizaj)
- سفیدی چشم (sclera_color)
- حدقه (pupil_size, pupil_meaning)
- چمک و تاب (brightness)
```

---

#### AvicennaTreatment
```
جدول: avicenna_treatments
- نوع درمان (treatment_type: herbal, dietary, lifestyle, bloodletting)
- درمان گیاهی (herbal_name, herbal_preparation, dosage)
- خواص (potency, moisture)
- درمان‌های غذایی (recommended_foods, forbidden_foods)
- سبک زندگی (lifestyle_advice)
```

---

#### AvicennaHerbalRemedyDictionary
```
جدول: avicenna_herbal_remedies
- شناخت گیاه (persian_name, english_name, latin_botanical_name)
- خواص دارویی (potency, moisture_property)
- تأثیرات (effects, treats_diseases)
- دوز (recommended_dosage, dosage_frequency)
- موارد مخالفه (contraindications, side_effects)
- منابع (avicenna_reference)
```

**مثال**: کاشنی (Chicory)
```
نام: Cichorium intybus
خاصیت: سرد و مرطوب
تأثیر: خنک‌کننده، ملین
درمان: تب، التهاب، مشکلات کبدی
دوز: 6-10 گرم
```

---

#### AvicennaMizajBalanceGuide
```
جدول: avicenna_mizaj_balance_guide
- مزاج (mizaj: garm_tar, garm_khoshk, sard_tar, sard_khoshk)
- خلط غالب (dominant_humor)
- غذاهای مناسب (recommended_foods)
- فصل‌های مناسب (favorable_seasons)
- فعالیت‌های توصیه‌شده (recommended_activities)
- بیماری‌های احتمالی (potential_diseases)
```

---

### **2. TCM Knowledge Base** (7 Models)

#### TCMPatternDisharmony
```
جدول: tcm_pattern_disharmonies
- نام الگو (chinese_name, pinyin_name, english_name)
- عناصر اساسی (involved_organs, involved_meridians)
- نوع نقص (pathology_type: deficiency, excess, stagnation)
- علائم و نشانه‌ها (main_symptoms, secondary_symptoms)
- تشخیص (tongue_findings, pulse_findings, other_signs)
- علل (etiological_factors)
- درمان (treatment_principles)
```

**مثال**: Wind-Heat Common Cold (風熱感冒)
```
عضو: Lung (ریه)
مسیر: Lung Meridian
علائم: سردرد، سوز گلو، تب
زبان: قرمز با پوشش زرد نازک
نبض: سطحی و تند
درمان: Release exterior, Clear heat
```

---

#### TCMMeridian
```
جدول: tcm_meridians
- شناخت (chinese_name, pinyin_name, english_name)
- نوع (meridian_type: primary, connecting, divergent)
- عضو (associated_organ, zang_fu_level)
- جریان انرژی (qi_flow_direction)
- نقاط آکوپنکچر (acupuncture_points)
- ساعت دوری (organ_clock_time, circadian_rhythm)
```

**مثال**: Liver Meridian (肝經)
```
نام: Gan Jing (Liver Channel)
عضو: Liver
ساعت اوج: 01:00-03:00
شروع: لبۀ پنجۀ بزرگ (lateral corner of big toenail)
پایان: زیر قفسۀ سینه راست
```

---

#### TCMAcupuncturePoint
```
جدول: tcm_acupuncture_points
- کد نقطه (point_code: "LV3", "HT7")
- موقعیت (location, location_detail)
- عملکرد (functions)
- نشانه‌های استفاده (indications)
- روش بازمان (moxibustion_suitable)
- عمق نیش (needle_depth, needle_sensation)
- دستکاری (manipulations)
```

**مثال**: Taichong (太衝) - LV3
```
مکان: بین متاتارسال 1 و 2 پای، در رتا
عملکرد: Coursing liver qi, Subduing liver yang
نشانه: سردرد، درد چشم، خشونت طبع، بی‌خوابی
```

---

#### TCMHerbalFormula
```
جدول: tcm_herbal_formulas
- نام (chinese_name, pinyin_name, english_name)
- نوع (formula_category: decoction, pill, powder)
- منبع (classical_reference, formulation_era)
- اصول (treatment_principles)
- گیاهان (herbs with role: chief, deputy, assistant)
- نشانه‌ها (indications)
- دوز (dosage, course_duration)
```

**مثال**: Yin Qiao San (銀翹散 - Honeysuckle and Forsythia Powder)
```
اصول: Release exterior, Clear heat
گیاهان:
  - Honeysuckle flower (chief): 9g
  - Forsythia fruit (chief): 9g
  - Reed rhizome (deputy): 6g
نشانه: سرما و آنفولانزا (مرحلۀ اولیه)
روش: پودر، حل در آب گرم
```

---

#### TCMHerbDictionary
```
جدول: tcm_herb_dictionary
- شناخت (chinese_name, english_name, latin_botanical_name)
- خاصیت (temperature_nature: cold/cool/warm/hot)
- طعم (flavor: bitter, sweet, salty, sour, acrid)
- ورود مسیرها (meridian_entries)
- عملکرد (primary_functions, treats_conditions)
- دوز (typical_dosage, dosage_range)
```

**مثال**: Ginseng (人蔘 - Ren Shen)
```
طبیعت: Warm
طعم: Sweet, slightly bitter
مسیرها: Spleen, Lung, Heart
عملکرد: Tonify qi, Supplement the spleen
دوز: 3-10 گرم
```

---

#### TCMTongueDiagnosis
```
جدول: tcm_tongue_diagnosis
- رنگ (tongue_color, color_meaning)
- پوشش (coating_color, coating_thickness, coating_distribution)
- رطوبت (moisture_level)
- شکاف‌ها (cracks, cracks_description)
- شکل (shape, special_signs)
- نمط‌های مربوطه (related_patterns, confidence_level)
```

**فرمول خوندن زبان**:
| رنگ | معنی | پوشش | معنی |
|-----|------|--------|--------|
| Pale | Qi/Blood deficiency | None | Normal |
| Red | Heat | Thin white | Normal/early cold |
| Crimson | Heat (excess) | Thick yellow | Heat excess |
| Purple | Blood stasis | Greasy | Damp-heat |
| Dark | Cold/Stagnation | Black | Severe heat/cold |

---

#### TCMPulseDiagnosis
```
جدول: tcm_pulse_diagnosis
- موقعیت (pulse_position: superficial, moderate, deep)
- سرعت (pulse_speed: slow, moderate, rapid)
- قوت (pulse_strength: weak, moderate, strong, surging)
- نوع (pulse_rhythm: regular, irregular, intermittent)
- کیفیت (pulse_quality: slippery, wiry, thready, choppy)
- نمط‌های مربوطه (related_patterns, confidence_level)
```

**28 نوع نبض سنتی**:
```
Floating (سطحی) + Tight (سفت) = Wind-Cold (سرما)
Deep (عمیق) + Slow (کند) = Cold deficiency (نقص سردی)
Rapid (تند) + Thin (نازک) = Yin deficiency (نقص یین)
Wiry (سیم‌مانند) + Tight = Stagnation/pain (ایستایش)
```

---

### **3. Ayurveda Knowledge Base** (9 Models)

#### AyurvedicConstitution
```
جدول: ayurveda_constitutions
- نوع دوشا (dosha_type: vata, pitta, kapha)
- ترکیب (dosha_combination)
- عناصر (elements: space, air, fire, water, earth)
- ویژگی‌های جسمانی (physical_characteristics)
- ویژگی‌های روحی (mental_characteristics)
- ویژگی‌های هاضمی (digestive_characteristics)
- پوست و مو (skin_type, hair_type)
- دما (body_temperature_tendency)
- سبک زندگی (sleep_pattern, energy_level)
```

**سه دوشا**:

1. **Vata** (جو/هوا + فضا)
   - ویژگی: سریع، تغییر‌پذیر، خلاق
   - جسم: باریک، سبک
   - شخصیت: نگران‌کن، فعال
   - هاضمه: نامنظم
   - فصل: پاییز، اوایل زمستان

2. **Pitta** (آتش + آب)
   - ویژگی: درخشان، حادکننده، فعال
   - جسم: متوسط، ورزشکار
   - شخصیت: هدفمند، قاطع
   - هاضمه: قوی
   - فصل: تابستان

3. **Kapha** (آب + زمین)
   - ویژگی: آرام، پایدار، مهربان
   - جسم: بزرگ، منسجم
   - شخصیت: صبور، وفادار
   - هاضمه: آهسته
   - فصل: بهار، اوایل گرما

---

#### AyurvedicDisease
```
جدول: ayurveda_diseases
- شناخت (sanskrit_name, english_name, modern_equivalent)
- طبقه‌بندی (disease_category)
- دوشاهای درگیر (involved_doshas)
- بافت‌های متأثر (affected_tissues)
- قنوات متأثر (affected_channels)
- سم (ama_involvement, ama_description)
- علائم (main_symptoms, secondary_symptoms)
- علل (causes, aggravating_factors)
- درمان (treatment_approaches, herbal_recommendations)
```

**مثال**: Jvara (تب)
```
عامل: Pitta + Vata
بافت: Rasa Dhatu (پلاسما)
سم: High ama involvement
علائم: تب، عرق، تنبلی
درمان:
  - Cooling herbs: Guduchi, Neem
  - Light diet
  - Rest and silence
```

---

#### AyurvedicPulseDiagnosis
```
جدول: ayurveda_pulse_diagnosis
- حرکت نبض (pulse_movement: serpentine, jumping, wavelike)
- موقعیت (pulse_position: superficial, middle, deep)
- الگوهای دوشا (vata_pattern, pitta_pattern, kapha_pattern)
- تغییرات فصلی (seasonal_variations)
- نشانه‌های دوشا (dosha_indicators)
- نشانه‌های نابالانسی (imbalance_signs)
```

**الگوهای نبض**:
```
Vata:   Serpentine (مثل مار) - متحرک، نامنظم
Pitta:  Jumping (مثل قورباغه) - قوی، تند
Kapha:  Wavelike (مثل اردک) - آرام، منتظم
```

---

#### AyurvedicTongueDiagnosis
```
جدول: ayurveda_tongue_diagnosis
- رنگ (tongue_color, color_dosha_indication)
- پوشش (coating_color, coating_thickness, ama_indication)
- بافت (texture, shape, cracks_present)
- حساسیت (sensitivity, heat_cold_indication)
- نشانه‌های ویژه (special_markings)
- سطح سم (ama_level: none, mild, moderate, severe)
```

---

#### AyurvedicHerbDictionary
```
جدول: ayurveda_herb_dictionary
- شناخت (sanskrit_name, english_name, latin_botanical_name)
- طعم‌های آیورودایی (tastes: sweet, sour, salty, etc.)
- خاصیت حرارتی (potency: heating, cooling, neutral)
- اثر بعدی (post_digestive_effect)
- تأثیرات دوشا (dosha_effects)
- عملکرد (primary_actions, treats_conditions)
- دوز (typical_dosage, recommended_forms)
```

**مثال**: Ashwagandha (اشواگندا)
```
طعم: Bitter, astringent
طبیعت: Warm
اثر بعدی: Sweet
دوشا: Balances Vata, reduces Kapha
عملکرد: Adaptogen, immune support
دوز: 1-6 گرم روزانه
```

---

#### AyurvedicTherapy
```
جدول: ayurveda_therapies
- شناخت (sanskrit_name, english_name)
- نوع (therapy_type: massage, oil, heat, cleansing)
- اهداف (therapeutic_goals)
- تأثیرات دوشا (dosha_effects)
- مواد مورد استفاده (materials_needed)
- مراحل (procedure_steps)
- مدت و تکرار (session_duration, frequency)
```

**مثال**: Abhyanga (روغن‌کاری)
```
مدت: 45-60 دقیقه
روغن: Sesame oil
مزایا:
  - تغذیۀ بافت‌ها
  - جریان خون
  - لطافت پوست
  - آرام‌سازی Vata
```

---

#### AyurvedicDietaryGuideline
```
جدول: ayurveda_dietary_guidelines
- نام (guideline_name)
- دوشای مرتبط (dosha_type)
- غذاهای مناسب (beneficial_foods)
- غذاهای ممنوع (foods_to_avoid)
- روغن‌های توصیه‌شده (recommended_oils)
- ادویه‌ها (recommended_spices)
- اوقات غذاخوری (meal_timing)
- سیال‌های مناسب (beverages)
```

---

#### AyurvedicDhatu
```
جدول: ayurveda_dhatus (7 بافت)
- شناخت (sanskrit_name, english_name)
- ترتیب (order_number: 1-7)
- عملکرد (functions)
- دوشای درگیر (associated_doshas)
- نشانه‌های سلامت (health_signs)
- نشانه‌های بیماری (disease_signs)
- غذاهای تغذیه‌کننده (nourishing_foods)
```

**7 بافت اساسی**:
```
1. Rasa (پلاسما) - تغذیۀ همۀ بافت‌ها
2. Rakta (خون) - حمل اکسیژن
3. Mamsa (ماهیچه) - قدرت و حرکت
4. Meda (چربی) - انرژی و حرارت
5. Asthi (استخوان) - ساختار
6. Majja (مغز) - شعور
7. Shukra (تخمدان/منی) - تولید مثل
```

---

#### AyurvedicSrotas
```
جدول: ayurveda_srotas (قنوات)
- شناخت (sanskrit_name, english_name)
- منبع (origin)
- جهت جریان (direction)
- پایانه (termination)
- وظیفه (functions)
- نشانه‌های سلامت (health_signs)
- نشانه‌های انسداد (disease_signs)
```

**13 قنۀ اساسی**:
```
1. Rasavaha - جریان پلاسما
2. Raktavaha - جریان خون
3. Masvaha - جریان ماهیچه
4. Medavaha - جریان چربی
5. Asthivaha - جریان استخوان
...و غیره
```

---

## 🔗 API Endpoints

### Knowledge Base Search

#### Avicenna
```
GET  /api/v1/knowledge/avicenna/diseases
     Query: query, mizaj, category, limit
GET  /api/v1/knowledge/avicenna/diseases/{id}
GET  /api/v1/knowledge/avicenna/tongue-diagnosis
GET  /api/v1/knowledge/avicenna/pulse-diagnosis
GET  /api/v1/knowledge/avicenna/herbal-remedies
GET  /api/v1/knowledge/avicenna/mizaj-balance/{mizaj}
```

#### TCM
```
GET  /api/v1/knowledge/tcm/patterns
GET  /api/v1/knowledge/tcm/patterns/{id}
GET  /api/v1/knowledge/tcm/meridians
GET  /api/v1/knowledge/tcm/meridians/{id}
GET  /api/v1/knowledge/tcm/acupuncture-points
GET  /api/v1/knowledge/tcm/formulas
GET  /api/v1/knowledge/tcm/herbs
```

#### Ayurveda
```
GET  /api/v1/knowledge/ayurveda/constitutions
GET  /api/v1/knowledge/ayurveda/constitutions/{id}
GET  /api/v1/knowledge/ayurveda/diseases
GET  /api/v1/knowledge/ayurveda/diseases/{id}
GET  /api/v1/knowledge/ayurveda/herbs
GET  /api/v1/knowledge/ayurveda/therapies
GET  /api/v1/knowledge/ayurveda/dietary-guidelines
GET  /api/v1/knowledge/ayurveda/dhatus
GET  /api/v1/knowledge/ayurveda/srotas
```

#### Comparative
```
GET  /api/v1/knowledge/compare/disease?disease_name=fever
GET  /api/v1/knowledge/statistics/knowledge-base
```

---

## 📁 Files Created

### Models
```
✅ backend/app/models/avicenna_knowledge_base.py     (7 models)
✅ backend/app/models/tcm_knowledge_base.py          (7 models)
✅ backend/app/models/ayurveda_knowledge_base.py     (9 models)
```

### Schemas
```
✅ backend/app/schemas/knowledge_base_schemas.py     (21 schemas)
```

### Routes
```
✅ backend/app/routers/knowledge_base.py             (25+ endpoints)
```

### Seed Data
```
✅ backend/seed_knowledge_base.py                    (Complete)
```

---

## 🚀 Next Steps

### Phase 2: Mobile Integration
```
1. ✅ Database complete
2. ✅ API endpoints ready
3. ⏳ Mobile app integration
4. ⏳ Real-time consultation
5. ⏳ Offline knowledge base on device
```

### Phase 3: AI Enhancement
```
1. ⏳ Multi-language support
2. ⏳ Advanced symptom matching
3. ⏳ Confidence scoring
4. ⏳ Treatment recommendations
5. ⏳ Drug interaction checking
```

---

## 📈 Statistics

**Total Models**: 23 (7 + 7 + 9)  
**Total API Endpoints**: 25+  
**Pydantic Schemas**: 21  
**Knowledge Base Tables**: 23  
**Lines of Code**: ~2,500

---

## ✅ Checklist

Database:
- [x] All 23 models created
- [x] Relationships defined
- [x] Cascade deletes configured
- [x] Indexes planned

API:
- [x] All GET endpoints
- [x] Search functionality
- [x] Comparative analysis
- [x] Statistics endpoints
- [x] Error handling

Data:
- [x] Seed script created
- [x] Sample data prepared
- [x] Data validation

---

**Status**: ✅ KNOWLEDGE BASE EXPANSION COMPLETE  
**Ready for**: Phase 2 Mobile Integration + Phase 3 AI Training
