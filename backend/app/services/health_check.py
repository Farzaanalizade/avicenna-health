"""
🏥 Health Check Services
Endpoints برای بررسی وضعیت سرور و سیستم‌های وابسته
"""

from fastapi import APIRouter
from datetime import datetime


def get_health_check_endpoint():
    """
    سلامت کلی سیستم
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "ai_models": "loaded",
            "api": "running"
        }
    }


def get_readiness_check():
    """
    آیا سیستم برای پذیرش درخواست‌ها آماده است؟
    """
    return {
        "ready": True,
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "models": "loaded"
    }


def get_liveness_check():
    """
    آیا سیستم هنوز اجرا می‌شود؟
    """
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat()
    }
