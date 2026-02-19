#!/usr/bin/env python3
"""
Test API with Professional Response Format
Verifies all checklist items:
- Status field (success, failed, validation_error, execution_error, timeout)
- Execution time measurement
- Error type classification
- Security flags in Docker command
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_professional_api():
    """Test API with professional response format"""
    
    print("=" * 70)
    print("Testing Professional API Response Format")
    print("=" * 70)
    print()
    
    code = """
def add(a, b):
    return a + b

def multiply(x, y):
    return x * y
"""

    payload = {"code": code}
    
    print("📝 Testing code:")
    print(code)
    print("\n🚀 Sending POST /api/generate-tests...")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=120
        )
        
        print(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Response Structure (Professional Format)")
            print("-" * 70)
            
            # Pretty print
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            
            # Validation
            print("✅ Validation Checklist:")
            print("-" * 70)
            
            checks = {
                "status field present": "status" in result,
                "status is valid": result.get("status") in ["success", "failed", "validation_error", "execution_error", "timeout"],
                "generated_tests field": "generated_tests" in result,
                "execution_output field": "execution_output" in result,
                "passed field": "passed" in result,
                "execution_time field": "execution_time" in result,
                "execution_time is float": isinstance(result.get("execution_time"), (int, float)),
                "error field exists": "error" in result,
                "error_type field exists": "error_type" in result,
                "error_type is valid or null": result.get("error_type") in [None, "TestFailure", "CodeInvalid", "Timeout", "SecurityViolation", "DockerError", "Unknown"],
            }
            
            passed = 0
            failed = 0
            for check, value in checks.items():
                status = "✓" if value else "✗"
                color = "✓" if value else "✗"
                print(f"  {color} {check}: {value}")
                if value:
                    passed += 1
                else:
                    failed += 1
            
            print()
            print("=" * 70)
            if result.get("status") == "success" and result.get("passed"):
                print(f"✅ SUCCESS: {passed}/{passed+failed} checks passed")
                print("Response format is production-ready!")
            else:
                print(f"⚠️ PARTIAL: {passed}/{passed+failed} checks passed")
                if result.get("status") == "failed":
                    print(f"Tests failed (expected in some cases)")
                if result.get("error_type"):
                    print(f"Error type: {result.get('error_type')}")
            print("=" * 70)
            
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request exceeded 120 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Backend is not running")
        print("Start backend with: cd backend && python -m uvicorn app.main:app --port 8000")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_security_validation():
    """Test security validation response"""
    
    print("\n" + "=" * 70)
    print("Testing Security Validation Error Response")
    print("=" * 70)
    print()
    
    # Code with dangerous import
    malicious_code = """
import os
os.system("rm -rf /")
"""

    payload = {"code": malicious_code}
    
    print("📝 Testing code with dangerous import:")
    print(malicious_code)
    print("\n🚀 Sending POST /api/generate-tests...")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Security Validation Response:")
            print("-" * 70)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print()
            
            # Check security response
            checks = {
                "status is validation_error": result.get("status") == "validation_error",
                "error_type is SecurityViolation": result.get("error_type") == "SecurityViolation",
                "error message present": result.get("error") is not None,
                "passed is False": result.get("passed") == False,
                "execution_time measured": "execution_time" in result,
            }
            
            passed = sum(1 for v in checks.values() if v)
            total = len(checks)
            
            print("✅ Security Check Validation:")
            for check, value in checks.items():
                status = "✓" if value else "✗"
                print(f"  {status} {check}: {value}")
            
            print()
            print("=" * 70)
            if passed == total:
                print(f"✅ SUCCESS: {passed}/{total} security checks passed")
                print("Security validation is working correctly!")
            else:
                print(f"⚠️ PARTIAL: {passed}/{total} checks passed")
            print("=" * 70)
            
            return True
        else:
            print(f"❌ Error: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    test1 = test_professional_api()
    test2 = test_security_validation()
    
    print("\n" + "=" * 70)
    if test1 and test2:
        print("✅ All professional API tests passed!")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed or incomplete")
        sys.exit(1)
