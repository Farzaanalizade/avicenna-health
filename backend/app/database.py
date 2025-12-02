from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# ایجاد engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# ایجاد SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base برای مدل‌ها
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency برای دریافت database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """ایجاد جداول دیتابیس"""
    # Import models برای اطمینان از ثبت در metadata
    from app.models import patient  # noqa: F401
    
    # ایجاد تمام جداول
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
