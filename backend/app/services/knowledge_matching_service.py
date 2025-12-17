"""
Knowledge Base Matching Service

این سرویس نتایج تحلیل Gemini را با دانایی‌های پزشکی سنتی (Avicenna, TCM, Ayurveda) 
تطابق می‌دهد و بهترین تطابق‌ها را برمی‌گرداند.

Services:
- match_avicenna_diseases()     → بیماری‌های اویسنایی
- match_tcm_patterns()          → الگوهای TCM
- match_ayurveda_diseases()     → بیماری‌های آیورودا
- get_all_matches()             → تمام تطابق‌ها
- calculate_match_score()       → محاسبه امتیاز تطابق
"""

import logging
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.knowledge_base_models import (
    AvicennaDisease,
    AvicennaHerb,
    TCMPatternDisharmony,
    TCMHerb,
    AyurvedicDisease,
    AyurvedicHerb,
)
from app.models.sensor_and_diagnostic_data import DiagnosticFinding

logger = logging.getLogger(__name__)


class KnowledgeMatchingService:
    """
    سرویس تطابق دانایی‌های پزشکی سنتی با نتایج تحلیل تصویر
    """

    def __init__(self):
        """Initialize the service"""
        self.avicenna_threshold = 0.5  # حداقل امتیاز برای Avicenna
        self.tcm_threshold = 0.5  # حداقل امتیاز برای TCM
        self.ayurveda_threshold = 0.5  # حداقل امتیاز برای Ayurveda

    async def match_avicenna_diseases(
        self,
        findings: Dict,
        confidence: float,
        db: Session
    ) -> List[Dict]:
        """
        بیماری‌های Avicenna را تطابق دهید
        
        Args:
            findings: نتایج تحلیل Gemini (مثال: {color: "red", coating: "thick"})
            confidence: اعتماد نتیجه Gemini (0-1)
            db: جلسه پایگاه داده
            
        Returns:
            [{disease_name, confidence, supporting_findings, recommendations}, ...]
        """
        try:
            # دریافت تمام بیماری‌های Avicenna
            diseases = db.query(AvicennaDisease).all()
            
            matches = []
            
            for disease in diseases:
                score = self._calculate_avicenna_score(findings, disease)
                
                if score >= self.avicenna_threshold:
                    # دریافت گیاهان مرتبط
                    herbs = db.query(AvicennaHerb).filter(
                        AvicennaHerb.disease_id == disease.id
                    ).limit(3).all()
                    
                    match = {
                        "disease_id": disease.id,
                        "disease_name": disease.name_fa,
                        "disease_name_en": disease.name_en,
                        "mizaj": disease.mizaj,
                        "confidence": round(score * confidence, 2),
                        "supporting_findings": self._get_supporting_findings(findings, disease),
                        "description": disease.description_fa,
                        "recommended_herbs": [
                            {
                                "name": herb.name_fa,
                                "name_en": herb.name_en,
                                "dosage": herb.dosage,
                                "frequency": herb.frequency,
                            }
                            for herb in herbs
                        ],
                        "severity": self._assess_severity(score),
                    }
                    matches.append(match)
            
            # مرتب‌سازی بر اساس امتیاز (بالاترین اول)
            matches.sort(key=lambda x: x["confidence"], reverse=True)
            
            # برگرداندن 5 بهترین تطابق
            return matches[:5]
            
        except Exception as e:
            logger.error(f"Error matching Avicenna diseases: {e}")
            return []

    async def match_tcm_patterns(
        self,
        findings: Dict,
        confidence: float,
        db: Session
    ) -> List[Dict]:
        """
        الگوهای TCM را تطابق دهید
        
        Args:
            findings: نتایج تحلیل
            confidence: اعتماد نتیجه
            db: جلسه پایگاه داده
            
        Returns:
            [{pattern_name, confidence, supporting_findings, recommendations}, ...]
        """
        try:
            # دریافت تمام الگوهای TCM
            patterns = db.query(TCMPatternDisharmony).all()
            
            matches = []
            
            for pattern in patterns:
                score = self._calculate_tcm_score(findings, pattern)
                
                if score >= self.tcm_threshold:
                    # دریافت گیاهان مرتبط
                    herbs = db.query(TCMHerb).filter(
                        TCMHerb.pattern_id == pattern.id
                    ).limit(3).all()
                    
                    match = {
                        "pattern_id": pattern.id,
                        "pattern_name": pattern.name_fa,
                        "pattern_name_en": pattern.name_en,
                        "organs": pattern.organs,
                        "imbalance_type": pattern.imbalance_type,
                        "confidence": round(score * confidence, 2),
                        "supporting_findings": self._get_supporting_findings(findings, pattern),
                        "description": pattern.description_fa,
                        "recommended_herbs": [
                            {
                                "name": herb.name_fa,
                                "name_en": herb.name_en,
                                "actions": herb.actions,
                                "dosage": herb.dosage,
                            }
                            for herb in herbs
                        ],
                        "balancing_method": pattern.balancing_method,
                    }
                    matches.append(match)
            
            # مرتب‌سازی بر اساس امتیاز
            matches.sort(key=lambda x: x["confidence"], reverse=True)
            
            return matches[:5]
            
        except Exception as e:
            logger.error(f"Error matching TCM patterns: {e}")
            return []

    async def match_ayurveda_diseases(
        self,
        findings: Dict,
        confidence: float,
        db: Session
    ) -> List[Dict]:
        """
        بیماری‌های Ayurveda را تطابق دهید
        
        Args:
            findings: نتایج تحلیل
            confidence: اعتماد نتیجه
            db: جلسه پایگاه داده
            
        Returns:
            [{disease_name, dosha, confidence, recommendations}, ...]
        """
        try:
            # دریافت تمام بیماری‌های Ayurveda
            diseases = db.query(AyurvedicDisease).all()
            
            matches = []
            
            for disease in diseases:
                score = self._calculate_ayurveda_score(findings, disease)
                
                if score >= self.ayurveda_threshold:
                    # دریافت گیاهان مرتبط
                    herbs = db.query(AyurvedicHerb).filter(
                        AyurvedicHerb.disease_id == disease.id
                    ).limit(3).all()
                    
                    match = {
                        "disease_id": disease.id,
                        "disease_name": disease.name_fa,
                        "disease_name_en": disease.name_en,
                        "dosha": disease.dosha,
                        "confidence": round(score * confidence, 2),
                        "supporting_findings": self._get_supporting_findings(findings, disease),
                        "description": disease.description_fa,
                        "recommended_herbs": [
                            {
                                "name": herb.name_fa,
                                "name_en": herb.name_en,
                                "rasa": herb.rasa,
                                "virya": herb.virya,
                                "dosage": herb.dosage,
                            }
                            for herb in herbs
                        ],
                        "balancing_doshas": disease.balancing_doshas,
                    }
                    matches.append(match)
            
            # مرتب‌سازی بر اساس امتیاز
            matches.sort(key=lambda x: x["confidence"], reverse=True)
            
            return matches[:5]
            
        except Exception as e:
            logger.error(f"Error matching Ayurveda diseases: {e}")
            return []

    async def get_all_matches(
        self,
        diagnosis_id: int,
        db: Session
    ) -> Dict:
        """
        دریافت تمام تطابق‌ها برای یک تشخیص
        
        Args:
            diagnosis_id: شناسه DiagnosticFinding
            db: جلسه پایگاه داده
            
        Returns:
            {
                avicenna_matches: [...],
                tcm_matches: [...],
                ayurveda_matches: [...]
            }
        """
        try:
            # دریافت نتایج تشخیص
            diagnosis = db.query(DiagnosticFinding).filter(
                DiagnosticFinding.id == diagnosis_id
            ).first()
            
            if not diagnosis:
                logger.warning(f"Diagnosis {diagnosis_id} not found")
                return {
                    "avicenna_matches": [],
                    "tcm_matches": [],
                    "ayurveda_matches": [],
                    "error": "Diagnosis not found"
                }
            
            findings = diagnosis.findings
            confidence = diagnosis.confidence
            
            # دریافت تطابق‌های تمام سنت‌ها
            avicenna = await self.match_avicenna_diseases(findings, confidence, db)
            tcm = await self.match_tcm_patterns(findings, confidence, db)
            ayurveda = await self.match_ayurveda_diseases(findings, confidence, db)
            
            return {
                "diagnosis_id": diagnosis_id,
                "analysis_type": diagnosis.analysis_type,
                "original_findings": findings,
                "original_confidence": confidence,
                "avicenna_matches": avicenna,
                "tcm_matches": tcm,
                "ayurveda_matches": ayurveda,
                "total_matches": len(avicenna) + len(tcm) + len(ayurveda),
            }
            
        except Exception as e:
            logger.error(f"Error getting all matches: {e}")
            return {
                "error": str(e),
                "avicenna_matches": [],
                "tcm_matches": [],
                "ayurveda_matches": [],
            }

    def _calculate_avicenna_score(self, findings: Dict, disease) -> float:
        """
        محاسبه امتیاز تطابق برای بیماری Avicenna
        
        Score = (matching_attributes / total_attributes) * 0.85 + bonus
        """
        try:
            score = 0.0
            disease_characteristics = disease.characteristics or {}
            
            # بررسی Mizaj
            if findings.get("mizaj") == disease.mizaj:
                score += 0.3
            
            # بررسی رنگ زبان
            if findings.get("color") and disease_characteristics.get("color"):
                if findings["color"].lower() in str(disease_characteristics.get("color", "")).lower():
                    score += 0.2
            
            # بررسی پوشش زبان
            if findings.get("coating") and disease_characteristics.get("coating"):
                if findings["coating"].lower() in str(disease_characteristics.get("coating", "")).lower():
                    score += 0.2
            
            # بررسی سایر مشخصات
            if findings.get("moisture") and disease_characteristics.get("moisture"):
                if findings["moisture"].lower() in str(disease_characteristics.get("moisture", "")).lower():
                    score += 0.15
            
            # عادی‌سازی امتیاز (0-1)
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating Avicenna score: {e}")
            return 0.0

    def _calculate_tcm_score(self, findings: Dict, pattern) -> float:
        """محاسبه امتیاز برای الگوی TCM"""
        try:
            score = 0.0
            
            # بررسی رنگ
            if findings.get("color") and pattern.tongue_appearance:
                if findings["color"].lower() in str(pattern.tongue_appearance).lower():
                    score += 0.3
            
            # بررسی پوشش
            if findings.get("coating") and pattern.coating:
                if findings["coating"].lower() in str(pattern.coating).lower():
                    score += 0.3
            
            # بررسی رطوبت
            if findings.get("moisture") and pattern.moisture:
                if findings["moisture"].lower() in str(pattern.moisture).lower():
                    score += 0.2
            
            # بررسی شکل
            if findings.get("shape") and pattern.shape:
                if findings["shape"].lower() in str(pattern.shape).lower():
                    score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating TCM score: {e}")
            return 0.0

    def _calculate_ayurveda_score(self, findings: Dict, disease) -> float:
        """محاسبه امتیاز برای بیماری Ayurveda"""
        try:
            score = 0.0
            
            # بررسی Dosha
            if findings.get("dosha") and disease.dosha:
                if findings.get("dosha") in str(disease.dosha).lower():
                    score += 0.3
            
            # بررسی رنگ
            if findings.get("color") and disease.tongue_signs:
                if findings["color"].lower() in str(disease.tongue_signs).lower():
                    score += 0.25
            
            # بررسی سایر علائم
            if findings.get("coating") and disease.tongue_signs:
                if findings["coating"].lower() in str(disease.tongue_signs).lower():
                    score += 0.25
            
            # بررسی شرایط پوسی‌دگی
            if findings.get("moisture") and disease.digestion_status:
                if "normal" in str(disease.digestion_status).lower():
                    score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating Ayurveda score: {e}")
            return 0.0

    def _get_supporting_findings(self, findings: Dict, disease) -> List[str]:
        """
        دریافت نتایج حمایت‌کننده برای تطابق
        """
        supporting = []
        
        for key, value in findings.items():
            if value and value != "none" and value != "normal":
                supporting.append(f"{key}: {value}")
        
        return supporting[:5]  # برگرداندن 5 اول

    def _assess_severity(self, score: float) -> str:
        """
        ارزیابی شدت بر اساس امتیاز
        """
        if score >= 0.8:
            return "high"
        elif score >= 0.6:
            return "moderate"
        else:
            return "low"


# Singleton instance
_service = KnowledgeMatchingService()


def get_matching_service() -> KnowledgeMatchingService:
    """دریافت نمونه سرویس"""
    return _service
