#!/usr/bin/env python
"""
🎮 Start Android Emulator
Emulator Launcher
"""

import subprocess
import sys
import os

def start_emulator():
    """Start Android Emulator"""
    
    mobile_path = r"d:\AvicennaAI\mobile"
    os.chdir(mobile_path)
    
    print("="*60)
    print("🎮 Android Emulator Launcher")
    print("="*60)
    print()
    
    # First list available emulators
    print("📋 Available emulators:")
    print()
    
    try:
        result = subprocess.run([
            "flutter",
            "emulators"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        print("\n🚀 Starting Pixel_6_API_33...")
        print()
        
        subprocess.run([
            "flutter",
            "emulators",
            "--launch",
            "Pixel_6_API_33"
        ])
        
    except KeyboardInterrupt:
        print("\n\n⛔ Emulator stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nMake sure you have Android emulator installed and configured.")
        sys.exit(1)

if __name__ == "__main__":
    start_emulator()
