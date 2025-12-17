"""
Production environment configuration for Avicenna AI
Loaded from environment variables for Docker/K8s deployment
"""

from pydantic import BaseSettings
from typing import Optional
import logging

class ProductionSettings(BaseSettings):
    """Production environment settings"""
    
    # Application settings
    APP_NAME: str = "Avicenna AI - Production"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"
    
    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    WORKERS: int = 4
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 40
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    # Redis/Cache
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT: int = 3600
    CACHE_PREDICTION_TIMEOUT: int = 86400  # 24 hours
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 168  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # CORS - Production domains
    ALLOWED_ORIGINS: list = [
        "https://your_domain.com",
        "https://www.your_domain.com",
        "https://app.your_domain.com",
    ]
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File uploads
    MAX_UPLOAD_SIZE_MB: int = 5
    UPLOAD_DIRECTORY: str = "/tmp/uploads"
    ALLOWED_UPLOAD_TYPES: list = ["image/jpeg", "image/png", "image/webp"]
    
    # API Keys - External services
    GEMINI_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    
    # Email (for reports, notifications)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@your_domain.com"
    
    # Monitoring & Logging
    SENTRY_DSN: Optional[str] = None  # Error tracking
    LOG_TO_FILE: bool = True
    LOG_FILE_PATH: str = "/var/log/avicenna/app.log"
    LOG_MAX_BYTES: int = 10_485_760  # 10MB
    LOG_BACKUP_COUNT: int = 10
    
    # Metrics
    PROMETHEUS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    # Feature flags
    ENABLE_WEBSOCKET: bool = True
    ENABLE_REAL_TIME_UPDATES: bool = True
    ENABLE_ML_PREDICTIONS: bool = True
    ENABLE_ADMIN_PANEL: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_production_settings() -> ProductionSettings:
    """Get production settings instance"""
    return ProductionSettings()

def setup_logging(settings: ProductionSettings):
    """Setup production logging with rotation"""
    from logging.handlers import RotatingFileHandler
    import json
    from datetime import datetime
    
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'line': record.lineno,
            }
            if record.exc_info:
                log_data['exception'] = self.formatException(record.exc_info)
            return json.dumps(log_data)
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    if settings.LOG_TO_FILE:
        file_handler = RotatingFileHandler(
            settings.LOG_FILE_PATH,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    logger.addHandler(console_handler)
    
    return logger

def get_settings() -> ProductionSettings:
    """
    Get settings - returns ProductionSettings in production mode
    """
    return ProductionSettings()
