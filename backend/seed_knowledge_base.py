"""
Knowledge Base Seed Data
Initial data for Avicenna, TCM, and Ayurveda knowledge bases

Usage:
    python backend/seed_knowledge_base.py
"""

from app.database import SessionLocal, engine, Base
from app.models.avicenna_knowledge_base import (
    AvicennaDisease, AvicennaTongueDiagnosis, AvicennaPulseDiagnosis,
    AvicennaHerbalRemedyDictionary, AvicennaMizajBalanceGuide
)
from app.models.tcm_knowledge_base import (
    TCMPatternDisharmony, TCMMeridian, TCMAcupuncturePoint,
    TCMHerbalFormula, TCMHerbDictionary
)
from app.models.ayurveda_knowledge_base import (
    AyurvedicConstitution, AyurvedicDisease, AyurvedicHerbDictionary,
    AyurvedicTherapy, AyurvedicDietaryGuideline, AyurvedicDhatu, AyurvedicSrotas
)


def seed_avicenna_knowledge():
    """Seed Avicenna medical knowledge"""
    db = SessionLocal()
    
    # بیماری‌های شناخت‌شده در طب سینایی
    avicenna_diseases = [
        AvicennaDisease(
            persian_name="تب",
            arabic_name="الحمى",
            latin_name="Febris",
            modern_equivalent="Fever",
            category="fever",
            severity="moderate",
            related_mizaj="garm_tar",
            involved_humors=[{"humor": "khoon", "excess": True}],
            symptoms=[
                {"symptom": "حرارت بدن", "severity": "high"},
                {"symptom": "خشکی دهان", "severity": "high"},
                {"symptom": "احساس سرما", "severity": "moderate"}
            ],
            tongue_signs=[
                {"sign": "رنگ زبان", "value": "red", "meaning": "گرمی خون"}
            ],
            pulse_signs=[
                {"sign": "نوع نبض", "value": "rapid", "meaning": "تسریع نبض"}
            ],
            treatments=[
                {"name": "کاشنی", "type": "herbal", "dosage": "غلیظ"},
                {"name": "گوسفندی", "type": "dietary"}
            ],
            source_books=["canon", "shifa"]
        ),
        AvicennaDisease(
            persian_name="صرع",
            arabic_name="الصرع",
            latin_name="Epilepsia",
            modern_equivalent="Epilepsy",
            category="neurological",
            severity="severe",
            related_mizaj="sard_khoshk",
            involved_humors=[{"humor": "soudaa", "excess": True}],
            symptoms=[
                {"symptom": "تشنج", "severity": "high"},
                {"symptom": "بیهوشی", "severity": "high"},
                {"symptom": "کف دهان", "severity": "moderate"}
            ],
            prognosis="بیماری مزمن که نیاز به درمان مداوم دارد",
            source_books=["canon"]
        ),
    ]
    
    # معیارهای تشخیصی زبان
    tongue_diagnoses = [
        AvicennaTongueDiagnosis(
            color_category="red",
            color_mizaj="garm_tar",
            color_description="رنگ قرمز نشان‌دهندۀ اضطراب خون و گرمی",
            coating_type="thin",
            coating_color="white",
            coating_meaning="پوشش نازک سفید نشان‌دهندۀ آغاز بیماری",
            texture="smooth",
            moisture="normal",
            related_mizaj="garm_tar",
            confidence=0.85
        ),
    ]
    
    # معیارهای تشخیصی نبض
    pulse_diagnoses = [
        AvicennaPulseDiagnosis(
            pulse_rate_range="fast",
            pulse_rate_min=80,
            pulse_rate_max=100,
            pulse_rhythm="regular",
            rhythm_meaning="نبض منظم",
            pulse_strength="strong",
            strength_meaning="نبض قوی نشان‌دهندۀ گرمی",
            pulse_depth="moderate",
            depth_meaning="عمق متوسط",
            related_mizaj="garm_tar",
            confidence=0.80
        ),
    ]
    
    # دارو‌های گیاهی
    herbal_remedies = [
        AvicennaHerbalRemedyDictionary(
            persian_name="کاشنی",
            arabic_name="الكاشنية",
            english_name="Chicory",
            latin_botanical_name="Cichorium intybus",
            potency="cold",
            moisture_property="moist",
            effects=[
                {"effect": "خنک‌کننده", "strength": "strong"},
                {"effect": "ملین", "strength": "moderate"}
            ],
            treats_diseases=[
                {"disease": "تب", "efficacy": 0.75},
                {"disease": "التهاب", "efficacy": 0.70}
            ],
            recommended_dosage="6-10 گرم در هر بار",
            avicenna_reference="قانون در طب، کتاب دوم"
        ),
    ]
    
    # راهنمای تعادل مزاج
    mizaj_guides = [
        AvicennaMizajBalanceGuide(
            mizaj="garm_tar",
            persian_name="گرم و تر",
            english_name="Hot and Moist",
            dominant_humor="khoon",
            recommended_foods=[
                {"food": "سبزیجات سرد", "benefit": "توازن", "frequency": "daily"},
                {"food": "کشمش و انجیر", "benefit": "تغذیه", "frequency": "regular"}
            ],
            recommended_activities=[
                {"activity": "پیاده‌روی", "frequency": "daily", "benefit": "گردش خون"}
            ],
            potential_diseases=[
                {"disease": "تب", "risk": "high"},
                {"disease": "التهاب", "risk": "moderate"}
            ]
        ),
    ]
    
    # Save Avicenna data
    for disease in avicenna_diseases:
        db.add(disease)
    for diagnosis in tongue_diagnoses:
        db.add(diagnosis)
    for diagnosis in pulse_diagnoses:
        db.add(diagnosis)
    for remedy in herbal_remedies:
        db.add(remedy)
    for guide in mizaj_guides:
        db.add(guide)
    
    db.commit()
    print("✅ Avicenna knowledge base seeded successfully")
    db.close()


def seed_tcm_knowledge():
    """Seed TCM knowledge"""
    db = SessionLocal()
    
    # نمط‌های بی‌هماهنگی
    tcm_patterns = [
        TCMPatternDisharmony(
            chinese_name="風熱感冒",
            pinyin_name="Feng Re Gan Mao",
            english_name="Wind-Heat Common Cold",
            pattern_category="exterior_heat",
            involved_organs=[{"organ": "lung", "role": "primary"}],
            involved_meridians=[{"meridian": "lung_meridian", "role": "affected"}],
            main_symptoms=[
                {"symptom": "headache", "frequency": "constant"},
                {"symptom": "sore_throat", "frequency": "constant"},
                {"symptom": "fever", "frequency": "constant"}
            ],
            tongue_findings=[
                {"finding": "color", "value": "red", "significance": "high"},
                {"finding": "coating", "value": "thin_yellow", "significance": "high"}
            ],
            pulse_findings=[
                {"finding": "position", "value": "superficial", "significance": "high"},
                {"finding": "speed", "value": "rapid", "significance": "high"}
            ],
            treatment_principles=[
                {"principle": "release_exterior", "importance": "primary"},
                {"principle": "clear_heat", "importance": "primary"}
            ]
        ),
    ]
    
    # مسیرهای انرژی
    meridians = [
        TCMMeridian(
            chinese_name="肝經",
            pinyin_name="Gan Jing",
            english_name="Liver Meridian",
            meridian_type="primary",
            associated_organ="liver",
            zang_fu_level="yin_organ",
            organ_clock_time="01:00-03:00",
            starting_location="Lateral corner of the big toenail",
            ending_location="Below the right costal margin"
        ),
    ]
    
    # نقاط آکوپنکچر
    acupuncture_points = [
        TCMAcupuncturePoint(
            meridian_id=1,
            point_code="LV3",
            chinese_name="太衝",
            pinyin_name="Taichong",
            english_name="Great Surge",
            location="On the dorsum of the foot",
            location_detail=[{"measurement": "between 1st and 2nd metatarsal", "direction": "web margin"}],
            functions=[
                {"function": "coursing liver qi", "importance": "high"},
                {"function": "subduing liver yang", "importance": "high"}
            ],
            indications=[
                {"indication": "migraine", "category": "head_disease"},
                {"indication": "eye pain", "category": "local_effect"}
            ]
        ),
    ]
    
    # فرمول‌های دارویی
    formulas = [
        TCMHerbalFormula(
            pattern_id=1,
            chinese_name="銀翹散",
            pinyin_name="Yin Qiao San",
            english_name="Honeysuckle and Forsythia Powder",
            formula_category="powder",
            treatment_principles=[
                {"principle": "release_exterior", "importance": "primary"},
                {"principle": "clear_heat", "importance": "primary"}
            ],
            herbs=[
                {"herb": "honeysuckle flower", "role": "chief", "dosage": "9g"},
                {"herb": "forsythia", "role": "chief", "dosage": "9g"},
                {"herb": "reed rhizome", "role": "deputy", "dosage": "6g"}
            ],
            indications=[
                {"indication": "wind-heat cold", "stage": "early"}
            ]
        ),
    ]
    
    # Save TCM data
    for pattern in tcm_patterns:
        db.add(pattern)
    for meridian in meridians:
        db.add(meridian)
    for formula in formulas:
        db.add(formula)
    
    db.commit()
    print("✅ TCM knowledge base seeded successfully")
    db.close()


def seed_ayurveda_knowledge():
    """Seed Ayurveda knowledge"""
    db = SessionLocal()
    
    # ساختار تشکیل‌کننده
    constitutions = [
        AyurvedicConstitution(
            dosha_type="vata",
            dosha_combination="vata",
            constitution_name="Vata Constitution",
            constitution_description="The wind principle - light, mobile, changeable",
            elements=[
                {"element": "space", "percentage": 50},
                {"element": "air", "percentage": 50}
            ],
            physical_characteristics=[
                {"trait": "body_frame", "value": "slender"},
                {"trait": "skin_type", "value": "dry"}
            ],
            mental_characteristics=[
                {"trait": "temperament", "value": "creative"},
                {"trait": "memory", "value": "quick_but_short_term"}
            ],
            digestive_characteristics=[
                {"trait": "digestion_strength", "value": "variable"},
                {"trait": "appetite", "value": "irregular"}
            ],
            skin_type="Dry, thin, cool",
            hair_type="Dry, curly, dark",
            sleep_duration_preference="6 hours",
            energy_level="Changeable",
            energy_pattern="Bursts of energy followed by fatigue",
            seasons_aggravating=["autumn", "early winter"],
            predisposition_to_diseases=[
                {"disease": "anxiety", "likelihood": "high"},
                {"disease": "insomnia", "likelihood": "high"}
            ],
            recommended_foods=[
                {"food": "warm_foods", "reason": "warming_effect", "frequency": "always"},
                {"food": "ghee", "reason": "nourishing", "frequency": "daily"}
            ]
        ),
    ]
    
    # بیماری‌های آیورودا
    diseases = [
        AyurvedicDisease(
            sanskrit_name="Jvara",
            english_name="Fever",
            modern_equivalent="Fever / Infection",
            disease_category="infectious",
            involved_doshas=[
                {"dosha": "pitta", "role": "primary"},
                {"dosha": "vata", "role": "secondary"}
            ],
            main_symptoms=[
                {"symptom": "high_body_temperature", "indication": "agni_involved"},
                {"symptom": "sweating", "indication": "toxin_release"},
                {"symptom": "weakness", "indication": "tissue_depletion"}
            ],
            causes=[
                {"cause": "poor_digestion", "type": "digestive", "weight": 0.6},
                {"cause": "ama_accumulation", "type": "metabolic", "weight": 0.7}
            ]
        ),
    ]
    
    # دارو‌های گیاهی
    herbs = [
        AyurvedicHerbDictionary(
            sanskrit_name="Guduchi",
            english_name="Tinospora Cordifolia",
            tastes=["bitter", "astringent"],
            potency="heating",
            post_digestive_effect="pungent",
            dosha_effects=[
                {"dosha": "pitta", "effect": "balancing"},
                {"dosha": "kapha", "effect": "reducing"}
            ],
            treats_conditions=[
                {"condition": "fever", "efficacy": 0.85},
                {"condition": "weak_immunity", "efficacy": 0.80}
            ],
            typical_dosage="3-6 grams",
            recommended_forms=["powder", "decoction", "juice"]
        ),
    ]
    
    # درمان‌های آیورودا
    therapies = [
        AyurvedicTherapy(
            sanskrit_name="Abhyanga",
            english_name="Ayurvedic Oil Massage",
            therapy_type="massage",
            therapeutic_goals=[
                {"goal": "nourish_tissues", "importance": "high"},
                {"goal": "promote_circulation", "importance": "high"}
            ],
            dosha_effects=[
                {"dosha": "vata", "effect": "pacifying"},
                {"dosha": "pitta", "effect": "calming"}
            ],
            treats_conditions=[
                {"condition": "stress", "efficacy": 0.90},
                {"condition": "arthritis", "efficacy": 0.75}
            ],
            session_duration="60 minutes",
            frequency="Daily"
        ),
    ]
    
    # دستورالعمل‌های تغذیه‌ای
    dietary_guidelines = [
        AyurvedicDietaryGuideline(
            guideline_name="Vata Balancing Diet",
            dosha_type="vata",
            beneficial_foods=[
                {"food": "warm_rice", "reason": "grounding", "frequency": "daily"},
                {"food": "ghee", "reason": "nourishing", "frequency": "daily"}
            ],
            foods_to_avoid=[
                {"food": "cold_drinks", "reason": "aggravating"},
                {"food": "dry_foods", "reason": "further_drying"}
            ],
            meal_timing=[
                {"time": "breakfast", "hours": "07:00-08:00", "note": "warm_and_nourishing"}
            ]
        ),
    ]
    
    # بافت‌های بدن
    dhatus = [
        AyurvedicDhatu(
            sanskrit_name="Rasa Dhatu",
            english_name="Plasma Tissue",
            order_number=1,
            functions=[
                {"function": "nourish_body", "role": "primary"},
                {"function": "support_immunity", "role": "secondary"}
            ]
        ),
    ]
    
    # قنوات بدن
    srotas = [
        AyurvedicSrotas(
            sanskrit_name="Rasavaha Srotas",
            english_name="Lymphatic Channels",
            functions=[
                {"function": "transport_plasma", "role": "primary"},
                {"function": "nourish_tissues", "role": "secondary"}
            ]
        ),
    ]
    
    # Save Ayurveda data
    for constitution in constitutions:
        db.add(constitution)
    for disease in diseases:
        db.add(disease)
    for herb in herbs:
        db.add(herb)
    for therapy in therapies:
        db.add(therapy)
    for guideline in dietary_guidelines:
        db.add(guideline)
    for dhatu in dhatus:
        db.add(dhatu)
    for srotas_item in srotas:
        db.add(srotas_item)
    
    db.commit()
    print("✅ Ayurveda knowledge base seeded successfully")
    db.close()


def main():
    """Seed all knowledge bases"""
    print("\n📚 Seeding Knowledge Bases...\n")
    
    try:
        seed_avicenna_knowledge()
        seed_tcm_knowledge()
        seed_ayurveda_knowledge()
        print("\n✅ All knowledge bases seeded successfully!\n")
    except Exception as e:
        print(f"\n❌ Error seeding knowledge bases: {e}\n")
        raise


if __name__ == "__main__":
    main()
