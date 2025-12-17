"""
Traditional Chinese Medicine (TCM) Knowledge Models
طب سنتی چینی

Based on:
- 黄帝内经 (Yellow Emperor's Inner Classic)
- 伤寒论 (Treatise on Cold Damage)
- 金匮要略 (Essential Prescriptions of the Golden Cabinet)
- Modern TCM documentation
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base


class TCMConstitution(str, Enum):
    """انواع تشکیل‌کننده در طب چینی"""
    PING_HE = "ping_he"              # Balanced/Harmonious
    QI_XU = "qi_xu"                  # Qi Deficiency
    YANG_XU = "yang_xu"              # Yang Deficiency
    YIN_XU = "yin_xu"                # Yin Deficiency
    TANG_XU = "tang_xu"              # Phlegm-Dampness
    WET_RE = "wet_re"                # Damp-Heat
    XUEYU = "xueyu"                  # Blood Stasis
    QI_ZHI = "qi_zhi"                # Qi Stagnation
    SPECIAL = "special"              # Special Diathesis


class TCMPatternDisharmony(Base):
    """نمط بی‌هماهنگی در طب چینی"""
    __tablename__ = "tcm_pattern_disharmonies"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # نام الگو
    chinese_name = Column(String(255), nullable=False)
    pinyin_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # تصنیف الگو
    pattern_category = Column(String(100), nullable=False)  # "interior_exterior", "cold_heat", "xu_shi"
    
    # عناصر اساسی
    involved_organs = Column(JSON, nullable=False)  # [{organ: "liver", role: "primary"}]
    involved_meridians = Column(JSON)  # [{meridian: "liver meridian", role: "affected"}]
    
    # نوع نقص یا مشکل
    pathology_type = Column(String(100))  # "deficiency", "excess", "stagnation", "collapse"
    
    # علائم و نشانه‌ها
    main_symptoms = Column(JSON, nullable=False)  # [{symptom: "headache", frequency: "constant"}]
    secondary_symptoms = Column(JSON)
    
    # تشخیص زبان
    tongue_findings = Column(JSON)  # [{finding: "color", value: "pale", significance: "high"}]
    
    # تشخیص نبض
    pulse_findings = Column(JSON)  # [{finding: "type", value: "thready", significance: "high"}]
    
    # دیگر علائم تشخیصی
    other_signs = Column(JSON)  # [{sign: "facial_color", value: "pale"}]
    
    # علل ایجاد کننده
    etiological_factors = Column(JSON)  # [{factor: "emotional_stress", weight: 0.7}]
    
    # درمان‌های توصیه‌شده
    treatment_principles = Column(JSON)  # [{"principle": "nourish_yin", "importance": "high"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    formulas = relationship("TCMHerbalFormula", back_populates="pattern")
    acupuncture_points = relationship("TCMAcupuncturePoint", back_populates="pattern")


class TCMTongueDiagnosis(Base):
    """تشخیص از روی زبان در طب چینی"""
    __tablename__ = "tcm_tongue_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # رنگ زبان
    tongue_color = Column(String(50), nullable=False)  # "pale", "normal", "red", "crimson", "purple"
    color_meaning = Column(Text)
    
    # آثار چین‌های اصلی
    main_qi_pulse_marks = Column(String(50))  # "presence", "absence", "prominent"
    
    # پوشش زبان (Coating)
    coating_color = Column(String(50))  # "white", "yellow", "gray", "black"
    coating_thickness = Column(String(50))  # "thin", "thick", "greasy"
    coating_distribution = Column(String(100))  # "uniform", "root_only", "thick_root_thin_tip"
    
    # رطوبت
    moisture_level = Column(String(50))  # "dry", "normal", "wet", "very_wet"
    
    # شکاف‌ها
    cracks = Column(Boolean, default=False)
    cracks_description = Column(String(255))  # "central", "scattered", "geographic"
    
    # شکل زبان
    shape = Column(String(100))  # "swollen", "slim", "indented", "enlarged"
    
    # نشانه‌های ویژه
    special_signs = Column(JSON)  # [{sign: "papillae_enlarged", meaning: "heat_sign"}]
    
    # نمط مربوطه
    related_patterns = Column(JSON)  # [{pattern: "spleen_qi_deficiency", confidence: 0.8}]
    
    # سطح قطعیت
    confidence_level = Column(Float, default=0.75)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TCMPulseDiagnosis(Base):
    """تشخیص از روی نبض در طب چینی"""
    __tablename__ = "tcm_pulse_diagnosis"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # ویژگی‌های اساسی نبض
    pulse_position = Column(String(50), nullable=False)  # "superficial", "moderate", "deep"
    pulse_speed = Column(String(50), nullable=False)  # "slow", "moderate", "rapid", "very_rapid"
    pulse_strength = Column(String(50), nullable=False)  # "weak", "moderate", "strong", "surging"
    pulse_rhythm = Column(String(50), nullable=False)  # "regular", "irregular", "intermittent"
    
    # ویژگی‌های کیفی
    pulse_quality = Column(String(100))  # "slippery", "wiry", "thready", "choppy", "tight"
    
    # نمط‌های ترکیبی
    composite_patterns = Column(JSON)  # [{pattern: "floating_rapid", meaning: "wind_heat"}]
    
    # نمط مربوطه
    related_patterns = Column(JSON)  # [{pattern: "lung_qi_deficiency", confidence: 0.7}]
    
    # معنی تشخیصی
    diagnostic_significance = Column(Text)
    
    # سطح قطعیت
    confidence_level = Column(Float, default=0.70)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TCMMeridian(Base):
    """مسیرهای انرژی (Meridians/Jing Luo)"""
    __tablename__ = "tcm_meridians"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت مسیر
    chinese_name = Column(String(255), nullable=False)
    pinyin_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # نوع مسیر
    meridian_type = Column(String(50), nullable=False)  # "primary", "connecting", "divergent", "eight_extraordinary"
    
    # عضو مرتبط
    associated_organ = Column(String(100), nullable=False)  # "liver", "heart", "lungs", "spleen", "kidney", "pericardium"
    zang_fu_level = Column(String(50))  # "yin_organ", "yang_organ"
    
    # جریان انرژی
    qi_flow_direction = Column(String(255))  # توصیف جریان
    
    # نقاط آکوپنکچر
    acupuncture_points = relationship("TCMAcupuncturePoint", back_populates="meridian")
    
    # نقاط ویژه
    special_points = Column(JSON)  # [{point_number: "3", point_name: "Taichong", function: "..."}]
    
    # شروع و پایان
    starting_location = Column(String(255))
    ending_location = Column(String(255))
    
    # مدت چرخه
    organ_clock_time = Column(String(50))  # ساعتی که انرژی در اوج است
    
    # سطح انرژی در ساعات مختلف
    circadian_rhythm = Column(JSON)  # [{hour: "01:00-03:00", energy_level: "peak"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TCMAcupuncturePoint(Base):
    """نقاط آکوپنکچر"""
    __tablename__ = "tcm_acupuncture_points"
    
    id = Column(Integer, primary_key=True, index=True)
    meridian_id = Column(Integer, ForeignKey("tcm_meridians.id"), nullable=False)
    pattern_id = Column(Integer, ForeignKey("tcm_pattern_disharmonies.id"), nullable=True)
    
    # شناخت نقطه
    point_code = Column(String(50), nullable=False, unique=True)  # "LV3", "HT7"
    chinese_name = Column(String(255), nullable=False)
    pinyin_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # موقعیت
    location = Column(Text, nullable=False)  # توصیف مکانی
    location_detail = Column(JSON)  # [{measurement: "3_cun_below_knee", direction: "lateral"}]
    
    # ترجیح
    point_preference = Column(String(50))  # "distal", "local", "empirical"
    
    # عملکرد‌های اساسی
    functions = Column(JSON, nullable=False)  # [{function: "regulate_liver_qi", importance: "high"}]
    
    # نشانه‌های استفاده
    indications = Column(JSON)  # [{indication: "headache", category: "local_effect"}]
    
    # اثر نبض
    pulse_effect = Column(String(255))
    
    # روش بازمان (Moxa/Moxibustion)
    moxibustion_suitable = Column(Boolean, default=False)
    
    # عمق نیش
    needle_depth = Column(String(100))
    needle_sensation = Column(String(255))  # احساس در نقطه
    
    # تعدادی که باید فعال شود
    manipulations = Column(JSON)  # [{technique: "tonifying", method: "reinforcing"}]
    
    # نکات احتیاطی
    precautions = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    meridian = relationship("TCMMeridian", back_populates="acupuncture_points")
    pattern = relationship("TCMPatternDisharmony", back_populates="acupuncture_points")


class TCMHerbalFormula(Base):
    """فرمول‌های داروی گیاهی تقلیدی چینی"""
    __tablename__ = "tcm_herbal_formulas"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey("tcm_pattern_disharmonies.id"), nullable=False)
    
    # شناخت فرمول
    chinese_name = Column(String(255), nullable=False)
    pinyin_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    
    # نوع فرمول
    formula_category = Column(String(100), nullable=False)  # "decoction", "pill", "powder", "patent_medicine"
    
    # منبع و منابع
    classical_reference = Column(String(255))  # "Shang Han Lun", "Jin Gui Yao Lue"
    formulation_era = Column(String(100))
    
    # اصول درمانی
    treatment_principles = Column(JSON, nullable=False)  # [{principle: "tonify_spleen", importance: "primary"}]
    
    # گیاهان تشکیل‌دهنده
    herbs = Column(JSON, nullable=False)  # [{herb: "ginseng", role: "chief", dosage: "9g"}]
    
    # تعادل فرمول
    formula_balance = Column(JSON)  # [{balance_type: "chief_deputy_assistant", description: "..."}]
    
    # نشانه‌های استفاده
    indications = Column(JSON, nullable=False)  # [{indication: "fatigue", stage: "chronic"}]
    
    # موارد مخالفه
    contraindications = Column(JSON)  # [{condition: "pregnancy", reason: "..."}]
    
    # اثرات جانبی
    side_effects = Column(JSON)  # [{effect: "digestive_upset", frequency: "rare"}]
    
    # روش تهیه
    preparation_method = Column(Text)
    decoction_time = Column(String(100))
    
    # دوز توصیه‌شده
    dosage = Column(String(255))
    dosage_frequency = Column(String(255))
    course_duration = Column(String(255))
    
    # تعاملات
    interactions = Column(JSON)  # [{interaction_with: "western_medicine", type: "caution"}]
    
    # تغییرات
    modifications = Column(JSON)  # [{modification: "add_extra_herb", condition: "if_constipation"}]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    pattern = relationship("TCMPatternDisharmony", back_populates="formulas")


class TCMHerbDictionary(Base):
    """فرهنگ گیاهان دارویی در طب چینی"""
    __tablename__ = "tcm_herb_dictionary"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # شناخت گیاه
    chinese_name = Column(String(255), nullable=False)
    pinyin_name = Column(String(255), nullable=False)
    english_name = Column(String(255), nullable=False)
    latin_botanical_name = Column(String(255), nullable=True)
    
    # خصوصیات طبیعت
    temperature_nature = Column(String(50), nullable=False)  # "cold", "cool", "warm", "hot", "neutral"
    flavor = Column(JSON, nullable=False)  # ["bitter", "sweet", "salty", "sour", "acrid", "bland"]
    
    # ورود به مسیرهای
    meridian_entries = Column(JSON, nullable=False)  # ["liver_meridian", "heart_meridian"]
    
    # عملکرد‌های اساسی
    primary_functions = Column(JSON, nullable=False)  # [{function: "tonify_qi", importance: "high"}]
    
    # بیماری‌های درمان‌کنندگی
    treats_conditions = Column(JSON)  # [{condition: "fever", efficacy: 0.85}]
    
    # نوع گیاه
    part_used = Column(String(255))  # "whole_plant", "leaf", "root", "rhizome", "seed"
    
    # دوز توصیه‌شده
    typical_dosage = Column(String(255))
    dosage_range = Column(String(255))
    
    # موارد مخالفه
    contraindications = Column(JSON)  # [{condition: "pregnancy", reason: "..."}]
    
    # تعاملات
    herb_interactions = Column(JSON)  # [{herb: "ginger", interaction: "enhances_warming"}]
    
    # نکات ذخیره‌سازی
    storage_conditions = Column(Text)
    shelf_life = Column(String(100))
    
    # منابع
    classical_references = Column(JSON)  # ["Sheng Nong Ben Cao Jing"]
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
