#!/usr/bin/env python
"""
📱 Flutter Mobile App Starter
شروع کننده اپ موبایل
"""

import subprocess
import sys
import os
from pathlib import Path

def start_mobile():
    """Start Flutter mobile app"""
    
    mobile_path = Path(__file__).parent / "mobile"
    os.chdir(mobile_path)
    
    print("\n" + "="*60)
    print("📱 Avicenna AI - Mobile App (Flutter)")
    print("="*60)
    print(f"✓ Mobile Path: {mobile_path}")
    print("="*60 + "\n")
    
    print("Checking available devices...\n")
    subprocess.run(["flutter", "devices"], check=False)
    
    print("\n" + "-"*60)
    print("Starting Flutter app...\n")
    
    cmd = ["flutter", "run"]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n✗ App stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_mobile()
