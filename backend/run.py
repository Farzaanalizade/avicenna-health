"""
Entry point for running the FastAPI application
This allows running with: uvicorn run:app --reload
Or directly: python run.py
"""
import uvicorn
from app.main import app

__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

