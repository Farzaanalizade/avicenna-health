@echo off
REM 🚀 Phase 3 - Quick Start Script (Batch - Windows)
REM این اسکریپت تمام چیزهای لازم برای تست کردن رو آماده می‌کنه

setlocal enabledelayedexpansion
title Avicenna Health - Phase 3 Backend

cls
echo.
echo ========================================
echo 🚀 Phase 3 - Quick Start Setup
echo ========================================
echo.

REM Step 1: Check Python
echo [1/8] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%
echo.

REM Step 2: Check Backend Directory
echo [2/8] Checking backend directory...
if exist backend (
    echo ✅ Backend directory found
    cd backend
) else (
    echo ❌ Backend directory not found.
    echo Please run this script from project root.
    pause
    exit /b 1
)
echo.

REM Step 3: Check Virtual Environment
echo [3/8] Checking virtual environment...
if exist venv (
    echo ✅ Virtual environment found
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment created
)
echo.

REM Step 4: Install Dependencies
echo [4/8] Installing dependencies...
pip install -q -r requirements.txt
echo ✅ Dependencies installed
echo.

REM Step 5: Check .env File
echo [5/8] Checking .env file...
if exist .env (
    echo ✅ .env file found
    findstr /m "GEMINI_API_KEY" .env >nul
    if %errorlevel% equ 0 (
        echo ✅ GEMINI_API_KEY is configured
    ) else (
        echo ℹ️  Adding GEMINI_API_KEY placeholder...
        echo.>> .env
        echo GEMINI_API_KEY=your_key_from_makersuite.google.com>> .env
    )
) else (
    echo ❌ .env file not found
    echo Creating .env file...
    (
        echo # Avicenna Health - Backend Configuration
        echo.
        echo # Database
        echo DATABASE_URL=sqlite:///./avicenna.db
        echo.
        echo # JWT Security
        echo JWT_SECRET_KEY=your-super-secret-key-change-in-production
        echo JWT_ALGORITHM=HS256
        echo JWT_EXPIRATION_HOURS=168
        echo.
        echo # Google Gemini API
        echo GEMINI_API_KEY=your_key_from_makersuite.google.com
        echo.
        echo # CORS Origins
        echo CORS_ORIGINS=["http://localhost:8000","http://localhost:3000","http://localhost:5173"]
        echo.
        echo # Image Processing
        echo MAX_IMAGE_SIZE_MB=5
        echo MAX_IMAGE_DIMENSION=4096
        echo MIN_IMAGE_DIMENSION=480
        echo.
        echo # Environment
        echo ENVIRONMENT=development
        echo DEBUG=True
    ) > .env
    echo ✅ .env file created
    echo ⚠️  Please set GEMINI_API_KEY in .env file
)
echo.

REM Step 6: Initialize Database
echo [6/8] Initializing database...
if exist avicenna.db (
    echo ✅ Database already exists
) else (
    echo Creating database...
    python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" 2>nul
    echo ✅ Database initialized
)
echo.

REM Step 7: Test Imports
echo [7/8] Testing imports...
python -c "from app.main import app; from app.services.gemini_vision_service import GeminiService; print('✅ Imports OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Import error - check your installation
)
echo.

REM Step 8: Start Backend
cls
echo.
echo ========================================
echo 🚀 Starting Backend Server
echo ========================================
echo.
echo ✅ Starting on http://localhost:8000
echo ✅ API Docs: http://localhost:8000/docs
echo ✅ ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo.
echo ℹ️  Server stopped
echo.
pause
