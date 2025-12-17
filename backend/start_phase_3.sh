#!/usr/bin/env bash

# 🚀 Phase 3 - Quick Start Script
# این اسکریپت تمام چیزهای لازم برای تست کردن رو آماده می‌کنه

set -e

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Main Script
print_header "🚀 Phase 3 - Quick Start Setup"

# Step 1: Check Python
print_info "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Step 2: Check Backend Directory
print_info "Checking backend directory..."
if [ -d "backend" ]; then
    print_success "Backend directory found"
    cd backend
else
    print_error "Backend directory not found. Run this script from project root."
    exit 1
fi

# Step 3: Check Virtual Environment
print_info "Checking virtual environment..."
if [ -d "venv" ]; then
    print_success "Virtual environment found"
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
else
    print_error "Virtual environment not found"
    print_info "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
    print_success "Virtual environment created"
fi

# Step 4: Install/Update Dependencies
print_info "Checking dependencies..."
pip install -q -r requirements.txt
print_success "Dependencies installed"

# Step 5: Check/Create .env file
print_info "Checking .env file..."
if [ -f ".env" ]; then
    print_success ".env file found"
    
    # Check if GEMINI_API_KEY is set
    if grep -q "GEMINI_API_KEY" .env; then
        print_success "GEMINI_API_KEY is configured"
    else
        print_info "GEMINI_API_KEY not set in .env"
        echo "GEMINI_API_KEY=your_key_from_makersuite.google.com" >> .env
        print_info "Added GEMINI_API_KEY placeholder to .env"
    fi
else
    print_error ".env file not found"
    print_info "Creating .env file..."
    
    cat > .env << EOF
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
EOF
    
    print_success ".env file created"
    print_info "⚠️  Please set GEMINI_API_KEY in .env file"
fi

# Step 6: Initialize Database
print_info "Initializing database..."
if [ -f "avicenna.db" ]; then
    print_success "Database already exists"
else
    print_info "Creating database..."
    python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null || true
    print_success "Database initialized"
fi

# Step 7: Test Imports
print_info "Testing imports..."
python3 -c "from app.main import app; from app.services.gemini_vision_service import GeminiService; print('✅ Imports OK')" 2>/dev/null || print_error "Import error"

# Step 8: Start Backend
print_header "🚀 Starting Backend Server"
print_info "Starting on http://localhost:8000"
print_info "API Docs available at http://localhost:8000/docs"
print_info ""
print_info "Press Ctrl+C to stop server"
print_info ""

python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
