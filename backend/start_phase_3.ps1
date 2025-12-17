# 🚀 Phase 3 - Quick Start Script (PowerShell - Windows)
# این اسکریپت تمام چیزهای لازم برای تست کردن رو آماده می‌کنه

# Requires -Version 3.0

# رنگ‌ها
$GREEN = 'Green'
$RED = 'Red'
$YELLOW = 'Yellow'
$CYAN = 'Cyan'

function Print-Header {
    param([string]$Text)
    Write-Host "`n" -ForegroundColor $CYAN
    Write-Host "========================================" -ForegroundColor $CYAN
    Write-Host $Text -ForegroundColor $CYAN
    Write-Host "========================================" -ForegroundColor $CYAN
    Write-Host ""
}

function Print-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor $GREEN
}

function Print-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor $RED
}

function Print-Info {
    param([string]$Text)
    Write-Host "ℹ️  $Text" -ForegroundColor $YELLOW
}

# Main Script
Print-Header "🚀 Phase 3 - Quick Start Setup"

# Step 1: Check Python
Print-Info "Checking Python..."
$pythonCheck = python --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Print-Success "Python found: $pythonCheck"
} else {
    Print-Error "Python not found. Please install Python 3.9+"
    exit 1
}

# Step 2: Check Backend Directory
Print-Info "Checking backend directory..."
if (Test-Path "backend") {
    Print-Success "Backend directory found"
    Set-Location backend
} else {
    Print-Error "Backend directory not found. Run this script from project root."
    exit 1
}

# Step 3: Check Virtual Environment
Print-Info "Checking virtual environment..."
if (Test-Path "venv") {
    Print-Success "Virtual environment found"
    & "venv\Scripts\Activate.ps1"
} else {
    Print-Error "Virtual environment not found"
    Print-Info "Creating virtual environment..."
    python -m venv venv
    & "venv\Scripts\Activate.ps1"
    Print-Success "Virtual environment created"
}

# Step 4: Install/Update Dependencies
Print-Info "Installing dependencies..."
pip install -q -r requirements.txt
Print-Success "Dependencies installed"

# Step 5: Check/Create .env file
Print-Info "Checking .env file..."
if (Test-Path ".env") {
    Print-Success ".env file found"
    
    # Check if GEMINI_API_KEY is set
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GEMINI_API_KEY") {
        Print-Success "GEMINI_API_KEY is configured"
    } else {
        Print-Info "GEMINI_API_KEY not set in .env"
        Add-Content ".env" "`nGEMINI_API_KEY=your_key_from_makersuite.google.com"
        Print-Info "Added GEMINI_API_KEY placeholder to .env"
    }
} else {
    Print-Error ".env file not found"
    Print-Info "Creating .env file..."
    
    $envContent = @'
# Avicenna Health - Backend Configuration

# Database
DATABASE_URL=sqlite:///./avicenna.db

# JWT Security
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168

# Google Gemini API
GEMINI_API_KEY=your_key_from_makersuite.google.com

# CORS Origins
CORS_ORIGINS=["http://localhost:8000","http://localhost:3000","http://localhost:5173"]

# Image Processing
MAX_IMAGE_SIZE_MB=5
MAX_IMAGE_DIMENSION=4096
MIN_IMAGE_DIMENSION=480

# Environment
ENVIRONMENT=development
DEBUG=True
'@
    
    Set-Content ".env" $envContent
    Print-Success ".env file created"
    Print-Info "⚠️  Please set GEMINI_API_KEY in .env file"
}

# Step 6: Initialize Database
Print-Info "Initializing database..."
if (Test-Path "avicenna.db") {
    Print-Success "Database already exists"
} else {
    Print-Info "Creating database..."
    python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" 2>$null
    Print-Success "Database initialized"
}

# Step 7: Test Imports
Print-Info "Testing imports..."
$importTest = python -c "from app.main import app; from app.services.gemini_vision_service import GeminiService; print('OK')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Print-Success "Imports OK"
} else {
    Print-Error "Import error - check your Python installation"
}

# Step 8: Display Instructions
Print-Header "🚀 Starting Backend Server"
Print-Info "Starting on http://localhost:8000"
Print-Info "API Docs available at http://localhost:8000/docs"
Print-Info ""
Print-Info "Press Ctrl+C to stop server"
Print-Info ""

# Step 9: Start Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Cleanup on exit
Write-Host "`n"
Print-Info "Server stopped"
