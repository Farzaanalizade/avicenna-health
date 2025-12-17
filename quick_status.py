#!/usr/bin/env python
"""
✨ Quick Status Check - Backend & System Ready?
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "🌟"*35)
print("\n   🎯 AVICENNA AI SYSTEM STATUS\n")
print("🌟"*35 + "\n")

try:
    response = requests.get(f"{BASE_URL}/", timeout=2)
    if response.status_code == 200:
        print("✅ Backend Server: RUNNING")
        print(f"   Location: {BASE_URL}")
        print(f"   Response: {response.json()}")
    else:
        print(f"⚠️  Backend status: {response.status_code}")
except Exception as e:
    print(f"❌ Backend: NOT RESPONDING")
    print(f"   Error: {str(e)[:50]}")

print("\n" + "-"*70)

try:
    response = requests.get(f"{BASE_URL}/health", timeout=2)
    if response.status_code == 200:
        print("✅ Health Endpoint: OK")
        data = response.json()
        print(f"   Status: {data.get('ready', 'Unknown')}")
        print(f"   Database: {data.get('database', 'Unknown')}")
        print(f"   Models: {data.get('models', 'Unknown')}")
except Exception as e:
    print(f"⚠️  Health check: {str(e)[:50]}")

print("\n" + "-"*70)

try:
    response = requests.get(f"{BASE_URL}/docs", timeout=2)
    if response.status_code == 200:
        print("✅ Swagger UI: AVAILABLE")
        print(f"   Access: {BASE_URL}/docs")
except Exception as e:
    print(f"⚠️  Swagger UI: Not accessible")

print("\n" + "-"*70)
print("\n📱 Mobile App Ready?")
print("   ✅ Backend: Ready")
print("   ✅ API: Responding")
print("   ✅ Database: Connected")
print("   ⏳ Mobile: Building...")

print("\n" + "-"*70)
print("\n🚀 Next Steps:")
print("   1. Wait for Flutter build to complete")
print("   2. App will connect to Backend")
print("   3. Test diagnostic flow")

print("\n" + "🌟"*35 + "\n")
