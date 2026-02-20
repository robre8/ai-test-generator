#!/usr/bin/env python3
"""
Manual security validation checks
"""

import sys

sys.path.insert(0, "backend")

from app.services.code_validator import get_safe_code_info

TEST_CASES = [
    ("Safe code", """
def add(a, b):
    return a + b
"""),
    ("Dangerous code - os", """
import os
os.system("ls")
"""),
    ("Dangerous code - subprocess", """
import subprocess
subprocess.call(["ls"])
"""),
]

for name, code in TEST_CASES:
    info = get_safe_code_info(code)
    print(f"\n{name}:")
    print(f"  Safe: {info['is_safe']}")
    if info["error_message"]:
        print(f"  Error: {info['error_message']}")
    if info["dangerous_items"]:
        print(f"  Dangerous items: {info['dangerous_items']}")
