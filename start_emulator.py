#!/usr/bin/env python
"""
🎮 Android Emulator Starter
شروع کننده شبیه‌ساز اندروید
"""

import subprocess
import sys
import os
from pathlib import Path

def start_emulator():
    """Start Android Emulator"""
    
    mobile_path = Path(__file__).parent / "mobile"
    os.chdir(mobile_path)
    
    print("\n" + "="*60)
    print("🎮 Android Emulator")
    print("="*60 + "\n")
    
    print("Available emulators:\n")
    result = subprocess.run(["flutter", "emulators"], capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"✗ Error: {result.stderr}")
        print("\nTrying to launch Pixel_6_API_33...")
    
    print("-"*60)
    print("Starting emulator: Pixel_6_API_33\n")
    
    cmd = ["flutter", "emulators", "--launch", "Pixel_6_API_33"]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n✗ Emulator stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTrying alternative emulator names...")
        sys.exit(1)

if __name__ == "__main__":
    start_emulator()
