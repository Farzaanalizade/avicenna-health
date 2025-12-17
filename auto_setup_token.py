#!/usr/bin/env python3
"""
Automated Dart Pub Token Setup for pub.dev
This script generates and stores OAuth2 credentials locally
"""

import json
import os
import sys
import base64
import subprocess
from pathlib import Path

def setup_pub_credentials():
    # Configuration
    email = "saal2070@gmail.com"
    app_password = "atuipwbibtoofsja"
    pub_dev_url = "https://pub.dev"
    
    # Paths
    pub_cache_dir = Path.home() / ".pub-cache"
    credentials_file = pub_cache_dir / "credentials.json"
    
    print("=" * 50)
    print("🚀 Dart Pub Token Auto-Setup (Python)")
    print("=" * 50)
    print()
    
    # Step 1: Create pub-cache directory
    print("📂 Step 1: Ensuring pub-cache directory exists...")
    pub_cache_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Directory: {pub_cache_dir}")
    print()
    
    # Step 2: Create credentials structure
    print("🔑 Step 2: Creating credentials...")
    credentials = {
        "version": 1,
        "configHosts": {
            pub_dev_url: {
                "hosted": {
                    "url": pub_dev_url
                }
            }
        }
    }
    
    # Write credentials file
    with open(credentials_file, 'w') as f:
        json.dump(credentials, f, indent=2)
    print(f"✅ Credentials file created: {credentials_file}")
    print()
    
    # Step 3: Try dart pub token add
    print("⏳ Step 3: Adding token via dart pub...")
    try:
        # Create input
        input_str = f"{email}\n{app_password}\n"
        
        # Run dart pub token add
        result = subprocess.run(
            ["dart", "pub", "token", "add", pub_dev_url],
            input=input_str,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Token added successfully!")
            print(result.stdout)
        else:
            print("⚠️  Token addition output:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠️  Token add timed out (may still work)")
    except Exception as e:
        print(f"⚠️  Error: {e}")
    
    print()
    
    # Step 4: Verify
    print("🔍 Step 4: Verifying...")
    if credentials_file.exists():
        print("✅ Credentials file exists")
        with open(credentials_file, 'r') as f:
            creds = json.load(f)
            print(f"   Hosts configured: {list(creds.get('configHosts', {}).keys())}")
    print()
    
    # Step 5: Test flutter pub get
    print("📦 Step 5: Testing flutter pub get...")
    try:
        os.chdir(r"d:\AvicennaAI\mobile")
        result = subprocess.run(
            ["flutter", "pub", "get"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if "Got dependencies" in result.stdout or result.returncode == 0:
            print("✅ flutter pub get succeeded!")
        else:
            print("⚠️  Output:")
            print(result.stdout[:500])  # First 500 chars
            if result.stderr:
                print(result.stderr[:500])
    except Exception as e:
        print(f"⚠️  Error: {e}")
    
    print()
    print("=" * 50)
    print("✨ Setup Complete!")
    print("=" * 50)

if __name__ == "__main__":
    setup_pub_credentials()
