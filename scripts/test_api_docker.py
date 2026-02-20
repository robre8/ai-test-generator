#!/usr/bin/env python3
"""
API integration test using Docker sandbox
"""

import requests

BASE_URL = "http://localhost:8000/api"


def test_api_with_docker_sandbox():
    code = """
def add(a, b):
    return a + b

def multiply(x, y):
    return x * y


def greet(name):
    return f"Hello, {name}!"
"""

    payload = {"code": code}

    print("=" * 60)
    print("Testing API with Docker Sandbox")
    print("=" * 60)
    print(f"\nCode:\n{code}")
    print("\nSending request to /api/generate-tests...")

    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=60,
        )

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            if result.get("error"):
                print(f"Error: {result.get('error')}")
                return False

            passed = result.get("passed", False)
            print(f"All tests passed: {passed}")

            return passed

        print(f"Failed with status {response.status_code}")
        print(f"Response: {response.text}")
        return False

    except requests.exceptions.Timeout:
        print("TIMEOUT: Request exceeded 60 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("CONNECTION ERROR: Could not connect to backend")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == "__main__":
    import sys

    success = test_api_with_docker_sandbox()
    sys.exit(0 if success else 1)
