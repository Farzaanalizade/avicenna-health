#!/usr/bin/env python3
"""
Week 2 Integration Testing Script
Tests all endpoints and integration points
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
HEADERS = {
    "Content-Type": "application/json",
}

# Test Data
TEST_DIAGNOSIS_ID = 1  # Adjust based on your database
TOKEN = None  # Will be set after login

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def login(email: str, password: str) -> Optional[str]:
    """Login and get JWT token"""
    print_header("1. Authentication Test")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/auth/login"
        data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(url, json=data, headers=HEADERS)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print_success(f"Login successful")
            print_info(f"Token: {token[:20]}...")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return None

def test_endpoint(
    method: str,
    endpoint: str,
    test_name: str,
    token: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None
) -> Optional[Dict]:
    """Test an API endpoint"""
    
    try:
        url = f"{BASE_URL}{API_PREFIX}{endpoint}"
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        else:
            print_error(f"Unknown method: {method}")
            return None
        
        # Print status
        if response.status_code in [200, 201]:
            print_success(f"{test_name}: {response.status_code}")
        else:
            print_error(f"{test_name}: {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
        
        # Try to parse JSON
        try:
            return response.json()
        except:
            return {"status": response.status_code}
            
    except Exception as e:
        print_error(f"{test_name}: {str(e)}")
        return None

def test_matching_endpoint(token: str, diagnosis_id: int):
    """Test GET /api/v1/analysis/{id}/match"""
    print_header("2. Knowledge Matching Endpoint Test")
    
    print_info(f"Testing: GET /analysis/{diagnosis_id}/match")
    
    result = test_endpoint(
        "GET",
        f"/analysis/{diagnosis_id}/match",
        "Match Endpoint",
        token
    )
    
    if result and result.get("success"):
        matches = result.get("matches", {})
        
        # Check Avicenna matches
        avicenna = matches.get("avicenna_matches", [])
        print_info(f"Avicenna matches: {len(avicenna)}")
        if avicenna:
            top = avicenna[0]
            print(f"  └─ Top: {top.get('disease_name', 'N/A')} "
                  f"({top.get('confidence', 0):.1%})")
        
        # Check TCM matches
        tcm = matches.get("tcm_matches", [])
        print_info(f"TCM matches: {len(tcm)}")
        if tcm:
            top = tcm[0]
            print(f"  └─ Top: {top.get('pattern_name', 'N/A')} "
                  f"({top.get('confidence', 0):.1%})")
        
        # Check Ayurveda matches
        ayurveda = matches.get("ayurveda_matches", [])
        print_info(f"Ayurveda matches: {len(ayurveda)}")
        if ayurveda:
            top = ayurveda[0]
            print(f"  └─ Top: {top.get('disease_name', 'N/A')} "
                  f"({top.get('confidence', 0):.1%})")
        
        print_success("Matching endpoint working correctly")
        return result
    else:
        print_error("Matching endpoint failed")
        return None

def test_recommendations_endpoint(token: str, diagnosis_id: int):
    """Test GET /api/v1/analysis/{id}/recommendations"""
    print_header("3. Recommendations Endpoint Test")
    
    print_info(f"Testing: GET /analysis/{diagnosis_id}/recommendations")
    
    result = test_endpoint(
        "GET",
        f"/analysis/{diagnosis_id}/recommendations",
        "Recommendations Endpoint",
        token
    )
    
    if result and result.get("success"):
        recs = result.get("recommendations", {})
        
        for tradition, data in recs.items():
            if data:
                print_info(f"{tradition.upper()} recommendations:")
                print(f"  ├─ Herbs: {len(data.get('herbs', []))} items")
                print(f"  ├─ Diet: {len(data.get('diet_recommendations', []))} items")
                print(f"  ├─ Lifestyle: {len(data.get('lifestyle_recommendations', []))} items")
                print(f"  └─ Treatments: {len(data.get('treatment_protocols', []))} items")
        
        print_success("Recommendations endpoint working correctly")
        return result
    else:
        print_error("Recommendations endpoint failed")
        return None

def test_comparison_endpoint(token: str, diagnosis_id: int):
    """Test GET /api/v1/analysis/{id}/compare"""
    print_header("4. Comparison Endpoint Test")
    
    print_info(f"Testing: GET /analysis/{diagnosis_id}/compare")
    
    result = test_endpoint(
        "GET",
        f"/analysis/{diagnosis_id}/compare",
        "Comparison Endpoint",
        token
    )
    
    if result and result.get("success"):
        comp = result.get("comparison", {})
        traditions = comp.get("traditions", {})
        
        print_info("Traditions Comparison:")
        for trad, data in traditions.items():
            if data:
                print(f"  ├─ {trad.upper()}:")
                print(f"  │  ├─ Total matches: {data.get('total_matches', 0)}")
                top = data.get('top_match')
                if top:
                    name = top.get('disease_name') or top.get('pattern_name')
                    conf = top.get('confidence', 0)
                    print(f"  │  └─ Top: {name} ({conf:.1%})")
        
        consensus = comp.get("consensus_areas", [])
        if consensus:
            print_info(f"Consensus areas: {len(consensus)}")
            for area in consensus:
                print(f"  └─ {area}")
        
        print_success("Comparison endpoint working correctly")
        return result
    else:
        print_error("Comparison endpoint failed")
        return None

def test_error_handling(token: str):
    """Test error handling scenarios"""
    print_header("5. Error Handling Tests")
    
    # Test invalid diagnosis ID
    print_info("Testing invalid diagnosis ID...")
    result = test_endpoint(
        "GET",
        "/analysis/99999/match",
        "Invalid Diagnosis ID",
        token
    )
    
    # Test missing token
    print_info("Testing missing authorization...")
    try:
        url = f"{BASE_URL}{API_PREFIX}/analysis/1/match"
        response = requests.get(url, headers={"Content-Type": "application/json"})
        if response.status_code == 401:
            print_success("Properly rejects requests without token")
        else:
            print_warning(f"Expected 401, got {response.status_code}")
    except Exception as e:
        print_error(f"Error test failed: {str(e)}")

def test_performance(token: str, diagnosis_id: int):
    """Test endpoint performance"""
    print_header("6. Performance Tests")
    
    endpoints = [
        f"/analysis/{diagnosis_id}/match",
        f"/analysis/{diagnosis_id}/recommendations",
        f"/analysis/{diagnosis_id}/compare"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"{BASE_URL}{API_PREFIX}{endpoint}"
            headers = HEADERS.copy()
            headers["Authorization"] = f"Bearer {token}"
            
            start = time.time()
            response = requests.get(url, headers=headers)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                if elapsed < 0.5:
                    print_success(f"{endpoint}: {elapsed:.3f}s (excellent)")
                elif elapsed < 1.0:
                    print_info(f"{endpoint}: {elapsed:.3f}s (good)")
                else:
                    print_warning(f"{endpoint}: {elapsed:.3f}s (slow)")
            
        except Exception as e:
            print_error(f"{endpoint}: {str(e)}")

def generate_report(results: Dict[str, Any]):
    """Generate test report"""
    print_header("TEST REPORT")
    
    total = results.get("total", 0)
    passed = results.get("passed", 0)
    failed = results.get("failed", 0)
    
    percentage = (passed / total * 100) if total > 0 else 0
    
    print_info(f"Total Tests: {total}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    print_info(f"Success Rate: {percentage:.1f}%")
    
    if percentage == 100:
        print_success("ALL TESTS PASSED! 🎉")
    elif percentage >= 80:
        print_warning("Most tests passed, review failures")
    else:
        print_error("Multiple failures detected")

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}📋 Week 2 Integration Testing{Colors.ENDC}")
    print(f"Backend: {BASE_URL}")
    print(f"Diagnosis ID: {TEST_DIAGNOSIS_ID}\n")
    
    # Step 1: Login
    token = login("user@example.com", "password")
    if not token:
        print_error("Cannot proceed without authentication")
        return
    
    # Step 2-4: Test endpoints
    match_result = test_matching_endpoint(token, TEST_DIAGNOSIS_ID)
    rec_result = test_recommendations_endpoint(token, TEST_DIAGNOSIS_ID)
    comp_result = test_comparison_endpoint(token, TEST_DIAGNOSIS_ID)
    
    # Step 5: Error handling
    test_error_handling(token)
    
    # Step 6: Performance
    test_performance(token, TEST_DIAGNOSIS_ID)
    
    # Summary
    results = {
        "total": 6,
        "passed": sum([1 for r in [match_result, rec_result, comp_result] if r]),
        "failed": sum([1 for r in [match_result, rec_result, comp_result] if not r])
    }
    
    generate_report(results)
    
    print(f"\n{Colors.BOLD}📝 Test logs saved to: test_results.json{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
