from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.patient import Patient
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """بررسی رمز عبور"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """هش کردن رمز عبور"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """ایجاد توکن JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """بررسی اعتبار توکن"""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        patient_id: str = payload.get("sub")
        
        if patient_id is None:
            raise credentials_exception
            
        return patient_id
    except JWTError:
        raise credentials_exception


async def get_current_patient(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Patient:
    """دریافت بیمار فعلی از توکن"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    patient_id = verify_token(token, credentials_exception)
    
    # تبدیل به int (چون در دیتابیس ID عددی است)
    try:
        patient_id = int(patient_id)
    except ValueError:
        raise credentials_exception
    
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if patient is None:
        raise credentials_exception
    
    if not patient.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    
    return patient


async def get_current_active_patient(
    current_patient: Patient = Depends(get_current_patient)
) -> Patient:
    """دریافت بیمار فعال"""
    if not current_patient.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب کاربری غیرفعال است"
        )
    return current_patient
