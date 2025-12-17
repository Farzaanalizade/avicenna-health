"""
Report Generation Service
Generates comprehensive reports with data export and visualization support
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List, BinaryIO
import logging
import csv
import json
from io import StringIO, BytesIO

logger = logging.getLogger(__name__)

class ReportService:
    """Generate comprehensive reports with multiple formats"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===========================
    # Report Generation
    # ===========================
    
    def generate_patient_report(self, patient_id: int) -> Dict[str, Any]:
        """Generate comprehensive patient health report"""
        from app.models.patient_and_diagnosis_data import (
            Patient, DiagnosticFinding, Recommendation, HealthRecord
        )
        
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return {}
        
        # Get diagnoses
        diagnoses = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        ).all()
        
        # Get recommendations
        recommendations = self.db.query(Recommendation).limit(10).all()
        
        # Get feedbacks
        feedbacks = self.db.query(HealthRecord).filter(
            HealthRecord.diagnosis_id.in_([d.id for d in diagnoses])
        ).all()
        
        return {
            "patient_id": patient_id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "mizaj_type": patient.mizaj_type,
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": {
                "total_diagnoses": len(diagnoses),
                "total_recommendations": len(recommendations),
                "total_feedbacks": len(feedbacks),
                "avg_rating": sum(f.rating for f in feedbacks) / len(feedbacks) if feedbacks else 0,
            },
            "diagnoses": [
                {
                    "condition": d.condition,
                    "severity": d.severity,
                    "date": d.created_at.isoformat(),
                }
                for d in diagnoses
            ],
            "top_recommendations": [
                {
                    "herb": r.herb_name,
                    "dosage": r.dosage,
                    "effectiveness": r.effectiveness_rating,
                }
                for r in recommendations
            ],
        }
    
    def generate_recommendation_report(self, recommendation_id: int) -> Dict[str, Any]:
        """Generate recommendation effectiveness report"""
        from app.models.patient_and_diagnosis_data import Recommendation, HealthRecord
        
        rec = self.db.query(Recommendation).filter(
            Recommendation.id == recommendation_id
        ).first()
        
        if not rec:
            return {}
        
        feedbacks = self.db.query(HealthRecord).filter(
            HealthRecord.recommendation_id == recommendation_id
        ).all()
        
        ratings = [f.rating for f in feedbacks]
        improvements = [f.symptom_improvement for f in feedbacks]
        
        return {
            "recommendation_id": recommendation_id,
            "herb_name": rec.herb_name,
            "dosage": rec.dosage,
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": {
                "total_users": len(feedbacks),
                "average_rating": sum(ratings) / len(ratings) if ratings else 0,
                "average_improvement": sum(improvements) / len(improvements) if improvements else 0,
                "effectiveness_rate": len([r for r in ratings if r >= 3]) / len(ratings) if ratings else 0,
                "success_rate": f"{(len([r for r in ratings if r >= 3]) / len(ratings) * 100) if ratings else 0:.1f}%",
            },
            "ratings_distribution": {
                "5_stars": len([r for r in ratings if r == 5]),
                "4_stars": len([r for r in ratings if r == 4]),
                "3_stars": len([r for r in ratings if r == 3]),
                "2_stars": len([r for r in ratings if r == 2]),
                "1_stars": len([r for r in ratings if r == 1]),
            },
        }
    
    # ===========================
    # Export to CSV
    # ===========================
    
    def export_patient_data_csv(self, patient_id: int) -> str:
        """Export patient data to CSV format"""
        from app.models.patient_and_diagnosis_data import (
            Patient, DiagnosticFinding, HealthRecord
        )
        
        buffer = StringIO()
        writer = csv.writer(buffer)
        
        # Patient info
        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()
        
        writer.writerow(["Patient Health Report"])
        writer.writerow(["Name", patient.name if patient else ""])
        writer.writerow(["Age", patient.age if patient else ""])
        writer.writerow(["Gender", patient.gender if patient else ""])
        writer.writerow([""])
        
        # Diagnosis history
        writer.writerow(["Diagnosis History"])
        writer.writerow(["Date", "Condition", "Severity", "Duration (days)"])
        
        diagnoses = self.db.query(DiagnosticFinding).filter(
            DiagnosticFinding.patient_id == patient_id
        ).all()
        
        for diagnosis in diagnoses:
            writer.writerow([
                diagnosis.created_at.date(),
                diagnosis.condition,
                diagnosis.severity,
                diagnosis.duration_days,
            ])
        
        return buffer.getvalue()
    
    def export_recommendations_csv(self) -> str:
        """Export all recommendations to CSV"""
        from app.models.patient_and_diagnosis_data import Recommendation, HealthRecord
        from sqlalchemy import func
        
        buffer = StringIO()
        writer = csv.writer(buffer)
        
        writer.writerow(["Herb Name", "Dosage", "Effectiveness", "Total Uses", "Avg Rating"])
        
        recommendations = self.db.query(
            Recommendation.herb_name,
            Recommendation.dosage,
            Recommendation.effectiveness_rating,
            func.count(HealthRecord.id).label("usage_count"),
            func.avg(HealthRecord.rating).label("avg_rating"),
        ).outerjoin(HealthRecord).group_by(
            Recommendation.herb_name,
            Recommendation.dosage,
            Recommendation.effectiveness_rating,
        ).all()
        
        for rec in recommendations:
            writer.writerow([
                rec.herb_name,
                rec.dosage,
                f"{rec.effectiveness_rating:.2f}",
                rec.usage_count or 0,
                f"{rec.avg_rating:.2f}" if rec.avg_rating else "N/A",
            ])
        
        return buffer.getvalue()
    
    # ===========================
    # Export to JSON
    # ===========================
    
    def export_report_json(self, report_data: Dict[str, Any]) -> str:
        """Export report data to JSON format"""
        return json.dumps(report_data, indent=2, default=str)
    
    # ===========================
    # PDF Export (using reportlab)
    # ===========================
    
    def export_report_pdf(self, report_data: Dict[str, Any]) -> bytes:
        """Export report to PDF format"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph("Avicenna Health Report", styles['Heading1'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            # Report info
            info_text = Paragraph(
                f"Generated: {report_data.get('generated_at', datetime.utcnow().isoformat())}",
                styles['Normal']
            )
            elements.append(info_text)
            elements.append(Spacer(1, 12))
            
            # Statistics table
            stats = report_data.get('statistics', {})
            table_data = [["Metric", "Value"]]
            for key, value in stats.items():
                table_data.append([str(key).replace('_', ' ').title(), str(value)])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            
            doc.build(elements)
            return buffer.getvalue()
        
        except ImportError:
            logger.warning("reportlab not installed for PDF export")
            return b"PDF export not available"
    
    # ===========================
    # Scheduled Reports
    # ===========================
    
    def schedule_report(
        self,
        user_id: int,
        report_type: str,
        frequency: str,
        email: str
    ) -> int:
        """Schedule automatic report generation"""
        from app.models.admin_models import ScheduledReport
        
        report = ScheduledReport(
            user_id=user_id,
            report_type=report_type,
            frequency=frequency,  # daily, weekly, monthly
            email=email,
            created_at=datetime.utcnow(),
        )
        self.db.add(report)
        self.db.commit()
        logger.info(f"Scheduled {frequency} {report_type} report for user {user_id}")
        return report.id
    
    def get_scheduled_reports(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's scheduled reports"""
        from app.models.admin_models import ScheduledReport
        
        reports = self.db.query(ScheduledReport).filter(
            ScheduledReport.user_id == user_id
        ).all()
        
        return [
            {
                "id": r.id,
                "report_type": r.report_type,
                "frequency": r.frequency,
                "email": r.email,
                "created_at": r.created_at.isoformat(),
            }
            for r in reports
        ]


def get_report_service(db: Session) -> ReportService:
    """Get report service instance"""
    return ReportService(db)
