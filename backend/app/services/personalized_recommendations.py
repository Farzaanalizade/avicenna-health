"""
سرویس توصیه‌های شخصی‌شده براساس پروفایل بیمار
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.models.avicenna_diagnosis import DiagnosticFinding, PulseAnalysis, UrineAnalysis, TongueCoating
from app.models.avicenna_diseases import TraditionalRemedy, MizajBalanceTreatment
from app.crud.avicenna_diseases import TraditionalRemedyOps


class PersonalizedRecommendationService:
    """سرویس ارائه توصیه‌های شخصی‌شده"""
    
    @staticmethod
    def generate_personalized_plan(patient: Patient, db: Session) -> Dict:
        """تولید برنامه شخصی‌شده برای بیمار"""
        
        # دریافت آخرین تشخیص
        latest_diagnosis = db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient.id
        ).order_by(DiagnosticFinding.created_at.desc()).first()
        
        if not latest_diagnosis:
            return {"error": "هیچ تشخیص قبلی برای این بیمار وجود ندارد"}
        
        plan = {
            "patient_id": patient.id,
            "patient_name": patient.full_name,
            "created_at": datetime.now(),
            "valid_until": datetime.now() + timedelta(days=30),
            "current_mizaj": latest_diagnosis.primary_mizaj,
            "target_mizaj": "motadel",
            "health_status": latest_diagnosis.overall_health_status,
            "phases": []
        }
        
        # مرحله ۱: تطهیر و تنقیه (اگر لزم باشد)
        if latest_diagnosis.primary_mizaj != "motadel":
            plan["phases"].append(
                PersonalizedRecommendationService._phase_1_cleansing(
                    latest_diagnosis, patient, db
                )
            )
        
        # مرحله ۲: تعادل‌سازی
        plan["phases"].append(
            PersonalizedRecommendationService._phase_2_balancing(
                latest_diagnosis, patient, db
            )
        )
        
        # مرحله ۳: تثبیت و نگهداری
        plan["phases"].append(
            PersonalizedRecommendationService._phase_3_maintenance(patient, db)
        )
        
        return plan
    
    @staticmethod
    def _phase_1_cleansing(
        diagnosis: DiagnosticFinding,
        patient: Patient,
        db: Session
    ) -> Dict:
        """مرحله اول: تطهیر و تنقیه (۱۰ روز)"""
        
        cleansing_treatments = {
            "garm": ["سنجاب", "گل‌سرخ", "عرقسوس"],
            "sard": ["زنجبیل", "دارچین", "فلفل"],
            "tar": ["زعفران", "گیاه‌تریاق", "بهاری"],
            "khoshk": ["عسل", "روغن‌کریشه", "بادام"],
        }
        
        primary_mizaj = diagnosis.primary_mizaj
        remedies = cleansing_treatments.get(primary_mizaj, [])
        
        return {
            "phase": 1,
            "duration": "۱۰ روز",
            "title": "تطهیر و تنقیه",
            "description": f"تطهیر بدن از اخلاط اضافی {primary_mizaj}",
            "main_treatments": remedies,
            "frequency": "روزی ۲ بار",
            "diet": PersonalizedRecommendationService._get_cleansing_diet(primary_mizaj),
            "lifestyle": [
                "حمام آب گرم روزانه",
                "ماساژ بدن با روغن‌های مناسب",
                "استراحت کافی",
                "پرهیز از فعالیت شدید"
            ],
            "warnings": [
                "در صورت بدحالی، فوری متصل شوید",
                "مصرف آب کافی ضروری است",
                "خواب منظم رعایت شود"
            ]
        }
    
    @staticmethod
    def _phase_2_balancing(
        diagnosis: DiagnosticFinding,
        patient: Patient,
        db: Session
    ) -> Dict:
        """مرحله دوم: تعادل‌سازی (۲۰ روز)"""
        
        balancing_map = {
            "garm": {
                "opposite_mizaj": "sard",
                "treatments": ["بابونه", "رز", "نعناع"],
                "diet": ["آب", "میوه سرد", "دوغ"]
            },
            "sard": {
                "opposite_mizaj": "garm",
                "treatments": ["زنجبیل", "دارچین", "فلفل"],
                "diet": ["گوشت گرم", "چای", "عسل"]
            },
            "tar": {
                "opposite_mizaj": "khoshk",
                "treatments": ["زعفران", "بهاری", "گل‌سرخ"],
                "diet": ["نان خشک", "گوشت بریان", "سبزیجات خام"]
            },
            "khoshk": {
                "opposite_mizaj": "tar",
                "treatments": ["روغن‌کریشه", "عسل", "شیر"],
                "diet": ["روغن زیتون", "دوغ", "میوه مرطوب"]
            }
        }
        
        primary_mizaj = diagnosis.primary_mizaj
        balance_info = balancing_map.get(primary_mizaj, {})
        
        return {
            "phase": 2,
            "duration": "۲۰ روز",
            "title": "تعادل‌سازی مزاج",
            "description": f"تعادل‌سازی مزاج {primary_mizaj} به مزاج {balance_info.get('opposite_mizaj', 'متعادل')}",
            "main_treatments": balance_info.get("treatments", []),
            "frequency": "روزی ۲-۳ بار",
            "diet": balance_info.get("diet", []),
            "lifestyle": [
                "فعالیت بدنی معمول",
                "ماساژ ۲ بار هفتگی",
                "یوگا یا تمرینات آرام",
                "مدیتیشن ۱۵ دقیقه‌ای روزانه"
            ],
            "monitoring": [
                "ثبت وضعیت روزانه",
                "پیگیری انرژی و حالت‌روحی",
                "مراقبت از علائم تغییر"
            ]
        }
    
    @staticmethod
    def _phase_3_maintenance(patient: Patient, db: Session) -> Dict:
        """مرحله سوم: تثبیت و نگهداری (۳۰ روز)"""
        
        return {
            "phase": 3,
            "duration": "۳۰ روز",
            "title": "تثبیت و نگهداری",
            "description": "حفظ تعادل مزاج و سلامت عمومی",
            "main_treatments": [
                "تریاق (بصورت پیشگیری)",
                "شربت‌های فصلی",
                "روغن‌کشی هفتگی"
            ],
            "frequency": "روزی ۱ بار یا حسب نیاز",
            "diet": [
                "رژیم متعادل براساس مزاج",
                "مصرف میوه‌های فصلی",
                "پرهیز از غذاهای پروسس‌شده"
            ],
            "lifestyle": [
                "ورزش منظم ۵ روز هفتگی",
                "خواب ۷-۸ ساعت شبانه",
                "مدیتیشن و یوگا",
                "مراعات بهداشت روان"
            ],
            "prevention": [
                "بررسی دوره‌ای ۱۵ روزی",
                "انطباق رژیم با فصل‌های مختلف",
                "مصرف شربت‌های محافظتی"
            ]
        }
    
    @staticmethod
    def generate_weekly_schedule(patient: Patient, db: Session) -> Dict:
        """تولید برنامه هفتگی برای بیمار"""
        
        schedule = {
            "week_starting": datetime.now(),
            "patient_id": patient.id,
            "daily_routines": {}
        }
        
        days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
        
        for day in days:
            schedule["daily_routines"][day] = {
                "morning": [
                    "بیدار شدن: ۶ صبح",
                    "نوشیدن آب گرم با عسل",
                    "ورزش سبک ۱۵ دقیقه",
                    "صحبت‌کنی و دوش"
                ],
                "midday": [
                    "ناهار: غذای فصلی متعادل",
                    "استراحت ۱۵ دقیقه",
                    "قدم زنی ۲۰ دقیقه"
                ],
                "evening": [
                    "شام: غذای سبک",
                    "چای گیاهی",
                    "مدیتیشن ۱۰ دقیقه"
                ],
                "night": [
                    "خواب منظم ۲۲:۳۰",
                    "اتاق خنک و تاریک"
                ]
            }
            
            # اضافه کردن فعالیت‌های خاص روزانه
            if day == "سه‌شنبه" or day == "جمعه":
                schedule["daily_routines"][day]["special"] = [
                    "ماساژ بدن با روغن مناسب",
                    "حمام آب گرم ۲۰ دقیقه"
                ]
        
        return schedule
    
    @staticmethod
    def generate_monthly_dietary_plan(patient: Patient, mizaj: str, db: Session) -> Dict:
        """تولید برنامه غذایی ماهانه"""
        
        dietary_guidelines = {
            "garm": {
                "breakfast": [
                    "دوغ با نعناع و خیار",
                    "نان سفید و پنیر",
                    "میوه‌های سرد"
                ],
                "lunch": [
                    "مرغ سفید پخته",
                    "برنج سفید",
                    "سبزیجات تازه",
                    "آب لیمو"
                ],
                "dinner": [
                    "سوپ سبزیجات سرد",
                    "گوشت مرغ",
                    "سالاد",
                    "آب"
                ],
                "snacks": [
                    "خیار",
                    "خربزه",
                    "کیوی",
                    "آب‌میوه طازه"
                ],
                "prohibited": [
                    "غذاهای چرب و تیز",
                    "ادویه‌های قوی",
                    "الکل",
                    "قهوه و چای قوی"
                ]
            },
            "sard": {
                "breakfast": [
                    "چای سرخ با عسل",
                    "تخم‌مرغ",
                    "نان سیاه",
                    "بادام"
                ],
                "lunch": [
                    "گوشت قرمز پختی",
                    "برنج یا لوبیا",
                    "سبزیجات گرم‌شده",
                    "آب جوش"
                ],
                "dinner": [
                    "سوپ گوشت",
                    "گوشت آتش‌پخته",
                    "سبزی طبخ‌شده",
                    "چای"
                ],
                "snacks": [
                    "خشکبار",
                    "بادام و فندق",
                    "عسل",
                    "خرما"
                ],
                "prohibited": [
                    "مواد سرد",
                    "دوغ",
                    "میوه سرد",
                    "غذاهای خام"
                ]
            }
        }
        
        guidelines = dietary_guidelines.get(mizaj, dietary_guidelines["garm"])
        
        return {
            "month": datetime.now().strftime("%B %Y"),
            "patient_mizaj": mizaj,
            "daily_guidelines": guidelines,
            "notes": [
                "هر روز ۳ وعده اصلی و ۲ وعده فرعی",
                "مصرف آب: حداقل ۸ لیوان روزانه",
                "غذا را آرام بخورید",
                "شام ۳ ساعت قبل از خواب"
            ],
            "special_recipes": PersonalizedRecommendationService._get_special_recipes(mizaj)
        }
    
    @staticmethod
    def _get_special_recipes(mizaj: str) -> List[Dict]:
        """دستور‌های خاص براساس مزاج"""
        
        recipes = {
            "garm": [
                {
                    "name": "شربت رز و بابونه",
                    "ingredients": ["گل‌سرخ", "بابونه", "آب", "عسل"],
                    "instructions": "۲ قاشق گل‌سرخ و بابونه را در یک لیتر آب جوش بجوشانید و عسل اضافه کنید",
                    "frequency": "روزی ۲ بار"
                },
                {
                    "name": "سلاد خنک",
                    "ingredients": ["خیار", "گوجه", "پیاز", "نعناع", "روغن زیتون"],
                    "instructions": "سبزیجات را خردریز کرده، نعناع اضافه کنید و روغن زیتون اچھلانید",
                    "frequency": "هر روز ناهار"
                }
            ],
            "sard": [
                {
                    "name": "شربت زنجبیل و دارچین",
                    "ingredients": ["زنجبیل", "دارچین", "آب", "عسل"],
                    "instructions": "۱ قاشق چایخوری زنجبیل و دارچین را در یک لیتر آب جوش بجوشانید",
                    "frequency": "روزی ۲ بار"
                },
                {
                    "name": "سوپ گوشت و لوبیا",
                    "ingredients": ["گوشت", "لوبیا", "سبزیجات", "ادویه‌های گرم"],
                    "instructions": "گوشت را پخته، لوبیا و سبزیجات اضافه کنید و تا تصفیه بپزید",
                    "frequency": "هفتگی ۲ بار"
                }
            ]
        }
        
        return recipes.get(mizaj, [])
    
    @staticmethod
    def generate_self_monitoring_guide(patient: Patient, db: Session) -> Dict:
        """راهنمای خود مراقبتی برای بیمار"""
        
        return {
            "patient_id": patient.id,
            "guide_title": "راهنمای خود مراقبتی روزانه",
            "daily_checks": [
                {
                    "time": "صبح",
                    "checks": [
                        "بررسی رنگ زبان",
                        "شمارش نبض",
                        "بررسی رنگ ادرار",
                        "ثبت انرژی (۱-۱۰)"
                    ]
                },
                {
                    "time": "عصر",
                    "checks": [
                        "بررسی حالت روحی",
                        "ثبت غذا خورده",
                        "بررسی علائم جدید"
                    ]
                },
                {
                    "time": "شب",
                    "checks": [
                        "بررسی کیفیت خواب",
                        "ثبت درجه حرارت",
                        "خلاصه‌سازی روز"
                    ]
                }
            ],
            "warning_signs": [
                "تغییر شدید در رنگ زبان",
                "تب ناگهانی",
                "نبض بسیار سریع یا آهسته",
                "درد شدید",
                "ادرار غیرطبیعی"
            ],
            "when_to_contact_doctor": [
                "هر گاه علائم هشداری مشاهده شد",
                "اگر درمان کار نکند",
                "اگر عوارض جانبی مشاهده شد",
                "هر ۱۵ روز برای بررسی دوره‌ای"
            ],
            "symptom_tracker": {
                "pain_level": "۱-۱۰",
                "energy_level": "۱-۱۰",
                "sleep_quality": "خوب/متوسط/بد",
                "mood": "خوشحال/عادی/ناراحت",
                "appetite": "عادی/کم/زیاد"
            }
        }
