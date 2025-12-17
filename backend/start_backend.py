#!/usr/bin/env python
"""
🚀 Start Backend Server
Avicenna AI Backend Launcher
"""

import subprocess
import sys
import os

def start_backend():
    """Start FastAPI Backend Server"""
    
    backend_path = r"d:\AvicennaAI\backend"
    os.chdir(backend_path)
    
    python_exe = r"d:\AvicennaAI\backend\venv\Scripts\python.exe"
    
    print("="*60)
    print("🚀 Avicenna AI Backend Server")
    print("="*60)
    print()
    print(f"📍 Location: {backend_path}")
    print(f"🐍 Python: {python_exe}")
    print(f"🔌 Port: 8000")
    print()
    print("Starting uvicorn server...")
    print()
    
    try:
        subprocess.run([
            python_exe,
            "-m",
            "uvicorn",
            "app.main:app",
            "--reload",
            "--port",
            "8000",
            "--host",
            "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n⛔ Server stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_backend()
