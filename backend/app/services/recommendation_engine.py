"""
Recommendation Engine

این سرویس بر اساس نتایج تطابق، توصیه‌های درمانی شامل:
- گیاهان دارویی
- توصیه‌های غذایی
- توصیه‌های سبک زندگی
- روش‌های درمانی

را تولید می‌کند.
"""

import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.knowledge_base_models import (
    AvicennaDisease,
    AvicennaHerb,
    AvicennaTreatment,
    TCMPatternDisharmony,
    TCMHerb,
    TCMTreatment,
    AyurvedicDisease,
    AyurvedicHerb,
    AyurvedicTreatment,
)

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    موتور توصیه‌های درمانی
    """

    def __init__(self):
        """Initialize the engine"""
        self.max_recommendations = 5
        self.treatment_duration_days = 30

    async def get_avicenna_recommendations(
        self,
        disease_id: int,
        db: Session
    ) -> Dict:
        """
        دریافت توصیه‌های Avicenna برای یک بیماری
        
        Args:
            disease_id: شناسه بیماری Avicenna
            db: جلسه پایگاه داده
            
        Returns:
            {
                herbs: [...],
                diet: [...],
                lifestyle: [...],
                treatments: [...],
                duration_days: 30
            }
        """
        try:
            disease = db.query(AvicennaDisease).filter(
                AvicennaDisease.id == disease_id
            ).first()
            
            if not disease:
                return {"error": "Disease not found"}
            
            # دریافت گیاهان
            herbs = db.query(AvicennaHerb).filter(
                AvicennaHerb.disease_id == disease_id
            ).limit(self.max_recommendations).all()
            
            # دریافت درمان‌ها
            treatments = db.query(AvicennaTreatment).filter(
                AvicennaTreatment.disease_id == disease_id
            ).limit(self.max_recommendations).all()
            
            recommendations = {
                "disease_id": disease_id,
                "disease_name": disease.name_fa,
                "tradition": "avicenna",
                "herbs": [
                    {
                        "id": herb.id,
                        "name": herb.name_fa,
                        "name_en": herb.name_en,
                        "dosage": herb.dosage,
                        "frequency": herb.frequency,
                        "preparation": herb.preparation_method,
                        "properties": herb.medicinal_properties,
                        "cautions": herb.cautions,
                    }
                    for herb in herbs
                ],
                "diet": self._get_avicenna_diet_recommendations(disease),
                "lifestyle": self._get_avicenna_lifestyle_recommendations(disease),
                "treatments": [
                    {
                        "name": treatment.name_fa,
                        "name_en": treatment.name_en,
                        "description": treatment.description_fa,
                        "frequency": treatment.frequency,
                        "duration_days": treatment.duration_days or 30,
                    }
                    for treatment in treatments
                ],
                "duration_days": self.treatment_duration_days,
                "follow_up_days": 14,
                "created_at": datetime.now().isoformat(),
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting Avicenna recommendations: {e}")
            return {"error": str(e)}

    async def get_tcm_recommendations(
        self,
        pattern_id: int,
        db: Session
    ) -> Dict:
        """
        دریافت توصیه‌های TCM برای یک الگو
        """
        try:
            pattern = db.query(TCMPatternDisharmony).filter(
                TCMPatternDisharmony.id == pattern_id
            ).first()
            
            if not pattern:
                return {"error": "Pattern not found"}
            
            # دریافت گیاهان
            herbs = db.query(TCMHerb).filter(
                TCMHerb.pattern_id == pattern_id
            ).limit(self.max_recommendations).all()
            
            # دریافت درمان‌ها
            treatments = db.query(TCMTreatment).filter(
                TCMTreatment.pattern_id == pattern_id
            ).limit(self.max_recommendations).all()
            
            recommendations = {
                "pattern_id": pattern_id,
                "pattern_name": pattern.name_fa,
                "tradition": "tcm",
                "organs_affected": pattern.organs,
                "imbalance_type": pattern.imbalance_type,
                "herbs": [
                    {
                        "id": herb.id,
                        "name": herb.name_fa,
                        "name_en": herb.name_en,
                        "actions": herb.actions,
                        "dosage": herb.dosage,
                        "frequency": herb.frequency,
                        "preparation": herb.preparation,
                        "thermal_nature": herb.thermal_nature,
                    }
                    for herb in herbs
                ],
                "diet": self._get_tcm_diet_recommendations(pattern),
                "lifestyle": self._get_tcm_lifestyle_recommendations(pattern),
                "treatments": [
                    {
                        "name": treatment.name_fa,
                        "name_en": treatment.name_en,
                        "method": treatment.method,
                        "frequency": treatment.frequency_per_week,
                    }
                    for treatment in treatments
                ],
                "duration_days": self.treatment_duration_days,
                "acupuncture_points": pattern.acupuncture_points,
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting TCM recommendations: {e}")
            return {"error": str(e)}

    async def get_ayurveda_recommendations(
        self,
        disease_id: int,
        db: Session
    ) -> Dict:
        """
        دریافت توصیه‌های Ayurveda برای یک بیماری
        """
        try:
            disease = db.query(AyurvedicDisease).filter(
                AyurvedicDisease.id == disease_id
            ).first()
            
            if not disease:
                return {"error": "Disease not found"}
            
            # دریافت گیاهان
            herbs = db.query(AyurvedicHerb).filter(
                AyurvedicHerb.disease_id == disease_id
            ).limit(self.max_recommendations).all()
            
            # دریافت درمان‌ها
            treatments = db.query(AyurvedicTreatment).filter(
                AyurvedicTreatment.disease_id == disease_id
            ).limit(self.max_recommendations).all()
            
            recommendations = {
                "disease_id": disease_id,
                "disease_name": disease.name_fa,
                "tradition": "ayurveda",
                "dosha_imbalance": disease.dosha,
                "balancing_doshas": disease.balancing_doshas,
                "herbs": [
                    {
                        "id": herb.id,
                        "name": herb.name_fa,
                        "name_en": herb.name_en,
                        "rasa": herb.rasa,
                        "virya": herb.virya,
                        "vipaka": herb.vipaka,
                        "dosage": herb.dosage,
                        "frequency": herb.frequency,
                        "balancing_doshas": herb.balancing_doshas,
                    }
                    for herb in herbs
                ],
                "diet": self._get_ayurveda_diet_recommendations(disease),
                "lifestyle": self._get_ayurveda_lifestyle_recommendations(disease),
                "treatments": [
                    {
                        "name": treatment.name_fa,
                        "name_en": treatment.name_en,
                        "description": treatment.description_fa,
                        "application_time": treatment.application_time,
                        "duration_days": treatment.duration_days,
                    }
                    for treatment in treatments
                ],
                "seasonal_considerations": disease.seasonal_considerations,
                "sleep_recommendations": disease.sleep_recommendation,
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting Ayurveda recommendations: {e}")
            return {"error": str(e)}

    def _get_avicenna_diet_recommendations(self, disease) -> List[str]:
        """
        دریافت توصیه‌های غذایی Avicenna
        """
        recommendations = []
        
        if disease.mizaj == "garm_tar":
            recommendations = [
                "از غذاهای گرم و حار خودداری کنید",
                "مصرف کننده میوه‌های سرد (خربزه، خیار، هندوانه)",
                "آب معدنی سرد و چای نعناع",
                "غذاهای سبک و کم‌چرب",
                "تجنب از ادویه‌های تند",
            ]
        elif disease.mizaj == "sard_tar":
            recommendations = [
                "غذاهای گرم و در درجه دوم گرم",
                "مصرف عسل و دیار",
                "ادویه‌های گرم‌مزاج",
                "اجتناب از غذاهای سرد و مرطوب",
                "خوردن نان کامل‌دانه",
            ]
        
        return recommendations

    def _get_avicenna_lifestyle_recommendations(self, disease) -> List[str]:
        """
        دریافت توصیه‌های سبک زندگی Avicenna
        """
        recommendations = [
            "ورزش منظم (30 دقیقه روزانه)",
            "خواب کافی (7-8 ساعت)",
            "جلوگیری از استرس و نگرانی",
            "تنفس عمیق و آرام",
            "قطع عادات بد",
        ]
        
        if disease.mizaj == "garm_tar":
            recommendations.append("اجتناب از حرارت شدید")
            recommendations.append("استراحت در سایه‌روزهای گرم")
        
        return recommendations

    def _get_tcm_diet_recommendations(self, pattern) -> List[str]:
        """
        دریافت توصیه‌های غذایی TCM
        """
        recommendations = [
            "غذاهای تازه و درجه یک",
            "اجتناب از غذاهای فریز شده",
            "نوشیدنی‌های گرم",
            "غذاهای روغنی را کم کنید",
        ]
        
        if "Liver" in pattern.organs:
            recommendations.append("اجتناب از الکل و چیزهای نپخته")
        
        if "Kidney" in pattern.organs:
            recommendations.append("کاهش نمک و غذاهای حار")
        
        return recommendations

    def _get_tcm_lifestyle_recommendations(self, pattern) -> List[str]:
        """
        دریافت توصیه‌های سبک زندگی TCM
        """
        return [
            "مدیتیشن روزانه (20 دقیقه)",
            "تای چی یا کونگ فو نرم",
            "تناسب بین کار و استراحت",
            "خود آگاهی احساسی",
            "ارتباط با طبیعت",
        ]

    def _get_ayurveda_diet_recommendations(self, disease) -> List[str]:
        """
        دریافت توصیه‌های غذایی Ayurveda
        """
        recommendations = [
            "غذاهای حسب Dosha شخص",
            "خوردن در اوقات منظم",
            "غذاهای تازه و طبیعی",
        ]
        
        if "Vata" in disease.dosha:
            recommendations.extend([
                "روغن های گرم (سسام، بادام)",
                "غذاهای داغ و مرطوب",
                "اجتناب از سردی و خشکی",
            ])
        elif "Pitta" in disease.dosha:
            recommendations.extend([
                "غذاهای سرد و خنک",
                "مصرف شیر و دسر",
                "اجتناب از تند و تیز",
            ])
        
        return recommendations

    def _get_ayurveda_lifestyle_recommendations(self, disease) -> List[str]:
        """
        دریافت توصیه‌های سبک زندگی Ayurveda
        """
        recommendations = [
            "روتین روزانه منظم (Dinacharya)",
            "خواب منظم (قبل از 10 شب)",
            "مدیتیشن صبحگاهی",
            "تدهیل (روغن مالش) 3 بار در هفته",
        ]
        
        if "Vata" in disease.dosha:
            recommendations.append("جنب‌ها ملایم و منظم")
        
        return recommendations


# Singleton instance
_engine = RecommendationEngine()


def get_recommendation_engine() -> RecommendationEngine:
    """دریافت نمونه انجن"""
    return _engine
