"""
Seed data برای پایگاه داده
داده‌های اولیه بر اساس تعاليم ابوعلی سینا
"""
import sys
sys.path.insert(0, '/backend')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.avicenna_diseases import (
    Disease, Symptom, DiseaseSymptomRelation, TraditionalRemedy,
    DiseaseRemediRelation, MedicalPlant
)


def seed_diseases(db: Session):
    """اضافه کردن بیماری‌ها"""
    
    diseases_data = [
        {
            "name_fa": "سوداء (ملانکولی)",
            "name_ar": "السوداء",
            "name_latin": "Melancholia",
            "category": "mental",
            "description": "بیماری روانی ناشی از تراکم صفراء سیاه",
            "avicenna_description": "غالبا در مردان ریاضی‌دان و فیلسوفان دیده می‌شود",
            "related_mizaj": ["sard", "khoshk"],
            "key_symptoms": ["تاریکی فکری", "ناامیدی", "بی‌حالی", "خواب کم"],
            "primary_affected_organs": ["مغز", "دل", "طحال"],
        },
        {
            "name_fa": "حمی",
            "name_ar": "الحمى",
            "name_latin": "Fever",
            "category": "fever",
            "description": "افزایش دمای بدن ناشی از عدم‌تعادل اخلاط",
            "avicenna_description": "چهار نوع حمی وجود دارد: یوماویه، دومیاویه، تراویه، ربعیه",
            "related_mizaj": ["garm"],
            "key_symptoms": ["تب", "تشنگی", "بی‌حالی", "سردرد"],
            "primary_affected_organs": ["قلب", "کبد"],
        },
        {
            "name_fa": "بات‌الریح (نقرس)",
            "name_ar": "النقرس",
            "name_latin": "Gout",
            "category": "joint",
            "description": "بیماری مفصلی ناشی از تراکم اخلاط بر",
            "avicenna_description": "بیشتر مردان پر‌خوار را تحت تأثیر قرار می‌دهد",
            "related_mizaj": ["garm", "tar"],
            "key_symptoms": ["درد شدید در مفاصل", "تورم", "سرخی", "حرارت"],
            "primary_affected_organs": ["مفاصل", "کبد"],
        },
        {
            "name_fa": "ربو (تنگی نفس)",
            "name_ar": "الربو",
            "name_latin": "Asthma",
            "category": "respiratory",
            "description": "تنگی نفس و دشواری تنفس",
            "avicenna_description": "ناشی از تراکم بخارات تر در ریه‌ها",
            "related_mizaj": ["tar"],
            "key_symptoms": ["تنگی نفس", "سرفه", "صریر", "فشار در سینه"],
            "primary_affected_organs": ["ریه", "دل"],
        },
        {
            "name_fa": "اسهال",
            "name_ar": "الإسهال",
            "name_latin": "Diarrhea",
            "category": "digestive",
            "description": "بیرون رفتن برطلب زیاد از روده",
            "avicenna_description": "به دنبال خوردن غذاهای سرد و تر",
            "related_mizaj": ["sard", "tar"],
            "key_symptoms": ["برطلب آب‌کی", "ضعف", "کمخونی"],
            "primary_affected_organs": ["معده", "روده"],
        },
    ]
    
    for disease_data in diseases_data:
        existing = db.query(Disease).filter(Disease.name_fa == disease_data["name_fa"]).first()
        if not existing:
            disease = Disease(**disease_data, is_active=True)
            db.add(disease)
    
    db.commit()
    print("✅ بیماری‌ها اضافه شد")


def seed_symptoms(db: Session):
    """اضافه کردن علائم"""
    
    symptoms_data = [
        {"name_fa": "سردرد", "name_ar": "الصداع", "symptom_type": "درد", "mizaj_related": ["garm"]},
        {"name_fa": "تشنگی", "name_ar": "العطش", "symptom_type": "احساس", "mizaj_related": ["garm"]},
        {"name_fa": "بی‌حالی", "name_ar": "الضعف", "symptom_type": "کمی انرژی", "mizaj_related": ["sard", "khoshk"]},
        {"name_fa": "سرفه", "name_ar": "السعال", "symptom_type": "تنفسی", "mizaj_related": ["tar"]},
        {"name_fa": "درد شکم", "name_ar": "آلام البطن", "symptom_type": "درد", "mizaj_related": ["garm"]},
        {"name_fa": "تورم", "name_ar": "الورم", "symptom_type": "فیزیکی", "mizaj_related": ["garm", "tar"]},
        {"name_fa": "خشکی دهان", "name_ar": "جفاف الفم", "symptom_type": "احساس", "mizaj_related": ["sard", "khoshk"]},
        {"name_fa": "ناامیدی", "name_ar": "الإحباط", "symptom_type": "روانی", "mizaj_related": ["sard"]},
    ]
    
    for symptom_data in symptoms_data:
        existing = db.query(Symptom).filter(Symptom.name_fa == symptom_data["name_fa"]).first()
        if not existing:
            symptom = Symptom(**symptom_data)
            db.add(symptom)
    
    db.commit()
    print("✅ علائم اضافه شد")


def seed_plants(db: Session):
    """اضافه کردن گیاهان دارویی"""
    
    plants_data = [
        {
            "name_fa": "زنجبیل",
            "name_ar": "الزنجبيل",
            "name_scientific": "Zingiber officinale",
            "plant_part_used": "ریزوم",
            "temperature_nature": "garm",
            "moisture_nature": "khoshk",
            "degree_of_strength": "3",
            "medicinal_uses": ["درمان سرفه", "بهبود هضم", "کاهش بی‌حالی"],
            "balances_mizaj": ["sard", "khoshk"],
        },
        {
            "name_fa": "بابونه",
            "name_ar": "البابونج",
            "name_scientific": "Matricaria chamomilla",
            "plant_part_used": "گل",
            "temperature_nature": "garm",
            "moisture_nature": "tar",
            "degree_of_strength": "1",
            "medicinal_uses": ["آرام‌بخشی", "درمان اضطراب", "تسکین درد"],
            "balances_mizaj": ["garm_tar"],
        },
        {
            "name_fa": "عرقسوس",
            "name_ar": "العرقسوس",
            "name_scientific": "Glycyrrhiza glabra",
            "plant_part_used": "ریزوم",
            "temperature_nature": "garm",
            "moisture_nature": "tar",
            "degree_of_strength": "1",
            "medicinal_uses": ["درمان سرفه", "محافظت معده", "آرام‌بخشی"],
            "balances_mizaj": ["khoshk"],
        },
        {
            "name_fa": "رز",
            "name_ar": "الورد",
            "name_scientific": "Rosa damascena",
            "plant_part_used": "گل",
            "temperature_nature": "sard",
            "moisture_nature": "khoshk",
            "degree_of_strength": "1",
            "medicinal_uses": ["تسکین سرفه", "بهبود خلق", "سرد‌کننده"],
            "balances_mizaj": ["garm"],
        },
    ]
    
    for plant_data in plants_data:
        existing = db.query(MedicalPlant).filter(MedicalPlant.name_fa == plant_data["name_fa"]).first()
        if not existing:
            plant = MedicalPlant(**plant_data)
            db.add(plant)
    
    db.commit()
    print("✅ گیاهان دارویی اضافه شد")


def seed_remedies(db: Session):
    """اضافه کردن درمان‌های سنتی"""
    
    remedies_data = [
        {
            "name_fa": "شربت زنجبیل",
            "name_ar": "شراب الزنجبيل",
            "remedy_type": "herbal",
            "preparation_method": "غوطه زنجبیل در آب گرم و اضافه عسل",
            "usage_method": "نوشیدن",
            "dosage": "فنجان یکی",
            "frequency": "روزی دو بار",
            "duration": "دو هفته",
            "temperature_nature": "garm",
            "moisture_nature": "khoshk",
            "effectiveness_level": "عالی",
            "used_for_conditions": ["تب", "سرفه", "بی‌حالی"],
        },
        {
            "name_fa": "چای بابونه",
            "name_ar": "شاي البابونج",
            "remedy_type": "herbal",
            "preparation_method": "غوطه بابونه در آب جوش",
            "usage_method": "نوشیدن",
            "dosage": "فنجان",
            "frequency": "روزی سه بار",
            "duration": "دو هفته",
            "temperature_nature": "garm",
            "moisture_nature": "tar",
            "effectiveness_level": "خوب",
            "used_for_conditions": ["اضطراب", "بی‌خوابی", "درد شکم"],
        },
        {
            "name_fa": "تریاق",
            "name_ar": "الترياق",
            "remedy_type": "herbal",
            "preparation_method": "ترکیب چند گیاه و عسل",
            "usage_method": "خوردن",
            "dosage": "قاشق چایخوری",
            "frequency": "روزی یک بار",
            "duration": "ماه",
            "temperature_nature": "garm",
            "moisture_nature": "tar",
            "effectiveness_level": "عالی",
            "used_for_conditions": ["سوداء", "ضعف عمومی", "پیری"],
        },
    ]
    
    for remedy_data in remedies_data:
        existing = db.query(TraditionalRemedy).filter(TraditionalRemedy.name_fa == remedy_data["name_fa"]).first()
        if not existing:
            remedy = TraditionalRemedy(**remedy_data, is_active=True)
            db.add(remedy)
    
    db.commit()
    print("✅ درمان‌های سنتی اضافه شد")


def main():
    """اجرای تمام seed‌ها"""
    db = SessionLocal()
    
    try:
        print("🌱 شروع پر کردن پایگاه داده...")
        seed_diseases(db)
        seed_symptoms(db)
        seed_plants(db)
        seed_remedies(db)
        print("✅ پایگاه داده با موفقیت پر شد!")
    except Exception as e:
        print(f"❌ خطا: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
