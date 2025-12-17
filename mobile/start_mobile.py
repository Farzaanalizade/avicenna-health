#!/usr/bin/env python
"""
📱 Start Mobile App on Emulator
Flutter App Launcher
"""

import subprocess
import sys
import os

def start_mobile():
    """Start Flutter Mobile App"""
    
    mobile_path = r"d:\AvicennaAI\mobile"
    os.chdir(mobile_path)
    
    print("="*60)
    print("📱 Avicenna AI Mobile App")
    print("="*60)
    print()
    print(f"📍 Location: {mobile_path}")
    print()
    
    # First check devices
    print("📱 Checking available devices...")
    print()
    
    try:
        result = subprocess.run([
            "flutter",
            "devices"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if "emulator" not in result.stdout.lower() and "device" not in result.stdout.lower():
            print("⚠️  No emulator or device found!")
            print("Please start Android Emulator first:")
            print("  flutter emulators --launch Pixel_6_API_33")
            return
        
        print("\n🚀 Starting Flutter app...")
        print()
        
        subprocess.run([
            "flutter",
            "run"
        ])
        
    except KeyboardInterrupt:
        print("\n\n⛔ App stopped by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_mobile()
