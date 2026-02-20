#!/usr/bin/env python3
"""
Validate TestResponse schema and conversion output
"""

import json
import sys

sys.path.insert(0, "backend")

from app.schemas.test_schema import TestResponse
from app.services.test_generation_service import process_code

print("=" * 70)
print("Testing TestResponse Validation")
print("=" * 70)

result_dict = process_code("def hello(): return 'hi'")

try:
    test_response = TestResponse.model_validate(result_dict)
    print("Validation successful")
    print(json.dumps(test_response.model_dump(), indent=2))
except Exception as e:
    print(f"Validation failed: {e}")
    print(json.dumps(result_dict, indent=2, default=str))
