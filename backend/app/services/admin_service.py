"""
Admin Dashboard Service
Provides analytics, user management, and reporting functionality
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AdminService:
    """Advanced admin analytics and management service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ===========================
    # User Analytics
    # ===========================
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        from app.models.patient_and_diagnosis_data import Patient
        
        total_users = self.db.query(func.count(Patient.id)).scalar() or 0
        active_users_7d = self.db.query(func.count(Patient.id)).filter(
            Patient.updated_at >= datetime.utcnow() - timedelta(days=7)
        ).scalar() or 0
        
        gender_dist = self.db.query(
            Patient.gender,
            func.count(Patient.id).label("count")
        ).group_by(Patient.gender).all()
        
        return {
            "total_users": total_users,
            "active_7d": active_users_7d,
            "active_rate": (active_users_7d / total_users * 100) if total_users > 0 else 0,
            "gender_distribution": {g: c for g, c in gender_dist},
        }
    
    def get_user_growth(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get user growth over time"""
        from app.models.patient_and_diagnosis_data import Patient
        
        growth_data = self.db.query(
            func.date(Patient.created_at).label("date"),
            func.count(Patient.id).label("count")
        ).filter(
            Patient.created_at >= datetime.utcnow() - timedelta(days=days)
        ).group_by(
            func.date(Patient.created_at)
        ).all()
        
        return [{"date": str(d.date), "count": d.count} for d in growth_data]
    
    # ===========================
    # Recommendation Analytics
    # ===========================
    
    def get_recommendation_statistics(self) -> Dict[str, Any]:
        """Get recommendation performance statistics"""
        from app.models.patient_and_diagnosis_data import Recommendation, HealthRecord
        
        total_recs = self.db.query(func.count(Recommendation.id)).scalar() or 0
        total_feedbacks = self.db.query(func.count(HealthRecord.id)).scalar() or 0
        
        avg_effectiveness = self.db.query(
            func.avg(Recommendation.effectiveness_rating)
        ).scalar() or 0.0
        
        top_herbs = self.db.query(
            Recommendation.herb_name,
            func.count(HealthRecord.id).label("usage"),
            func.avg(HealthRecord.rating).label("avg_rating")
        ).outerjoin(HealthRecord).group_by(
            Recommendation.herb_name
        ).order_by(desc("usage")).limit(10).all()
        
        return {
            "total_recommendations": total_recs,
            "total_feedbacks": total_feedbacks,
            "average_effectiveness": float(avg_effectiveness),
            "top_herbs": [
                {
                    "name": h.herb_name,
                    "usage": h.usage,
                    "avg_rating": float(h.avg_rating) if h.avg_rating else 0.0
                }
                for h in top_herbs
            ],
        }
    
    def get_effectiveness_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get effectiveness trend over time"""
        from app.models.patient_and_diagnosis_data import HealthRecord
        
        trend_data = self.db.query(
            func.date(HealthRecord.created_at).label("date"),
            func.avg(HealthRecord.rating).label("avg_rating"),
            func.count(HealthRecord.id).label("count")
        ).filter(
            HealthRecord.created_at >= datetime.utcnow() - timedelta(days=days)
        ).group_by(
            func.date(HealthRecord.created_at)
        ).all()
        
        return [
            {
                "date": str(d.date),
                "avg_rating": float(d.avg_rating) if d.avg_rating else 0.0,
                "feedback_count": d.count
            }
            for d in trend_data
        ]
    
    # ===========================
    # System Health
    # ===========================
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        from app.models.patient_and_diagnosis_data import (
            Patient, DiagnosticFinding, Recommendation, HealthRecord
        )
        
        try:
            patients = self.db.query(func.count(Patient.id)).scalar() or 0
            diagnoses = self.db.query(func.count(DiagnosticFinding.id)).scalar() or 0
            recommendations = self.db.query(func.count(Recommendation.id)).scalar() or 0
            feedbacks = self.db.query(func.count(HealthRecord.id)).scalar() or 0
            
            # Database connection test
            db_healthy = True
            try:
                self.db.execute("SELECT 1")
            except:
                db_healthy = False
            
            return {
                "database": "healthy" if db_healthy else "unhealthy",
                "records": {
                    "patients": patients,
                    "diagnoses": diagnoses,
                    "recommendations": recommendations,
                    "feedbacks": feedbacks,
                },
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {
                "database": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    # ===========================
    # Reports
    # ===========================
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate comprehensive summary report"""
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "user_stats": self.get_user_statistics(),
            "recommendation_stats": self.get_recommendation_statistics(),
            "system_health": self.get_system_health(),
        }
    
    def export_csv_data(self, data_type: str) -> str:
        """Export data to CSV format"""
        import csv
        from io import StringIO
        
        buffer = StringIO()
        writer = csv.writer(buffer)
        
        if data_type == "users":
            from app.models.patient_and_diagnosis_data import Patient
            
            writer.writerow(["ID", "Name", "Email", "Age", "Gender", "Mizaj", "Created"])
            users = self.db.query(Patient).all()
            for u in users:
                writer.writerow([
                    u.id, u.name, u.email, u.age, u.gender, u.mizaj_type, u.created_at
                ])
        
        elif data_type == "recommendations":
            from app.models.patient_and_diagnosis_data import Recommendation
            
            writer.writerow(["ID", "Herb", "Dosage", "Effectiveness", "Created"])
            recs = self.db.query(Recommendation).all()
            for r in recs:
                writer.writerow([
                    r.id, r.herb_name, r.dosage, r.effectiveness_rating, r.created_at
                ])
        
        return buffer.getvalue()
    
    def export_pdf_report(self, report_type: str) -> bytes:
        """Export report to PDF format"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from io import BytesIO
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(f"Avicenna Health Report - {report_type}", styles['Heading1'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            if report_type == "summary":
                report_data = self.generate_summary_report()
                
                # User stats table
                user_data = report_data['user_stats']
                table_data = [
                    ["Metric", "Value"],
                    ["Total Users", str(user_data['total_users'])],
                    ["Active (7d)", str(user_data['active_7d'])],
                    ["Active Rate", f"{user_data['active_rate']:.1f}%"],
                ]
                
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
    # Audit Log
    # ===========================
    
    def log_admin_action(self, action: str, user_id: int, details: str = ""):
        """Log admin actions for audit trail"""
        from app.models.admin_models import AuditLog
        
        audit_entry = AuditLog(
            action=action,
            user_id=user_id,
            details=details,
            timestamp=datetime.utcnow(),
        )
        self.db.add(audit_entry)
        self.db.commit()
        logger.info(f"Admin action logged: {action} by user {user_id}")
    
    def get_audit_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent audit log entries"""
        from app.models.admin_models import AuditLog
        
        entries = self.db.query(AuditLog).order_by(
            desc(AuditLog.timestamp)
        ).limit(limit).all()
        
        return [
            {
                "id": e.id,
                "action": e.action,
                "user_id": e.user_id,
                "details": e.details,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in entries
        ]


def get_admin_service(db: Session) -> AdminService:
    """Get admin service instance"""
    return AdminService(db)
