#!/usr/bin/env python
"""
🚀 Master Launcher - Start Both Backend + Mobile
Full Stack Startup Script
"""

import subprocess
import sys
import os
import time
import threading

def run_backend():
    """Run backend in background"""
    print("\n" + "="*60)
    print("🖥️  BACKEND SERVER")
    print("="*60 + "\n")
    
    backend_path = r"d:\AvicennaAI\backend"
    python_exe = r"d:\AvicennaAI\backend\venv\Scripts\python.exe"
    
    os.chdir(backend_path)
    
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
    except Exception as e:
        print(f"❌ Backend Error: {e}")

def run_emulator():
    """Run emulator"""
    print("\n" + "="*60)
    print("🎮 ANDROID EMULATOR")
    print("="*60 + "\n")
    
    time.sleep(2)  # Wait for backend to start
    
    mobile_path = r"d:\AvicennaAI\mobile"
    os.chdir(mobile_path)
    
    try:
        subprocess.run([
            "flutter",
            "emulators",
            "--launch",
            "Pixel_6_API_33"
        ])
    except Exception as e:
        print(f"❌ Emulator Error: {e}")

def run_mobile():
    """Run mobile app"""
    print("\n" + "="*60)
    print("📱 MOBILE APP")
    print("="*60 + "\n")
    
    time.sleep(45)  # Wait for emulator to start
    
    mobile_path = r"d:\AvicennaAI\mobile"
    os.chdir(mobile_path)
    
    try:
        subprocess.run([
            "flutter",
            "run"
        ])
    except Exception as e:
        print(f"❌ Mobile Error: {e}")

def main():
    """Start all services"""
    
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "🚀 AVICENNA AI FULL STACK" + " "*17 + "║")
    print("║" + " "*20 + "Backend + Mobile Launcher" + " "*13 + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("Starting services in order:")
    print("  1️⃣  Backend Server (Port 8000)")
    print("  2️⃣  Android Emulator")
    print("  3️⃣  Mobile App (on Emulator)")
    print()
    
    # Create threads
    backend_thread = threading.Thread(target=run_backend, daemon=False)
    emulator_thread = threading.Thread(target=run_emulator, daemon=False)
    mobile_thread = threading.Thread(target=run_mobile, daemon=False)
    
    # Start backend first
    backend_thread.start()
    
    # Start emulator after backend
    emulator_thread.start()
    
    # Start mobile app after emulator
    mobile_thread.start()
    
    # Wait for all to complete
    backend_thread.join()
    emulator_thread.join()
    mobile_thread.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ All services stopped by user")
        sys.exit(0)
