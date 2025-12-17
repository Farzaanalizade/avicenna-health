#!/usr/bin/env python
"""
🚀 Backend Server Starter
شروع کننده سرور Backend
"""

import subprocess
import sys
import os
from pathlib import Path

def start_backend():
    """Start FastAPI backend server"""
    
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Python path
    python_exe = backend_path / "venv" / "Scripts" / "python.exe"
    
    print("\n" + "="*60)
    print("🚀 Avicenna AI - Backend Server")
    print("="*60)
    print(f"✓ Backend Path: {backend_path}")
    print(f"✓ Python Exe: {python_exe}")
    print(f"✓ Port: 8000")
    print("="*60 + "\n")
    
    # Start uvicorn
    cmd = [
        str(python_exe),
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--port", "8000",
        "--host", "0.0.0.0"
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n✗ Backend stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_backend()
