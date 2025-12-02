from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "AvicennaAI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./avicenna.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
