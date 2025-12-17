from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import auth, patients, health
from app.routers import avicenna_diagnosis, avicenna_diseases, analysis_service
from app.routers import sensor_diagnostic, knowledge_base, image_analysis, websocket, analytics, feedback, predictions
from app.core.config import settings
from app.services.health_check import (
    get_health_check_endpoint,
    get_readiness_check,
    get_liveness_check
)

# Import all models to ensure they're registered with Base
# This must be done before creating tables
from app.models import patient  # noqa: F401
from app.models import user  # noqa: F401
from app.models import health_record  # noqa: F401
from app.models import health_data  # noqa: F401
from app.models import doctor  # noqa: F401
from app.models import avicenna_diagnosis as avicenna_diag  # noqa: F401
from app.models import avicenna_diseases as avicenna_dis  # noqa: F401
from app.models import sensor_and_diagnostic_data as sensor_diag  # noqa: F401
from app.models import avicenna_knowledge_base as avicenna_kb  # noqa: F401
from app.models import tcm_knowledge_base as tcm_kb  # noqa: F401
from app.models import ayurveda_knowledge_base as ayurveda_kb  # noqa: F401

# ایجاد جداول
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Avicenna AI API",
    description="Traditional Persian Medicine AI Assistant",
    version="1.0.0"
)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اضافه کردن روت‌ها
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(health.router)
app.include_router(avicenna_diagnosis.router)
app.include_router(avicenna_diseases.router)
app.include_router(analysis_service.router)
app.include_router(sensor_diagnostic.router)
app.include_router(knowledge_base.router)
app.include_router(image_analysis.router)  # ✨ Image analysis with Gemini
app.include_router(websocket.router)  # ✨ Real-time WebSocket updates
app.include_router(analytics.router)  # ✨ Analytics and effectiveness tracking
app.include_router(feedback.router)  # ✨ User feedback collection and management
app.include_router(predictions.router)  # ✨ ML-based recommendation predictions

@app.get("/")
def root():
    return {"message": "Welcome to Avicenna AI API"}


@app.get("/health")
def health_check_simple():
    """Simple health check for load balancers"""
    return get_readiness_check()


@app.get("/health/live")
def liveness_probe():
    """Liveness probe for Kubernetes"""
    return get_liveness_check()


@app.get("/health/ready")
def readiness_probe():
    """Readiness probe for Kubernetes"""
    return get_readiness_check()


@app.get("/health/system")
def system_health_check(db: Session = Depends(get_db)):
    """Comprehensive system health check"""
    return get_health_check_endpoint(db)

