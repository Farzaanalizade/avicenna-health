"""
داده‌های گسترده‌تر برای بیماری‌ها و درمان‌های سنتی
"""
import sys
sys.path.insert(0, '/backend')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.avicenna_diseases import Disease, Symptom, TraditionalRemedy, MedicalPlant


EXTENDED_DISEASES = [
    # بیماری‌های تنفسی
    {
        "name_fa": "سل (درن)",
        "name_ar": "السل",
        "category": "respiratory",
        "related_mizaj": ["sard", "khoshk"],
        "key_symptoms": ["سرفه مزمن", "خونریزی ریه", "تب شامی", "لاغری"],
        "primary_affected_organs": ["ریه", "دل"],
    },
    {
        "name_fa": "سرفه خشک",
        "name_ar": "السعال الجاف",
        "category": "respiratory",
        "related_mizaj": ["khoshk"],
        "key_symptoms": ["سرفه بدون بلغم", "خراش حلق"],
        "primary_affected_organs": ["ریه"],
    },
    
    # بیماری‌های گوارشی
    {
        "name_fa": "یرقان (ایکتر)",
        "name_ar": "اليرقان",
        "category": "digestive",
        "related_mizaj": ["garm"],
        "key_symptoms": ["زردی پوست", "زردی چشم", "بی‌اشتهایی"],
        "primary_affected_organs": ["کبد", "صفرا"],
    },
    {
        "name_fa": "قولنج (مغص)",
        "name_ar": "القولنج",
        "category": "digestive",
        "related_mizaj": ["garm", "tar"],
        "key_symptoms": ["درد شدید شکم", "تورم شکم"],
        "primary_affected_organs": ["روده"],
    },
    {
        "name_fa": "دیسپپسیا (بدهضمی)",
        "name_ar": "سوء الهضم",
        "category": "digestive",
        "related_mizaj": ["sard"],
        "key_symptoms": ["عدم هضم", "نفخ", "احساس سنگینی"],
        "primary_affected_organs": ["معده"],
    },
    
    # بیماری‌های پوستی
    {
        "name_fa": "جرب",
        "name_ar": "الجرب",
        "category": "skin",
        "related_mizaj": ["garm", "tar"],
        "key_symptoms": ["خارش شدید", "زخم و ترشح"],
        "primary_affected_organs": ["پوست"],
    },
    {
        "name_fa": "برص (ویتیلیگو)",
        "name_ar": "البهاق",
        "category": "skin",
        "related_mizaj": ["sard", "khoshk"],
        "key_symptoms": ["لکه‌های سفید", "عدم احساس"],
        "primary_affected_organs": ["پوست"],
    },
    
    # بیماری‌های عصبی
    {
        "name_fa": "فالج",
        "name_ar": "الفالج",
        "category": "neurological",
        "related_mizaj": ["sard", "khoshk"],
        "key_symptoms": ["فلج اندام", "ضعف عضلانی"],
        "primary_affected_organs": ["مغز", "اعصاب"],
    },
    {
        "name_fa": "میگرن",
        "name_ar": "الشقيقة",
        "category": "neurological",
        "related_mizaj": ["garm"],
        "key_symptoms": ["سردرد یک‌طرفه", "تهوع"],
        "primary_affected_organs": ["مغز"],
    },
    
    # بیماری‌های قلبی
    {
        "name_fa": "خفقان",
        "name_ar": "الخفقان",
        "category": "circulatory",
        "related_mizaj": ["garm", "tar"],
        "key_symptoms": ["تپش قلب", "ترس"],
        "primary_affected_organs": ["قلب"],
    },
    {
        "name_fa": "فشار خون بالا",
        "name_ar": "ارتفاع ضغط الدم",
        "category": "circulatory",
        "related_mizaj": ["garm"],
        "key_symptoms": ["سردرد", "سرخی چهره", "تنگی نفس"],
        "primary_affected_organs": ["قلب", "رگ‌ها"],
    },
]

EXTENDED_SYMPTOMS = [
    {"name_fa": "تب شامی", "symptom_type": "تب", "mizaj_related": ["garm"]},
    {"name_fa": "لاغری", "symptom_type": "تغییر وزن", "mizaj_related": ["khoshk"]},
    {"name_fa": "تورم بدن", "symptom_type": "تورم", "mizaj_related": ["tar"]},
    {"name_fa": "نفخ شکم", "symptom_type": "گوارشی", "mizaj_related": ["sard"]},
    {"name_fa": "یبوست", "symptom_type": "گوارشی", "mizaj_related": ["khoshk"]},
    {"name_fa": "دشواری تنفس", "symptom_type": "تنفسی", "mizaj_related": ["tar"]},
    {"name_fa": "جوش و خارش", "symptom_type": "پوستی", "mizaj_related": ["garm"]},
    {"name_fa": "حساسیت سرما", "symptom_type": "احساس", "mizaj_related": ["sard"]},
    {"name_fa": "تپش دل", "symptom_type": "قلبی", "mizaj_related": ["garm", "tar"]},
    {"name_fa": "بی‌خوابی", "symptom_type": "عصبی", "mizaj_related": ["garm"]},
    {"name_fa": "خمیازه و نعاس", "symptom_type": "عصبی", "mizaj_related": ["sard"]},
    {"name_fa": "التهاب دهان", "symptom_type": "درمولوژی", "mizaj_related": ["garm"]},
]

EXTENDED_PLANTS = [
    {
        "name_fa": "سنجاب",
        "name_scientific": "Plantago major",
        "plant_part_used": "برگ",
        "temperature_nature": "sard",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["ضد سرفه", "بهبود ریه", "التئام زخم"],
        "balances_mizaj": ["garm"],
    },
    {
        "name_fa": "دارچین",
        "name_scientific": "Cinnamomum verum",
        "plant_part_used": "پوست تنه",
        "temperature_nature": "garm",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["بهبود گردش خون", "گرمادهی", "ضد بکتری"],
        "balances_mizaj": ["sard", "khoshk"],
    },
    {
        "name_fa": "شاه‌بهرام (خانه‌بهار)",
        "name_scientific": "Satureja montana",
        "plant_part_used": "برگ",
        "temperature_nature": "garm",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["بهبود هضم", "ضد درد", "ضد تشنج"],
        "balances_mizaj": ["sard"],
    },
    {
        "name_fa": "خاکشیر",
        "name_scientific": "Geranium sibiricum",
        "plant_part_used": "ریشه",
        "temperature_nature": "sard",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["جراحت و زخم", "اسهال", "درد شکم"],
        "balances_mizaj": ["garm"],
    },
    {
        "name_fa": "آویشن",
        "name_scientific": "Thymus vulgaris",
        "plant_part_used": "برگ",
        "temperature_nature": "garm",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["ضد سرفه", "ضد آسم", "بهبود تنفس"],
        "balances_mizaj": ["tar"],
    },
    {
        "name_fa": "نعناع فلفلی",
        "name_scientific": "Mentha piperita",
        "plant_part_used": "برگ",
        "temperature_nature": "sard",
        "moisture_nature": "khoshk",
        "medicinal_uses": ["بهبود هضم", "سرد‌کننده", "ضد تشنج"],
        "balances_mizaj": ["garm"],
    },
    {
        "name_fa": "الوئه ورا",
        "name_scientific": "Aloe barbadensis",
        "plant_part_used": "ژل درونی",
        "temperature_nature": "sard",
        "moisture_nature": "tar",
        "medicinal_uses": ["التئام زخم", "محافظت معده", "ملین"],
        "balances_mizaj": ["garm"],
    },
    {
        "name_fa": "لیمو",
        "name_scientific": "Citrus limon",
        "plant_part_used": "میوه",
        "temperature_nature": "sard",
        "moisture_nature": "tar",
        "medicinal_uses": ["ضد اسکوربوت", "فرز‌کننده", "کمک به هضم"],
        "balances_mizaj": ["garm"],
    },
]

EXTENDED_REMEDIES = [
    {
        "name_fa": "شربت سنجاب",
        "remedy_type": "herbal",
        "preparation_method": "جوشاندن برگ‌های سنجاب در آب",
        "dosage": "فنجان",
        "frequency": "روزی ۲ بار",
        "used_for_conditions": ["سرفه", "ریه‌ها"],
        "temperature_nature": "sard",
    },
    {
        "name_fa": "شیر و عسل",
        "remedy_type": "herbal",
        "preparation_method": "گرم‌کردن شیر و اضافه کردن عسل",
        "dosage": "یک فنجان",
        "frequency": "شب قبل از خواب",
        "used_for_conditions": ["سرفه", "بی‌خوابی"],
        "temperature_nature": "garm",
    },
    {
        "name_fa": "دوغ و نعناع",
        "remedy_type": "herbal",
        "preparation_method": "مخلوط کردن دوغ سرد و نعناع تازه",
        "dosage": "یک لیوان",
        "frequency": "روزی دو بار",
        "used_for_conditions": ["گرما", "بدهضمی"],
        "temperature_nature": "sard",
    },
    {
        "name_fa": "قهوه‌گل",
        "remedy_type": "herbal",
        "preparation_method": "جوشاندن گل‌های گل‌سرخ و بابونه",
        "dosage": "فنجان",
        "frequency": "روزی یک بار",
        "used_for_conditions": ["آرام‌بخشی", "بی‌اشتهایی"],
        "temperature_nature": "sard",
    },
    {
        "name_fa": "مرهم زعفران",
        "remedy_type": "herbal",
        "preparation_method": "حل کردن زعفران در روغن",
        "dosage": "مالش موضعی",
        "frequency": "روزی یک بار",
        "used_for_conditions": ["زخم", "آفتاب‌سوختگی"],
        "temperature_nature": "garm",
    },
]


def seed_extended_data(db: Session):
    """اضافه کردن داده‌های گسترده"""
    
    print("🌱 اضافه کردن بیماری‌های گسترده...")
    for disease_data in EXTENDED_DISEASES:
        existing = db.query(Disease).filter(Disease.name_fa == disease_data["name_fa"]).first()
        if not existing:
            disease = Disease(**disease_data, is_active=True)
            db.add(disease)
    
    print("🌱 اضافه کردن علائم گسترده...")
    for symptom_data in EXTENDED_SYMPTOMS:
        existing = db.query(Symptom).filter(Symptom.name_fa == symptom_data["name_fa"]).first()
        if not existing:
            symptom = Symptom(**symptom_data)
            db.add(symptom)
    
    print("🌱 اضافه کردن گیاهان دارویی گسترده...")
    for plant_data in EXTENDED_PLANTS:
        existing = db.query(MedicalPlant).filter(MedicalPlant.name_fa == plant_data["name_fa"]).first()
        if not existing:
            plant = MedicalPlant(**plant_data)
            db.add(plant)
    
    print("🌱 اضافه کردن درمان‌های سنتی گسترده...")
    for remedy_data in EXTENDED_REMEDIES:
        existing = db.query(TraditionalRemedy).filter(TraditionalRemedy.name_fa == remedy_data["name_fa"]).first()
        if not existing:
            remedy = TraditionalRemedy(**remedy_data, is_active=True)
            db.add(remedy)
    
    db.commit()
    print("✅ تمام داده‌های گسترده اضافه شد!")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_extended_data(db)
    except Exception as e:
        print(f"❌ خطا: {e}")
        db.rollback()
    finally:
        db.close()
