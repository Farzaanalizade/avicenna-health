"""
Ayurvedic Medicine Knowledge Models
طب سنتی هندی - آیورودا

Based on:
- Charaka Samhita (چاراک سنهیتا)
- Sushruta Samhita (سوشروت سنهیتا)
- Ashtanga Hridaya (اشتانگ هریدیا)
- Modern Ayurvedic protocols
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base


class DoshaType(str, Enum):
    """سه دوشا (سیال حاکم) در آیورودا"""
    VATA = "vata"                  # جو/هوا + فضا (Movement)
    PITTA = "pitta"                # آتش + آب (Transformation)
    KAPHA = "kapha"                # آب + زمین (Stability)


class DoshaCombination(str, Enum):
    """ترکیبات دوشا"""
    VATA_PITTA = "vata_pitta"
    VATA_KAPHA = "vata_kapha"
    PITTA_KAPHA = "pitta_kapha"
    TRIDOSHA = "tridosha"          # متعادل
    VATA_DOMINANT = "vata"
    PITTA_DOMINANT = "pitta"
    KAPHA_DOMINANT = "kapha"


class AyurvedicConstitution(Base):
    """ساختار تشکیل بدنی در آیورودا"""
    __tablename__ = "ayurveda_constitutions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت
    dosha_type = Column(String(50), nullable=False)  # DoshaType
    dosha_combination = Column(String(50), nullable=False)  # DoshaCombination
    
    # نام و شرح
    constitution_name = Column(String(255), nullable=False)
    constitution_description = Column(Text)
    
    # عناصر اساسی
    elements = Column(JSON)  # [{element: "space", percentage: 40}, {element: "air", percentage: 60}]
    
    # ویژگی‌های جسمانی
    physical_characteristics = Column(JSON)  # [{trait: "body_frame", value: "slender"}, ...]
    
    # ویژگی‌های روحی
    mental_characteristics = Column(JSON)  # [{trait: "temperament", value: "creative"}, ...]
    
    # ویژگی‌های هاضمی
    digestive_characteristics = Column(JSON)  # [{trait: "digestion_strength", value: "variable"}]
    
    # رنگ و بافت پوست
    skin_type = Column(String(100))
    skin_characteristics = Column(JSON)
    
    # نوع مو و ریش
    hair_type = Column(String(100))
    hair_characteristics = Column(JSON)
    
    # دمای بدن
    body_temperature_tendency = Column(String(100))
    
    # تحمل غذایی
    food_preferences = Column(JSON)
    food_tolerances = Column(JSON)
    
    # الگوی خواب
    sleep_pattern = Column(String(100))
    sleep_duration_preference = Column(String(100))
    
    # سطح انرژی
    energy_level = Column(String(100))
    energy_pattern = Column(String(255))
    
    # رفتار و اخلاق
    behavioral_traits = Column(JSON)  # [{trait: "emotional_stability", value: "moderate"}]
    
    # فصل‌های موثر
    seasons_aggravating = Column(JSON)  # فصل‌هایی که دوشا تشدید می‌شود
    
    # بیماری‌های احتمالی
    predisposition_to_diseases = Column(JSON)  # [{disease: "anxiety", likelihood: "high"}]
    
    # توصیه‌های زندگی
    lifestyle_recommendations = Column(JSON)  # [{recommendation: "daily_massage", frequency: "daily"}]
    
    # غذاهای مناسب
    recommended_foods = Column(JSON)  # [{food: "rice", reason: "pacifying", frequency: "regular"}]
    
    # غذاهای ممنوع
    foods_to_avoid = Column(JSON)  # [{food: "heavy_foods", reason: "aggravating"}]
    
    # رژیم زندگی
    daily_routine = Column(JSON)  # [{time: "06:00", activity: "oil_massage", duration: "15 min"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicDisease(Base):
    """بیماری‌های شناخت‌شده در آیورودا"""
    __tablename__ = "ayurveda_diseases"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت بیماری
    sanskrit_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    hindi_name = Column(String(255), nullable=True)
    modern_equivalent = Column(String(255), nullable=True)
    
    # طبقه‌بندی
    disease_category = Column(String(100), nullable=False)  # "infectious", "metabolic", "mental", "degenerative"
    
    # دوشا‌های درگیر
    involved_doshas = Column(JSON, nullable=False)  # [{dosha: "vata", role: "primary"}]
    
    # اغتشاشات بافت (Dhatu)
    affected_tissues = Column(JSON)  # [{tissue: "rasa_dhatu", role: "affected"}]
    
    # قنوات‌های متأثر (Srotas)
    affected_channels = Column(JSON)  # [{channel: "rasavaha_srotas", involvement: "significant"}]
    
    # تجمع سم (Ama)
    ama_involvement = Column(Boolean, default=False)
    ama_description = Column(Text)
    
    # علائم و نشانه‌ها
    main_symptoms = Column(JSON, nullable=False)
    secondary_symptoms = Column(JSON)
    
    # علائم دهان و زبان
    tongue_signs = Column(JSON)  # تغییرات روی زبان
    
    # علائم پالس و چشم
    pulse_characteristics = Column(JSON)
    eye_signs = Column(JSON)
    
    # دیگر علائم تشخیصی
    other_diagnostic_signs = Column(JSON)
    
    # علل ایجاد کننده
    causes = Column(JSON)  # [{cause: "improper_diet", type: "dietary", weight: 0.7}]
    
    # عوامل تشدید‌کننده
    aggravating_factors = Column(JSON)
    
    # مراحل بیماری
    disease_stages = Column(JSON)  # [{stage: "early", signs: "..."}, {stage: "chronic", signs: "..."}]
    
    # درمان‌های توصیه‌شده
    treatment_approaches = Column(JSON)  # [{"approach": "rasayana", "stage": "recovery"}]
    
    # تغذیه‌شناسی درمانی
    dietary_therapy = Column(JSON)  # [{food: "ghee", reason: "nourishing"}, ...]
    
    # درمان‌های گیاهی
    herbal_recommendations = Column(JSON)  # [{herb: "ashwagandha", form: "powder"}]
    
    # درمان‌های طب‌فیزیکی
    physical_therapies = Column(JSON)  # [{therapy: "abhyanga", frequency: "daily"}]
    
    # درمان‌های ذهنی و روحی
    mental_spiritual_therapies = Column(JSON)  # [{therapy: "meditation", frequency: "daily"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicPulseDiagnosis(Base):
    """تشخیص از روی نبض در آیورودا"""
    __tablename__ = "ayurveda_pulse_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # نوع حرکت نبض (Gati - Movement)
    pulse_movement = Column(String(50), nullable=False)  # "serpentine", "jumping", "wavelike"
    movement_description = Column(Text)
    
    # الگوی نبض برای هر دوشا
    vata_pattern = Column(String(255))  # "serpentine" - مثل مار
    pitta_pattern = Column(String(255))  # "jumping" - مثل قورباغه
    kapha_pattern = Column(String(255))  # "wavelike" - مثل اردک
    
    # موقعیت نبض
    pulse_position = Column(String(50))  # "superficial", "middle", "deep"
    position_meaning = Column(Text)
    
    # تغییرات دوره‌ای
    seasonal_variations = Column(JSON)  # [{season: "spring", pulse_change: "increased_pitta"}]
    
    # تغییرات زمانی
    time_of_day_variations = Column(JSON)  # [{time: "early_morning", pulse_change: "increased_vata"}]
    
    # نشانه‌های دوشا
    dosha_indicators = Column(JSON)  # [{dosha: "vata", rate: "70-100 bpm", quality: "serpentine"}]
    
    # نشانه‌های نابالانسی
    imbalance_signs = Column(JSON)  # [{imbalance: "excess_pitta", signs: "rapid_hot_pulse"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicTongueDiagnosis(Base):
    """تشخیص از روی زبان در آیورودا"""
    __tablename__ = "ayurveda_tongue_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # رنگ زبان
    tongue_color = Column(String(50), nullable=False)
    color_dosha_indication = Column(String(50))  # کدام دوشا را نشان می‌دهد
    color_meaning = Column(Text)
    
    # پوشش زبان
    coating_color = Column(String(50))
    coating_thickness = Column(String(50))
    coating_meaning = Column(Text)
    coating_ama_indication = Column(Boolean, default=False)  # نشانۀ سم (ama)
    
    # بافت و شکل
    texture = Column(String(50))
    shape = Column(String(50))
    
    # شکاف‌ها و خطوط
    cracks_present = Column(Boolean, default=False)
    cracks_pattern = Column(String(255))
    cracks_meaning = Column(Text)
    
    # حساسیت و حرارت
    sensitivity = Column(String(50))
    heat_cold_indication = Column(String(100))
    
    # نشانه‌های ویژه
    special_markings = Column(JSON)  # [{marking: "tooth_marks", dosha: "kapha"}]
    
    # دوشای غالب
    predominant_dosha = Column(String(50))
    
    # سطح Ama (سم)
    ama_level = Column(String(50))  # "none", "mild", "moderate", "severe"
    
    # نشانه‌های دیگر
    other_indicators = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicHerbDictionary(Base):
    """فرهنگ گیاهان دارویی در آیورودا"""
    __tablename__ = "ayurveda_herb_dictionary"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت گیاه
    sanskrit_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    hindi_name = Column(String(255), nullable=True)
    latin_botanical_name = Column(String(255), nullable=True)
    
    # طعم‌های آیورودایی (Rasa)
    tastes = Column(JSON, nullable=False)  # ["sweet", "bitter", "astringent"]
    
    # خصوصیات حرارتی (Virya)
    potency = Column(String(50), nullable=False)  # "heating", "cooling", "neutral"
    
    # اثر بعدی هاضمه (Vipaka)
    post_digestive_effect = Column(String(50))  # "sweet", "sour", "pungent"
    
    # تأثیرات دوشا
    dosha_effects = Column(JSON)  # [{dosha: "vata", effect: "balancing"}, ...]
    
    # انرژی و اثرات (Prabhava)
    special_potencies = Column(JSON)  # اثرات خاص فراتر از طعم و حرارت
    
    # بخش‌های دارویی
    parts_used = Column(JSON)  # ["root", "leaf", "seed", "bark", "fruit"]
    
    # عملکرد‌های اساسی
    primary_actions = Column(JSON)  # [{action: "anti_inflammatory", strength: "strong"}]
    
    # بیماری‌های درمان‌کننده
    treats_conditions = Column(JSON)  # [{condition: "digestive_issues", efficacy: 0.85}]
    
    # دوز معمول
    typical_dosage = Column(String(255))
    
    # اشکال توصیه‌شده
    recommended_forms = Column(JSON)  # ["powder", "decoction", "oil", "paste"]
    
    # موارد مخالفه
    contraindications = Column(JSON)  # [{condition: "pregnancy", reason: "..."}, ...]
    
    # تعاملات
    herb_interactions = Column(JSON)  # [{herb: "ginger", interaction: "complementary"}]
    
    # موارد احتیاطی
    precautions = Column(Text)
    
    # منابع
    classical_references = Column(JSON)  # ["Charaka Samhita", "Sushruta Samhita"]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicTherapy(Base):
    """درمان‌های سنتی آیورودایی"""
    __tablename__ = "ayurveda_therapies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت درمان
    sanskrit_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # نوع درمان
    therapy_type = Column(String(100), nullable=False)  # "massage", "oil_therapy", "heat", "cleansing"
    
    # زیرشاخه‌های درمان
    therapy_category = Column(String(100))  # برای massage مثلاً "abhyanga"
    
    # هدف درمانی
    therapeutic_goals = Column(JSON)  # [{goal: "remove_toxins", importance: "high"}]
    
    # دوشاهای متأثر
    dosha_effects = Column(JSON)  # [{dosha: "vata", effect: "pacifying"}]
    
    # مواد مورد استفاده
    materials_needed = Column(JSON)  # [{material: "sesame_oil", quantity: "250ml", role: "main"}]
    
    # مراحل انجام
    procedure_steps = Column(JSON)  # [{step: 1, description: "prepare_oil", duration: "5min"}]
    
    # مدت درمان
    session_duration = Column(String(100))  # مثلاً "60 minutes"
    frequency = Column(String(255))  # مثلاً "daily for 2 weeks"
    
    # بیماری‌هایی که درمان می‌کند
    treats_conditions = Column(JSON)  # [{condition: "arthritis", efficacy: 0.8}]
    
    # موارد مخالفه
    contraindications = Column(JSON)  # شرایطی که نباید انجام شود
    
    # نتایج مورد انتظار
    expected_outcomes = Column(JSON)  # [{outcome: "reduced_pain", timeline: "2-3 weeks"}]
    
    # احتیاطات
    precautions = Column(Text)
    
    # نوت‌های ویژه
    special_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicDietaryGuideline(Base):
    """دستورالعمل‌های تغذیه‌ای آیورودایی"""
    __tablename__ = "ayurveda_dietary_guidelines"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت
    guideline_name = Column(String(255), nullable=False)
    
    # دوشا مرتبط
    dosha_type = Column(String(50), nullable=False)
    
    # غذاهای مناسب
    beneficial_foods = Column(JSON)  # [{food: "rice", reason: "grounding", frequency: "daily"}]
    
    # غذاهای ممنوع
    foods_to_avoid = Column(JSON)  # [{food: "cold_drinks", reason: "aggravating"}]
    
    # روغن‌های توصیه‌شده
    recommended_oils = Column(JSON)  # [{oil: "sesame", use: "cooking", frequency: "daily"}]
    
    # ادویه‌ها و تصابیر
    recommended_spices = Column(JSON)  # [{spice: "ginger", benefit: "aids_digestion"}]
    
    # نمک
    salt_recommendation = Column(String(255))
    
    # شیر و محصولات لبنی
    dairy_products = Column(JSON)  # [{product: "ghee", benefit: "nourishing"}]
    
    # درنج‌های مناسب
    suitable_meals = Column(JSON)  # [{meal: "warm_breakfast", description: "..."}]
    
    # اوقات غذاخوری
    meal_timing = Column(JSON)  # [{time: "breakfast", hours: "07:00-08:00", note: "..."}]
    
    # سیال‌های مناسب
    beverages = Column(JSON)  # [{beverage: "warm_water", benefit: "aids_digestion"}]
    
    # روند هاضمه
    digestive_practices = Column(JSON)  # [{practice: "chew_well", duration: "30 times"}]
    
    # سایز پرتو (Agni - آتش هاضمه)
    digestive_fire_support = Column(JSON)
    
    # فصل‌های مختلف
    seasonal_adjustments = Column(JSON)  # [{season: "winter", adjustment: "eat_warming_foods"}]
    
    # سن‌های مختلف
    age_adjustments = Column(JSON)  # [{age: "elderly", adjustment: "lighter_meals"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicDhatu(Base):
    """بافت‌های بدن در آیورودا"""
    __tablename__ = "ayurveda_dhatus"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت بافت
    sanskrit_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # ترتیب
    order_number = Column(Integer)  # 1-7
    
    # توضیح
    description = Column(Text)
    
    # عملکرد
    functions = Column(JSON)
    
    # دوشای درگیر
    associated_doshas = Column(JSON)  # [{dosha: "vata", role: "primary"}]
    
    # نشانه‌های سلامت
    health_signs = Column(JSON)  # نشانه‌های تشکیل صحیح
    
    # نشانه‌های بیماری
    disease_signs = Column(JSON)  # نشانه‌های نابالانسی
    
    # غذاهای تغذیه‌کننده
    nourishing_foods = Column(JSON)  # [{food: "ghee", benefit: "strengthens"}]
    
    # درمان‌های توصیه‌شده
    recommended_treatments = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AyurvedicSrotas(Base):
    """قنوات بدن در آیورودا"""
    __tablename__ = "ayurveda_srotas"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت قناه
    sanskrit_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # توضیح
    description = Column(Text)
    
    # منبع
    origin = Column(String(255))
    
    # وجهت جریان
    direction = Column(String(255))
    
    # پایانه
    termination = Column(String(255))
    
    # وظیفه
    functions = Column(JSON)
    
    # دوشای درگیر
    associated_doshas = Column(JSON)
    
    # نشانه‌های سلامت
    health_signs = Column(JSON)
    
    # نشانه‌های انسداد یا اختلال
    disease_signs = Column(JSON)
    
    # درمان‌های توصیه‌شده
    recommended_treatments = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
