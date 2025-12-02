"""
Health Analysis Orchestration Service
سرویس هماهنگ‌کننده برای اجرای تحلیل‌های جامع سلامت
"""
from fastapi import Depends
from app.database import get_db
import base64
from pathlib import Path
from sqlalchemy.orm import Session
import logging

from app.models import health_data as models
from app.services.ai_service import AIService
from app.services.avicenna_knowledge import AvicennaKnowledgeBase

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()
        self.knowledge_base = AvicennaKnowledgeBase()

    async def analyze_health_report(self, report_id: int) -> models.HealthReport:
        """
        یک گزارش سلامت را به صورت جامع تحلیل می‌کند.
        1. داده‌های مرتبط (زبان، چشم، ...) را از دیتابیس می‌خواند.
        2. هر داده را به سرویس AI مناسب ارسال می‌کند.
        3. نتایج را تلفیق کرده و با LLM یک گزارش نهایی تولید می‌کند.
        4. گزارش را در دیتابیس آپدیت می‌کند.
        """
        health_report = self.db.query(models.HealthReport).filter(models.HealthReport.id == report_id).first()
        if not health_report:
            logger.error(f"HealthReport با شناسه {report_id} یافت نشد.")
            raise ValueError("Health report not found")

        # لیستی برای نگهداری نتایج تحلیل‌های جزئی
        analysis_results = []

        # 1. تحلیل زبان
        if health_report.tongue_analysis_id:
            tongue_record = self.db.query(models.TongueAnalysis).get(health_report.tongue_analysis_id)
            if tongue_record and Path(tongue_record.image_path).exists():
                try:
                    with open(tongue_record.image_path, "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode()
                    tongue_result = await self.ai_service.analyze_tongue(img_base64)
                    
                    # ذخیره نتایج در جدول تحلیل زبان
                    tongue_record.ai_diagnosis = tongue_result.get("avicenna_diagnosis")
                    tongue_record.detailed_analysis = tongue_result
                    self.db.commit()
                    
                    analysis_results.append(f"تحلیل زبان: {tongue_result.get('avicenna_diagnosis')}")
                except Exception as e:
                    logger.error(f"خطا در تحلیل زبان برای گزارش {report_id}: {e}")

        # 2. تحلیل چشم (مشابه زبان)
        if health_report.eye_analysis_id:
            eye_record = self.db.query(models.EyeAnalysis).get(health_report.eye_analysis_id)
            if eye_record and Path(eye_record.image_path).exists():
                try:
                    with open(eye_record.image_path, "rb") as img_file:
                        img_base64 = base64.b64encode(img_file.read()).decode()
                    eye_result = await self.ai_service.analyze_eye(img_base64)
                    
                    eye_record.ai_diagnosis = eye_result.get("avicenna_diagnosis")
                    eye_record.detailed_analysis = eye_result
                    self.db.commit()

                    analysis_results.append(f"تحلیل چشم: {eye_result.get('avicenna_diagnosis')}")
                except Exception as e:
                    logger.error(f"خطا در تحلیل چشم برای گزارش {report_id}: {e}")
        
        # 3. تحلیل علائم حیاتی
        if health_report.vital_signs_ids:
            vital_signs_record_id = health_report.vital_signs_ids[0] # فرض بر اینکه فقط یکی است
            vitals = self.db.query(models.VitalSigns).get(vital_signs_record_id)
            if vitals:
                vitals_summary = f"علائم حیاتی: ضربان قلب {vitals.heart_rate}، اکسیژن خون {vitals.spo2}%"
                analysis_results.append(vitals_summary)


        # 4. تلفیق و تولید گزارش نهایی با LLM (در اینجا شبیه‌سازی می‌شود)
        if self.ai_service.gemini_service:
            # در یک پروژه واقعی، ما این نتایج را به Gemini ارسال می‌کنیم
            # prompt = f"بر اساس تحلیل‌های زیر، یک خلاصه سلامت و توصیه‌های عملی ارائه بده:\n" + "\n".join(analysis_results)
            # final_summary = await self.ai_service.gemini_service.generate_text(prompt)
            # health_report.ai_summary = final_summary
            
            # شبیه‌سازی شده:
            health_report.ai_summary = "بر اساس تحلیل‌های انجام شده، وضعیت عمومی شما خوب به نظر می‌رسد. " + " ".join(analysis_results)
            health_report.risk_level = "low"
            health_report.should_see_doctor = False
        else:
            # حالت بدون Gemini
            health_report.ai_summary = "تحلیل اولیه انجام شد. " + " ".join(analysis_results)
            health_report.risk_level = "medium" # احتیاط بیشتر در حالت عدم دسترسی به LLM

        health_report.recommendations = {
            "lifestyle": self.knowledge_base.get_lifestyle_tips("متعادل"),
            "nutrition": self.knowledge_base.get_foods_for_mizaj("متعادل")
        }
        
        self.db.commit()
        self.db.refresh(health_report)
        
        logger.info(f"گزارش سلامت {report_id} با موفقیت تحلیل و آپدیت شد.")
        return health_report

def get_analysis_service(db: Session = Depends(get_db)):
    return AnalysisService(db)
