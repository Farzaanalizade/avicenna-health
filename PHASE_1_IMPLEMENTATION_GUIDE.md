# 🚀 Phase 1 Implementation Guide
## Backend Enhancement & AI Integration

**Duration**: 2-3 weeks  
**Priority**: CRITICAL - Foundation for entire system  
**Target**: Complete API endpoints + AI pipeline ready

---

## 📋 Checklist

### Week 1: Database & Data Models

#### Step 1.1: Create New Database Tables
- [ ] Create migration files
- [ ] Add SensorData table
- [ ] Add ImageAnalysis table
- [ ] Add ToothCoating & TongueFeatures
- [ ] Add WearableDevice registration
- [ ] Add VitalSignsTimeSeries
- [ ] Add AudioAnalysis table
- [ ] Add MovementAnalysis (gyroscope)
- [ ] Add DiagnosisReport table

#### Step 1.2: Update SQLAlchemy Models
- [ ] Create `/backend/app/models/sensor_data.py`
- [ ] Create `/backend/app/models/image_analysis.py`
- [ ] Create `/backend/app/models/wearable_device.py`
- [ ] Create `/backend/app/models/vital_signs.py`
- [ ] Create `/backend/app/models/audio_analysis.py`
- [ ] Update Patient model with new relationships
- [ ] Create migration script

#### Step 1.3: Create Enums & Constants
- [ ] Create `/backend/app/models/enums.py` updates:
  - ImageType (TONGUE, EYE, SKIN, FACE)
  - SensorType (GYROSCOPE, ACCELEROMETER, etc.)
  - AudioType (HEARTBEAT, BREATHING)
  - AnalysisStatus (PENDING, PROCESSING, COMPLETE, ERROR)

### Week 1: Database & Schemas

#### Step 1.4: Create Pydantic Schemas
- [ ] Create `/backend/app/schemas/sensor_schemas.py`
- [ ] Create `/backend/app/schemas/image_schemas.py`
- [ ] Create `/backend/app/schemas/vital_signs_schemas.py`
- [ ] Create `/backend/app/schemas/wearable_schemas.py`
- [ ] Create `/backend/app/schemas/diagnosis_schemas.py`

**Files to Create**:

```python
# backend/app/models/sensor_data.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sensor_type = Column(String(50), nullable=False)  # GYRO, ACCEL, TEMP, etc
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    raw_value = Column(JSON, nullable=False)  # Raw sensor reading
    processed_value = Column(JSON, nullable=True)  # Processed/filtered
    unit = Column(String(20))  # m/s², °C, bpm, etc
    
    device_info = Column(JSON, nullable=True)  # Device metadata
    confidence_score = Column(Float, default=0.0)
    
    # Relationships
    patient = relationship("Patient", back_populates="sensor_readings")
```

```python
# backend/app/models/image_analysis.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum as SQLEnum

class ImageType(SQLEnum):
    TONGUE = "tongue"
    EYE = "eye"
    SKIN = "skin"
    FACE = "face"

class ImageAnalysis(Base):
    __tablename__ = "image_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    image_type = Column(Enum(ImageType), nullable=False)
    
    image_url = Column(String(500), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # AI Analysis Results
    ai_provider = Column(String(50))  # claude, openai, tensorflow, etc
    ai_analysis = Column(JSON, nullable=True)
    confidence_scores = Column(JSON, nullable=True)
    detected_features = Column(JSON, nullable=True)
    
    # Avicenna Analysis
    avicenna_assessment = Column(JSON, nullable=True)
    mizaj_indication = Column(String(50), nullable=True)
    
    # Status
    analysis_status = Column(String(20), default="PENDING")
    error_message = Column(String(500), nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="image_analyses")
```

### Week 2: API Endpoints

#### Step 2.1: Sensor Data Endpoints
- [ ] Create `/backend/app/routers/sensors.py`
- [ ] Implement POST `/api/v1/sensor-data/upload`
- [ ] Implement GET `/api/v1/sensor-data/{patient_id}`
- [ ] Implement POST `/api/v1/sensor-data/validate`
- [ ] Add batch processing
- [ ] Add data filtering & aggregation

#### Step 2.2: Image Analysis Endpoints
- [ ] Create `/backend/app/routers/image_analysis.py`
- [ ] Implement POST `/api/v1/analysis/tongue`
- [ ] Implement POST `/api/v1/analysis/eye`
- [ ] Implement POST `/api/v1/analysis/skin`
- [ ] Implement POST `/api/v1/analysis/face`
- [ ] Implement GET `/api/v1/analysis/history/{type}`
- [ ] Add image validation
- [ ] Add async processing queue

#### Step 2.3: Wearable Integration Endpoints
- [ ] Create `/backend/app/routers/wearables.py`
- [ ] Implement POST `/api/v1/wearable/register`
- [ ] Implement POST `/api/v1/wearable/authorize`
- [ ] Implement GET `/api/v1/wearable/sync-status`
- [ ] Implement POST `/api/v1/wearable/manual-sync`
- [ ] Implement DELETE `/api/v1/wearable/disconnect`

#### Step 2.4: Vital Signs Endpoints
- [ ] Create `/backend/app/routers/vital_signs.py`
- [ ] Implement POST `/api/v1/vital-signs/record`
- [ ] Implement GET `/api/v1/vital-signs/latest`
- [ ] Implement GET `/api/v1/vital-signs/trends`
- [ ] Implement GET `/api/v1/vital-signs/anomalies`

#### Step 2.5: Audio Analysis Endpoints
- [ ] Create `/backend/app/routers/audio_analysis.py`
- [ ] Implement POST `/api/v1/audio/heartbeat`
- [ ] Implement POST `/api/v1/audio/breathing`
- [ ] Implement GET `/api/v1/audio/analysis/{id}`

**Sample API Implementation**:

```python
# backend/app/routers/sensors.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sensor_data import SensorData
from app.schemas.sensor_schemas import SensorDataCreate, SensorDataResponse
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/sensor-data", tags=["sensors"])

@router.post("/upload", response_model=list[SensorDataResponse])
async def upload_sensor_data(
    patient_id: int,
    sensor_readings: list[SensorDataCreate],
    db: Session = Depends(get_db)
):
    """Batch upload sensor readings"""
    try:
        saved_readings = []
        for reading in sensor_readings:
            db_reading = SensorData(
                patient_id=patient_id,
                sensor_type=reading.sensor_type,
                raw_value=reading.raw_value,
                unit=reading.unit,
                device_info=reading.device_info,
                timestamp=reading.timestamp or datetime.utcnow()
            )
            db.add(db_reading)
            saved_readings.append(db_reading)
        
        db.commit()
        return [SensorDataResponse.from_orm(r) for r in saved_readings]
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{patient_id}")
async def get_sensor_data(
    patient_id: int,
    sensor_type: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Retrieve sensor data for patient"""
    query = db.query(SensorData).filter(SensorData.patient_id == patient_id)
    
    if sensor_type:
        query = query.filter(SensorData.sensor_type == sensor_type)
    
    # Last N hours
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    query = query.filter(SensorData.timestamp >= cutoff_time)
    
    readings = query.order_by(SensorData.timestamp.desc()).all()
    return [SensorDataResponse.from_orm(r) for r in readings]
```

### Week 2-3: AI Integration

#### Step 3.1: AI Service Setup
- [ ] Create `/backend/app/services/ai_providers/claude_vision.py`
- [ ] Create `/backend/app/services/ai_providers/openai_vision.py`
- [ ] Create `/backend/app/services/ai_providers/tensorflow_models.py`
- [ ] Create `/backend/app/services/ai_factory.py`
- [ ] Set up API keys & credentials
- [ ] Implement error handling & fallbacks

#### Step 3.2: Image Analysis Service
- [ ] Create `/backend/app/services/image_analysis_service.py`
- [ ] Implement `analyze_tongue_image()`
- [ ] Implement `analyze_eye_image()`
- [ ] Implement `analyze_skin_image()`
- [ ] Implement `analyze_face_image()`
- [ ] Add Avicenna interpretation
- [ ] Add confidence scoring

#### Step 3.3: Audio Analysis Service
- [ ] Create `/backend/app/services/audio_analysis_service.py`
- [ ] Implement `analyze_heart_sounds()`
- [ ] Implement `analyze_breathing_sounds()`
- [ ] Add frequency analysis
- [ ] Add abnormality detection

#### Step 3.4: Avicenna Diagnosis Engine
- [ ] Create `/backend/app/services/avicenna_engine.py`
- [ ] Implement `calculate_mizaj()`
- [ ] Implement `match_disease_patterns()`
- [ ] Implement `generate_diagnosis()`
- [ ] Build disease knowledge base
- [ ] Create symptom-disease mapping

**Sample AI Service**:

```python
# backend/app/services/ai_factory.py
from typing import Optional
import os
from anthropic import Anthropic

class AIProviderFactory:
    def __init__(self):
        self.claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai_client = None  # Initialize if needed
        self.models = {}
    
    async def analyze_tongue_image(self, image_path: str) -> dict:
        """Analyze tongue using Claude Vision"""
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            prompt = """
            Analyze this tongue image according to traditional Persian medicine principles:
            
            1. Color Assessment (by Avicenna):
            - Pink/Red (HOT)
            - Pale (COLD)
            - Yellow (EXCESS BILE)
            - White (EXCESS PHLEGM)
            
            2. Coating Analysis:
            - Presence, thickness, color
            - Normal, white, yellow, or brown
            
            3. Moisture Level:
            - Dry / Normal / Wet
            
            4. Surface Texture:
            - Smooth / Rough / Cracked
            
            5. Avicenna's Diagnosis:
            - Dominant humor (mizaj)
            - Imbalance type
            - Severity level
            
            6. Modern Correlation:
            - Likely medical conditions
            - Recommended tests
            
            Provide structured JSON response with all findings.
            """
            
            response = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data.hex(),
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            return {
                "status": "success",
                "analysis": response.content[0].text,
                "confidence_score": 0.95  # Claude's average
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
```

#### Step 3.5: Diagnosis Generation Endpoint
- [ ] Create `/backend/app/routers/diagnosis.py`
- [ ] Implement POST `/api/v1/diagnosis/generate`
- [ ] Implement GET `/api/v1/diagnosis/report/{id}`
- [ ] Implement POST `/api/v1/diagnosis/recommendations`
- [ ] Add report storage
- [ ] Add historical comparison

### Week 3: Testing & Optimization

#### Step 4.1: Unit Tests
- [ ] Test database models
- [ ] Test API endpoints
- [ ] Test AI services
- [ ] Test Avicenna engine

#### Step 4.2: Integration Tests
- [ ] Test full image analysis workflow
- [ ] Test sensor data pipeline
- [ ] Test diagnosis generation
- [ ] Test error handling

#### Step 4.3: Performance
- [ ] Optimize database queries
- [ ] Add caching (Redis)
- [ ] Optimize AI processing
- [ ] Load testing

---

## 📝 Code Templates

### Database Migration Template

```python
# backend/app/database/migrations/001_initial_schema.py
"""Create initial tables for health data collection"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'sensor_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('sensor_type', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('raw_value', sa.JSON(), nullable=False),
        sa.Column('processed_value', sa.JSON(), nullable=True),
        sa.Column('unit', sa.String(20), nullable=True),
        sa.Column('device_info', sa.JSON(), nullable=True),
        sa.Column('confidence_score', sa.Float(), default=0.0),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id']),
        sa.Index('idx_patient_sensor', 'patient_id', 'sensor_type')
    )

def downgrade():
    op.drop_table('sensor_data')
```

### Service Factory Template

```python
# backend/app/services/analysis_factory.py
from abc import ABC, abstractmethod
from typing import Optional

class ImageAnalyzer(ABC):
    @abstractmethod
    async def analyze(self, image_path: str) -> dict:
        pass

class ClaudeImageAnalyzer(ImageAnalyzer):
    async def analyze(self, image_path: str) -> dict:
        # Implementation
        pass

class TensorFlowImageAnalyzer(ImageAnalyzer):
    async def analyze(self, image_path: str) -> dict:
        # Implementation
        pass

class AnalyzerFactory:
    _analyzers = {
        'claude': ClaudeImageAnalyzer,
        'tensorflow': TensorFlowImageAnalyzer,
    }
    
    @staticmethod
    async def get_analyzer(provider: str) -> ImageAnalyzer:
        analyzer_class = AnalyzerFactory._analyzers.get(provider)
        if not analyzer_class:
            raise ValueError(f"Unknown analyzer: {provider}")
        return analyzer_class()
```

---

## 🔄 Processing Pipeline

### Data Flow Diagram

```
Mobile App
    ↓
Camera Image / Sensor Data
    ↓
[Upload to Backend API]
    ↓
[Validation & Preprocessing]
    ├─ Image: Compression, format check
    ├─ Sensor: Range validation, outlier detection
    └─ Audio: Format check, quality assessment
    ↓
[AI Analysis Pipeline]
    ├─ Claude Vision API (primary)
    ├─ Fallback: OpenAI Vision
    └─ Fallback: Local TensorFlow models
    ↓
[Avicenna Interpretation]
    ├─ Map to mizaj
    ├─ Identify patterns
    └─ Cross-reference diseases
    ↓
[Generate Diagnosis Report]
    ├─ Avicenna diagnosis
    ├─ Modern diagnosis
    ├─ Confidence scores
    └─ Recommendations
    ↓
[Store in Database]
    ├─ Raw data
    ├─ Analysis results
    └─ Reports
    ↓
[Return to Mobile App]
    └─ Display to user

```

---

## 🗂️ Directory Structure After Phase 1

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sensor_data.py          # NEW
│   │   ├── image_analysis.py       # NEW
│   │   ├── wearable_device.py      # NEW
│   │   ├── vital_signs.py          # NEW
│   │   ├── audio_analysis.py       # NEW
│   │   ├── avicenna_analysis.py    # NEW
│   │   ├── diagnosis_report.py     # NEW
│   │   └── [existing files]
│   │
│   ├── schemas/
│   │   ├── sensor_schemas.py       # NEW
│   │   ├── image_schemas.py        # NEW
│   │   ├── wearable_schemas.py     # NEW
│   │   ├── vital_signs_schemas.py  # NEW
│   │   └── [existing files]
│   │
│   ├── routers/
│   │   ├── sensors.py              # NEW
│   │   ├── image_analysis.py       # NEW
│   │   ├── wearables.py            # NEW
│   │   ├── vital_signs.py          # NEW
│   │   ├── audio_analysis.py       # NEW
│   │   ├── diagnosis.py            # NEW
│   │   └── [existing files]
│   │
│   ├── services/
│   │   ├── ai_factory.py           # NEW
│   │   ├── ai_providers/           # NEW
│   │   │   ├── __init__.py
│   │   │   ├── claude_vision.py
│   │   │   ├── openai_vision.py
│   │   │   └── tensorflow_models.py
│   │   ├── analysis_service.py     # NEW
│   │   ├── image_analysis_service.py # NEW
│   │   ├── audio_analysis_service.py  # NEW
│   │   ├── avicenna_engine.py      # NEW
│   │   ├── wearable_integration.py # NEW
│   │   └── [existing files]
│   │
│   ├── database/
│   │   ├── migrations/             # NEW
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   │       └── 001_initial.py
│   │   └── [existing files]
│   │
│   ├── main.py                     # UPDATE: Add new routers
│   └── [existing files]
│
├── requirements.txt                # UPDATE: Add new dependencies
├── tests/                          # NEW
│   ├── test_sensors.py
│   ├── test_image_analysis.py
│   └── test_diagnosis.py
│
└── [existing files]
```

---

## 📦 New Dependencies to Install

```bash
# Image Processing
pip install pillow>=10.2.0
pip install opencv-python-headless>=4.8.0

# AI/ML
pip install torch>=2.0.0
pip install torchvision>=0.15.0
pip install tensorflow>=2.13.0
pip install scikit-learn>=1.3.0

# Audio Processing
pip install librosa>=0.10.0
pip install scipy>=1.11.0
pip install soundfile>=0.12.1

# Async Processing
pip install celery>=5.3.0
pip install redis>=5.0.0

# Database & ORM
pip install psycopg2-binary>=2.9.0
pip install alembic>=1.13.1

# API Clients
pip install openai>=1.12.0
pip install anthropic>=0.18.1
pip install google-cloud-vision>=3.4.0

# Time Series
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install statsmodels>=0.14.0
```

---

## ✅ Success Criteria

- [ ] All 8+ new database tables created
- [ ] All API endpoints responding correctly
- [ ] Image analysis working with Claude + fallback
- [ ] Sensor data pipeline functional
- [ ] Avicenna diagnosis engine live
- [ ] Database queries optimized (< 200ms)
- [ ] Error handling & logging complete
- [ ] 80%+ test coverage
- [ ] Documentation updated

---

## 🚨 Common Issues & Solutions

### Issue 1: Image Upload Size Limit
```python
# backend/app/main.py
app = FastAPI(...)
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

# Increase max upload size
@app.post("/upload")
async def upload(file: UploadFile):
    max_size = 50 * 1024 * 1024  # 50MB
    size = await file.size()
    if size > max_size:
        raise HTTPException(413, "File too large")
```

### Issue 2: AI API Timeouts
```python
# Use async with timeouts
import asyncio
from openai import AsyncOpenAI

async def analyze_with_timeout():
    try:
        result = await asyncio.wait_for(
            claude_client.messages.create(...),
            timeout=30
        )
    except asyncio.TimeoutError:
        # Fallback to local model
```

### Issue 3: Database Connection Pooling
```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
)
```

---

## 📞 Next Steps After Phase 1

Once Phase 1 is complete:
1. **Mobile Sensor Integration** (Phase 2)
2. **AI Model Optimization** (Phase 3)
3. **Web Dashboard** (Phase 4)
4. **Full Integration Testing** (Phase 5)

---

**Document Version**: 1.0  
**Last Updated**: December 15, 2025  
**Status**: Ready for Implementation
