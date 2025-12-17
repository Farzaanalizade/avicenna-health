# 🚀 PHASE 1 - IMMEDIATE ACTION PLAN
## Get Backend Ready in 1 Week

**Estimated Time**: 40-60 hours  
**Start Date**: Today  
**Target Completion**: End of Week  
**Status**: Ready to Begin

---

## ⏰ Weekly Schedule

### Day 1 (Today) - Planning & Setup (4 hours)

#### Morning (2 hours)
```
08:00 - Read PHASE_1_IMPLEMENTATION_GUIDE.md Section 1.1-1.2
09:00 - Review database design
10:00 - Plan file structure
```

#### Afternoon (2 hours)
```
13:00 - Set up development environment
14:00 - Verify backend is running
14:30 - Get Claude API key
15:00 - Test Claude API connection
```

### Days 2-3 (Mon-Tue) - Database Models (10 hours)

#### Create Model Files (5 hours)
```
- backend/app/models/sensor_data.py
- backend/app/models/image_analysis.py
- backend/app/models/wearable_device.py
- backend/app/models/vital_signs.py
- backend/app/models/audio_analysis.py
```

#### Create Schemas (5 hours)
```
- backend/app/schemas/sensor_schemas.py
- backend/app/schemas/image_schemas.py
- backend/app/schemas/vital_signs_schemas.py
```

### Days 4-5 (Wed-Thu) - API Endpoints (15 hours)

#### Create Routers (10 hours)
```
- backend/app/routers/sensors.py
- backend/app/routers/image_analysis.py
- backend/app/routers/wearables.py
- backend/app/routers/vital_signs.py
```

#### Testing (5 hours)
```
- Test each endpoint with Postman
- Add error handling
- Verify data validation
```

### Days 6-7 (Fri-Sat) - AI Integration & Polish (15 hours)

#### AI Integration (10 hours)
```
- Create backend/app/services/ai_factory.py
- Integrate Claude Vision API
- Set up fallback logic
- Test image analysis
```

#### Testing & Documentation (5 hours)
```
- Write unit tests
- Create API documentation
- Prepare for mobile integration
```

---

## 📋 Day-by-Day Tasks

### DAY 1: TODAY

#### Task 1.1: Read Documentation (30 min)
```
[ ] Open: PHASE_1_IMPLEMENTATION_GUIDE.md
[ ] Read: Sections 1.1 - 1.4 (Database design)
[ ] Understand: What tables you need to create
```

#### Task 1.2: Review Existing Code (30 min)
```
[ ] Check backend/app/models/patient.py
[ ] Check backend/app/main.py
[ ] Understand: Current database structure
```

#### Task 1.3: Plan File Structure (30 min)
```
[ ] Create list of files to create
[ ] Organize by priority
[ ] Estimate hours per file
```

#### Task 1.4: Environment Setup (60 min)
```
[ ] cd backend
[ ] pip install -r requirements.txt (if not done)
[ ] python -m uvicorn app.main:app --reload
[ ] Verify: Server runs on http://localhost:8000
[ ] Get Claude API key from https://console.anthropic.com
[ ] Set ANTHROPIC_API_KEY in .env
```

#### Task 1.5: Test Claude Connection (30 min)
```python
# Quick test in Python
from anthropic import Anthropic

client = Anthropic(api_key="your-key-here")
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content[0].text)
# Should print response if successful
```

---

### DAY 2-3: DATABASE MODELS

#### Task 2.1: Create SensorData Model (1 hour)
```python
# File: backend/app/models/sensor_data.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    sensor_type = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    raw_value = Column(JSON, nullable=False)
    processed_value = Column(JSON, nullable=True)
    unit = Column(String(20))
    device_info = Column(JSON, nullable=True)
    confidence_score = Column(Float, default=0.0)
    
    # Relationships
    patient = relationship("Patient", back_populates="sensor_readings")
```

#### Task 2.2: Create ImageAnalysis Model (1 hour)
```python
# File: backend/app/models/image_analysis.py

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
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
    ai_provider = Column(String(50))
    ai_analysis = Column(JSON, nullable=True)
    confidence_scores = Column(JSON, nullable=True)
    detected_features = Column(JSON, nullable=True)
    avicenna_assessment = Column(JSON, nullable=True)
    mizaj_indication = Column(String(50), nullable=True)
    analysis_status = Column(String(20), default="PENDING")
    error_message = Column(String(500), nullable=True)
    
    patient = relationship("Patient", back_populates="image_analyses")
```

#### Task 2.3: Create WearableDevice Model (1 hour)
```python
# File: backend/app/models/wearable_device.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class WearableDevice(Base):
    __tablename__ = "wearable_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    device_type = Column(String(50), nullable=False)  # Apple Watch, Fitbit, etc.
    device_id = Column(String(100), unique=True, nullable=False)
    device_name = Column(String(100))
    connection_status = Column(String(20), default="DISCONNECTED")
    last_sync = Column(DateTime, nullable=True)
    battery_level = Column(Integer, nullable=True)
    api_token = Column(String(500), nullable=True)
    sync_frequency = Column(Integer, default=300)  # seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="wearable_devices")
    vital_signs = relationship("VitalSigns", back_populates="wearable_device")
```

#### Task 2.4: Create VitalSigns Model (1 hour)
```python
# File: backend/app/models/vital_signs.py

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class VitalSigns(Base):
    __tablename__ = "vital_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    wearable_device_id = Column(Integer, ForeignKey("wearable_devices.id"), nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    heart_rate = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    body_temperature = Column(Float, nullable=True)
    systolic_bp = Column(Float, nullable=True)
    diastolic_bp = Column(Float, nullable=True)
    respiratory_rate = Column(Float, nullable=True)
    
    data_source = Column(String(50))  # wearable, manual, etc.
    quality_score = Column(Float, default=0.8)
    
    patient = relationship("Patient", back_populates="vital_signs")
    wearable_device = relationship("WearableDevice", back_populates="vital_signs")
```

#### Task 2.5: Create AudioAnalysis Model (1 hour)
```python
# File: backend/app/models/audio_analysis.py

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class AudioAnalysis(Base):
    __tablename__ = "audio_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    audio_type = Column(String(50), nullable=False)  # heartbeat, breathing
    audio_url = Column(String(500), nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Float)
    
    ai_analysis = Column(JSON, nullable=True)
    detected_abnormalities = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    analysis_status = Column(String(20), default="PENDING")
    error_message = Column(String(500), nullable=True)
    
    patient = relationship("Patient", back_populates="audio_analyses")
```

#### Task 2.6: Update Patient Model (30 min)
```python
# Add these relationships to backend/app/models/patient.py

# Add these imports at top
from app.models.sensor_data import SensorData
from app.models.image_analysis import ImageAnalysis
from app.models.wearable_device import WearableDevice
from app.models.vital_signs import VitalSigns
from app.models.audio_analysis import AudioAnalysis

# Add these relationships in Patient class
sensor_readings = relationship("SensorData", back_populates="patient", cascade="all, delete-orphan")
image_analyses = relationship("ImageAnalysis", back_populates="patient", cascade="all, delete-orphan")
wearable_devices = relationship("WearableDevice", back_populates="patient", cascade="all, delete-orphan")
vital_signs = relationship("VitalSigns", back_populates="patient", cascade="all, delete-orphan")
audio_analyses = relationship("AudioAnalysis", back_populates="patient", cascade="all, delete-orphan")
```

#### Task 2.7: Create Schemas (2 hours)
```python
# File: backend/app/schemas/sensor_schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SensorDataCreate(BaseModel):
    sensor_type: str
    raw_value: Dict[str, Any]
    unit: str
    device_info: Optional[Dict] = None
    timestamp: Optional[datetime] = None

class SensorDataResponse(BaseModel):
    id: int
    patient_id: int
    sensor_type: str
    raw_value: Dict
    processed_value: Optional[Dict]
    confidence_score: float
    timestamp: datetime

    class Config:
        from_attributes = True

# Similar patterns for image, vital signs, etc.
```

#### Task 2.8: Create Database Migrations (1 hour)
```bash
# In backend directory
cd backend
alembic revision --autogenerate -m "Add Phase 1 tables (sensors, images, vitals)"
# Review generated migration file
alembic upgrade head
```

**Verify**: Check PostgreSQL that all new tables exist
```sql
\dt
-- Should show:
-- sensor_data
-- image_analysis
-- wearable_devices
-- vital_signs
-- audio_analysis
```

---

### DAY 4-5: API ENDPOINTS

#### Task 4.1: Create Sensors Router (3 hours)
```python
# File: backend/app/routers/sensors.py

from fastapi import APIRouter, Depends, HTTPException
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
    """Upload sensor readings"""
    saved = []
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
        saved.append(db_reading)
    
    db.commit()
    return saved

@router.get("/{patient_id}")
async def get_sensor_data(
    patient_id: int,
    sensor_type: str = None,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get sensor data for patient"""
    query = db.query(SensorData).filter(SensorData.patient_id == patient_id)
    
    if sensor_type:
        query = query.filter(SensorData.sensor_type == sensor_type)
    
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    query = query.filter(SensorData.timestamp >= cutoff)
    
    return query.order_by(SensorData.timestamp.desc()).all()
```

#### Task 4.2: Create Image Analysis Router (3 hours)
```python
# File: backend/app/routers/image_analysis.py

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.image_analysis import ImageAnalysis, ImageType
from app.services.ai_factory import AIProviderFactory

router = APIRouter(prefix="/api/v1/analysis", tags=["image_analysis"])

ai_factory = AIProviderFactory()

@router.post("/tongue")
async def analyze_tongue(
    patient_id: int,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    """Analyze tongue image"""
    try:
        # Save image temporarily
        temp_path = f"/tmp/{file.filename}"
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # Analyze with Claude
        result = await ai_factory.analyze_tongue(temp_path)
        
        # Save to database
        analysis = ImageAnalysis(
            patient_id=patient_id,
            image_type=ImageType.TONGUE,
            image_url=temp_path,
            ai_provider="claude",
            ai_analysis=result,
            analysis_status="COMPLETE"
        )
        db.add(analysis)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Similar endpoints for eye, skin, face
```

#### Task 4.3: Create Wearables Router (2 hours)
```python
# File: backend/app/routers/wearables.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.wearable_device import WearableDevice

router = APIRouter(prefix="/api/v1/wearable", tags=["wearables"])

@router.post("/register")
async def register_wearable(
    patient_id: int,
    device_type: str,
    device_id: str,
    device_name: str,
    db: Session = Depends(get_db)
):
    """Register wearable device"""
    wearable = WearableDevice(
        patient_id=patient_id,
        device_type=device_type,
        device_id=device_id,
        device_name=device_name,
        connection_status="CONNECTED"
    )
    db.add(wearable)
    db.commit()
    return {"id": wearable.id, "status": "registered"}

@router.get("/sync-status/{patient_id}")
async def get_sync_status(patient_id: int, db: Session = Depends(get_db)):
    """Get wearable sync status"""
    devices = db.query(WearableDevice).filter(
        WearableDevice.patient_id == patient_id
    ).all()
    
    return [{
        "device_id": d.device_id,
        "status": d.connection_status,
        "last_sync": d.last_sync,
        "battery": d.battery_level
    } for d in devices]
```

#### Task 4.4: Create Vital Signs Router (2 hours)
```python
# File: backend/app/routers/vital_signs.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vital_signs import VitalSigns
from pydantic import BaseModel

class VitalSignsCreate(BaseModel):
    heart_rate: float
    spo2: float
    body_temperature: float
    systolic_bp: float
    diastolic_bp: float
    data_source: str

router = APIRouter(prefix="/api/v1/vital-signs", tags=["vital_signs"])

@router.post("/record")
async def record_vital_signs(
    patient_id: int,
    vitals: VitalSignsCreate,
    db: Session = Depends(get_db)
):
    """Record vital signs"""
    vital_record = VitalSigns(
        patient_id=patient_id,
        heart_rate=vitals.heart_rate,
        spo2=vitals.spo2,
        body_temperature=vitals.body_temperature,
        systolic_bp=vitals.systolic_bp,
        diastolic_bp=vitals.diastolic_bp,
        data_source=vitals.data_source
    )
    db.add(vital_record)
    db.commit()
    return {"id": vital_record.id, "status": "recorded"}

@router.get("/latest/{patient_id}")
async def get_latest_vitals(patient_id: int, db: Session = Depends(get_db)):
    """Get latest vital signs"""
    vitals = db.query(VitalSigns).filter(
        VitalSigns.patient_id == patient_id
    ).order_by(VitalSigns.timestamp.desc()).first()
    
    return vitals
```

#### Task 4.5: Register Routers in Main App (30 min)
```python
# In backend/app/main.py - add these imports and registration

from app.routers import sensors, image_analysis, wearables, vital_signs

# Add after existing router includes:
app.include_router(sensors.router)
app.include_router(image_analysis.router)
app.include_router(wearables.router)
app.include_router(vital_signs.router)
```

#### Task 4.6: Test Endpoints (2 hours)
```bash
# Use Postman or curl to test

# Test sensor upload
curl -X POST http://localhost:8000/api/v1/sensor-data/upload \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1, "sensor_readings": [{"sensor_type": "GYRO", "raw_value": {"x": 0.1, "y": 0.2}, "unit": "deg/s"}]}'

# Test vital signs
curl -X POST http://localhost:8000/api/v1/vital-signs/record \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1, "heart_rate": 72, "spo2": 98, "body_temperature": 37.0, "systolic_bp": 120, "diastolic_bp": 80, "data_source": "wearable"}'
```

---

### DAY 6-7: AI INTEGRATION & POLISH

#### Task 6.1: Create AI Factory (3 hours)
```python
# File: backend/app/services/ai_factory.py

from anthropic import Anthropic
import json
import base64

class AIProviderFactory:
    def __init__(self):
        self.claude_client = Anthropic()
    
    async def analyze_tongue(self, image_path: str) -> dict:
        """Analyze tongue image with Claude"""
        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            prompt = """
            Analyze this tongue image according to Avicenna's Persian medicine:
            
            Return JSON with:
            {
                "color": "pink|red|pale|yellow|white",
                "coating": "none|white|yellow|brown",
                "moisture": "dry|normal|wet",
                "texture": "smooth|rough|cracked",
                "avicenna_diagnosis": "HOT_DRY|HOT_WET|COLD_WET|COLD_DRY",
                "mizaj_imbalance": "mild|moderate|severe",
                "confidence_score": 0.0-1.0
            }
            """
            
            message = self.claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": [{
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    }, {
                        "type": "text",
                        "text": prompt
                    }]
                }]
            )
            
            # Parse response
            response_text = message.content[0].text
            result = json.loads(response_text)
            return {
                "status": "success",
                "analysis": result,
                "provider": "claude"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "provider": "claude"
            }
    
    async def analyze_eye(self, image_path: str) -> dict:
        """Similar for eye"""
        pass
    
    async def analyze_skin(self, image_path: str) -> dict:
        """Similar for skin"""
        pass
    
    async def analyze_face(self, image_path: str) -> dict:
        """Similar for face"""
        pass
```

#### Task 6.2: Test Claude Integration (2 hours)
```bash
# Test with sample image
python -c "
from backend.app.services.ai_factory import AIProviderFactory
import asyncio

factory = AIProviderFactory()
result = asyncio.run(factory.analyze_tongue('path/to/tongue/image.jpg'))
print(result)
"
```

#### Task 6.3: Write Unit Tests (3 hours)
```python
# File: backend/tests/test_sensors.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sensor_upload():
    response = client.post(
        "/api/v1/sensor-data/upload",
        json={
            "patient_id": 1,
            "sensor_readings": [{
                "sensor_type": "GYRO",
                "raw_value": {"x": 0.1},
                "unit": "deg/s"
            }]
        }
    )
    assert response.status_code == 200

def test_vital_signs():
    response = client.post(
        "/api/v1/vital-signs/record",
        json={
            "patient_id": 1,
            "heart_rate": 72,
            "spo2": 98,
            "body_temperature": 37.0,
            "systolic_bp": 120,
            "diastolic_bp": 80,
            "data_source": "wearable"
        }
    )
    assert response.status_code == 200
```

#### Task 6.4: Documentation & Handoff (1 hour)
```
[ ] Create API documentation
[ ] Write README for Phase 1
[ ] List what's working
[ ] List what's next (Phase 2)
[ ] Prepare for team handoff
```

---

## ✅ Checklist

### Before You Start
- [ ] Backend server running
- [ ] PostgreSQL connected
- [ ] Claude API key obtained
- [ ] Code editor open
- [ ] Requirements installed

### Day 1
- [ ] Read documentation
- [ ] Review existing code
- [ ] Environment setup complete
- [ ] Claude connection tested

### Days 2-3
- [ ] 5 new models created
- [ ] 3 new schemas created
- [ ] Database migrations run
- [ ] New tables verified in database

### Days 4-5
- [ ] 4 API routers created
- [ ] All endpoints tested
- [ ] Error handling added
- [ ] Data validation working

### Days 6-7
- [ ] Claude integration complete
- [ ] Image analysis working
- [ ] Unit tests written
- [ ] Documentation updated

---

## 🎯 Success Criteria

### Technical
- ✅ All 5 database tables created
- ✅ 10+ API endpoints working
- ✅ Claude analysis functional
- ✅ 80%+ test coverage
- ✅ All errors handled gracefully

### Quality
- ✅ Code follows PEP 8
- ✅ Documentation complete
- ✅ No hardcoded values
- ✅ Proper error messages
- ✅ Logging implemented

### Performance
- ✅ API response < 500ms
- ✅ Image analysis < 5 seconds
- ✅ Database queries optimized
- ✅ No memory leaks

---

## 🚨 If You Get Stuck

### Database Issues
→ Check: `PHASE_1_IMPLEMENTATION_GUIDE.md` Section 1.1  
→ Test: `psql` connection directly

### Claude API Fails
→ Check: API key in `.env`  
→ Test: Claude connection script  
→ Review: `AI_PROVIDERS_COMPARISON.md`

### Endpoint Not Working
→ Check: Router registered in `main.py`  
→ Test: `curl` command directly  
→ Review: Request/response format

### Model Import Error
→ Check: Models imported in `__init__.py`  
→ Check: Relationships defined correctly  
→ Run: Migration again

---

## 📞 Quick Commands

```bash
# Start backend
cd backend && python -m uvicorn app.main:app --reload

# Run tests
pytest backend/tests/ -v

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Check database
psql -U username -d avicenna -c "\dt"

# Quick Python test
python -c "from anthropic import Anthropic; print('OK')"
```

---

## 🎉 After This Week

You'll have:
- ✅ Production-ready backend
- ✅ 10+ working API endpoints
- ✅ Claude image analysis integrated
- ✅ Full database schema
- ✅ Ready for mobile integration

**Next**: Phase 2 - Mobile Sensor Integration (Week 2-3)

---

**Good luck! You've got this! 💪**

Start with Task 1.1 → Get Claude key → Create first model → Ship it!

