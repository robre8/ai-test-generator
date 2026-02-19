#!/usr/bin/env python3
"""
Prueba de integración del API con Docker sandbox
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_with_docker_sandbox():
    """Test API with Docker sandbox"""
    
    # Código simple para probar
    code = """
def add(a, b):
    return a + b

def multiply(x, y):
    return x * y

def greet(name):
    return f"Hello, {name}!"
"""

    payload = {
        "code": code
    }
    
    print("=" * 60)
    print("Testing API with Docker Sandbox")
    print("=" * 60)
    print(f"\n📝 Code:\n{code}")
    print("\n🚀 Sending request to /api/generate-tests...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-tests",
            json=payload,
            timeout=60
        )
        
        print(f"✓ Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Response received!")
            
            if result.get('error'):
                print(f"\n❌ Error: {result.get('error')}")
                return False
            
            tests = result.get('generated_tests', '')
            output = result.get('execution_output', '')
            passed = result.get('passed', False)
            
            if tests:
                print(f"\n✅ Generated {len(tests.split('def '))} tests")
                tests_preview = '\n'.join(tests.split('\n')[:10])
                print(f"Preview:\n{tests_preview}...")
            
            if output:
                # Extract just the summary line
                summary_lines = [l for l in output.split('\n') if 'passed' in l.lower() or 'failed' in l.lower()]
                if summary_lines:
                    print(f"\n✅ Execution Output: {summary_lines[-1]}")
            
            print(f"\n✅ All tests passed: {passed}")
            
            return passed
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request exceeded 60 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Could not connect to backend")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_api_with_docker_sandbox()
    sys.exit(0 if success else 1)
