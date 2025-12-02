from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class HealthStatus(str, Enum):
    """وضعیت سلامت"""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


class QuickCheckRequest(BaseModel):
    """درخواست بررسی سریع علائم حیاتی"""
    heart_rate: Optional[int] = Field(None, ge=40, le=200, description="ضربان قلب (bpm)")
    blood_pressure_systolic: Optional[int] = Field(None, ge=70, le=200, description="فشار خون سیستولیک")
    blood_pressure_diastolic: Optional[int] = Field(None, ge=40, le=130, description="فشار خون دیاستولیک")
    temperature: Optional[float] = Field(None, ge=35.0, le=42.0, description="دمای بدن (°C)")
    oxygen_saturation: Optional[int] = Field(None, ge=70, le=100, description="اشباع اکسیژن (%)")
    symptoms: Optional[List[str]] = Field(default_factory=list, description="لیست علائم")


class QuickCheckResponse(BaseModel):
    """پاسخ بررسی سریع"""
    status: HealthStatus
    message: str
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    vital_signs_summary: dict


class TongueImageUpload(BaseModel):
    """آپلود تصویر زبان"""
    image_base64: str = Field(..., description="تصویر زبان در فرمت Base64")
    notes: Optional[str] = Field(None, description="یادداشت‌های اضافی")


class TongueAnalysisResponse(BaseModel):
    """پاسخ تحلیل زبان"""
    analysis_id: int
    color_assessment: str
    coating_assessment: str
    texture_assessment: str
    health_indicators: List[str]
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime

    class Config:
        from_attributes = True


class HealthHistoryItem(BaseModel):
    """یک آیتم از تاریخچه سلامت"""
    id: int
    record_type: str
    data: dict
    analysis_result: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class HealthHistoryResponse(BaseModel):
    """پاسخ تاریخچه سلامت"""
    total_records: int
    records: List[HealthHistoryItem]
