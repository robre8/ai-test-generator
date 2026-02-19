#!/usr/bin/env python3
"""
Test to verify TestResponse validation works correctly
"""
import sys
sys.path.insert(0, 'backend')

from app.schemas.test_schema import TestResponse
from app.services.test_generation_service import process_code

print("=" * 70)
print("Testing TestResponse Validation")
print("=" * 70)
print()

# Call process_code
print("1. Calling process_code with simple code...")
result_dict = process_code("def hello(): return 'hi'")

print(f"\n2. process_code returned dict with keys: {list(result_dict.keys())}")
print()

# Try to validate with Pydantic
print("3. Validating with TestResponse model...")
try:
    test_response = TestResponse.model_validate(result_dict)
    print("✅ Validation successful!")
    print()
    print(f"   status: {test_response.status}")
    print(f"   passed: {test_response.passed}")
    print(f"   execution_time: {test_response.execution_time}")
    print(f"   error_type: {test_response.error_type}")
    print(f"   error message: {test_response.error}")
    print()
    
    # Convert to JSON (what FastAPI does)
    print("4. Converting to JSON (FastAPI format)...")
    json_dict = test_response.model_dump()
    print(f"   JSON keys: {list(json_dict.keys())}")
    print()
    
    import json
    json_str = test_response.model_dump_json()
    print("5. JSON output:")
    print(json.dumps(json.loads(json_str), indent=2))
    
except Exception as e:
    print(f"❌ Validation failed: {e}")
    print()
    print("Dict keys from process_code:", list(result_dict.keys()))
    print("Dict content:")
    import json
    print(json.dumps(result_dict, indent=2, default=str))
