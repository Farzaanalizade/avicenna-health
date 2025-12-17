#!/usr/bin/env python
"""
🧪 API Test Script - Test Backend + Mobile Connectivity
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("🔍 Testing Root Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_swagger():
    """Test Swagger UI"""
    print("\n" + "="*60)
    print("📚 Testing Swagger UI")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Swagger UI available at: {BASE_URL}/docs")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("❤️  Testing Health Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Endpoint not found (expected): {e}")
        return False

def test_auth_signup():
    """Test auth signup"""
    print("\n" + "="*60)
    print("🔐 Testing Auth Signup")
    print("="*60)
    try:
        payload = {
            "email": "test@example.com",
            "password": "Test@123456",
            "full_name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=payload)
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Avicenna AI - Backend API Test Suite                    ║")
    print("║   Testing connectivity and basic endpoints                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    results = {
        "Root Endpoint": test_root(),
        "Swagger UI": test_swagger(),
        "Health Endpoint": test_health(),
        "Auth Signup": test_auth_signup(),
    }
    
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is ready for mobile app!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("\n" + "="*60)
    print("🚀 Next Steps:")
    print("="*60)
    print("1. Keep Backend running on http://localhost:8000")
    print("2. Mobile app should connect to: http://10.0.2.2:8000 (Android)")
    print("3. Or: http://localhost:8000 (Web/Windows)")
    print("4. Try diagnostic flow in mobile app")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
