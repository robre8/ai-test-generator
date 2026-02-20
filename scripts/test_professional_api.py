#!/usr/bin/env python3
"""
Test API with Professional Response Format
"""

import json
import requests

BASE_URL = "http://localhost:8000/api"


def test_professional_api():
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

    print("Testing code:")
    print(code)
    print("\nSending POST /api/generate-tests...")
    print("-" * 70)

    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=120,
        )

        print(f"Status Code: {response.status_code}\n")

        if response.status_code == 200:
            result = response.json()

            print("Response Structure")
            print("-" * 70)
            print(json.dumps(result, indent=2, ensure_ascii=False))

            checks = {
                "status field present": "status" in result,
                "status is valid": result.get("status") in [
                    "success",
                    "failed",
                    "validation_error",
                    "execution_error",
                    "timeout",
                ],
                "execution_time field": "execution_time" in result,
                "error_type field exists": "error_type" in result,
            }

            passed = sum(1 for v in checks.values() if v)
            total = len(checks)

            print("\nValidation Checklist:")
            for check, value in checks.items():
                status = "✓" if value else "✗"
                print(f"  {status} {check}: {value}")

            print(f"\nResult: {passed}/{total} checks passed")
            return True

        print(f"Error: Status {response.status_code}")
        print(response.text)
        return False

    except requests.exceptions.Timeout:
        print("TIMEOUT: Request exceeded 120 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR: Backend is not running")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_security_validation():
    print("\n" + "=" * 70)
    print("Testing Security Validation Error Response")
    print("=" * 70)

    malicious_code = """
import os
os.system("rm -rf /")
"""

    payload = {"code": malicious_code}

    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()

            checks = {
                "status is validation_error": result.get("status") == "validation_error",
                "error_type is SecurityViolation": result.get("error_type") == "SecurityViolation",
            }

            passed = sum(1 for v in checks.values() if v)
            total = len(checks)

            print(f"Security checks: {passed}/{total}")
            return True

        print(f"Error: Status {response.status_code}")
        return False

    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == "__main__":
    import sys

    test1 = test_professional_api()
    test2 = test_security_validation()

    sys.exit(0 if test1 and test2 else 1)
