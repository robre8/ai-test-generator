#!/usr/bin/env python
"""
Test security validation
"""
import os
import sys

sys.path.insert(0, r"d:\python projects\ai-test-generator\backend")

from dotenv import load_dotenv
load_dotenv(r"d:\python projects\ai-test-generator\backend\.env")

from app.services.code_validator import validate_code_safety, get_safe_code_info

test_cases = [
    ("Código seguro", """
def add(a, b):
    return a + b
"""),
    ("Código peligroso - os", """
import os
os.system("ls")

def add(a, b):
    return a + b
"""),
    ("Código peligroso - subprocess", """
import subprocess
subprocess.call(["ls"])
"""),
    ("Código peligroso - open", """
with open('/etc/passwd') as f:
    data = f.read()
"""),
    ("Código peligroso - eval", """
code = input("Enter code: ")
eval(code)
"""),
    ("Clase segura", """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
"""),
]

print("=" * 80)
print("SECURITY VALIDATION TESTS")
print("=" * 80)

for name, code in test_cases:
    print(f"\n{name}:")
    print("-" * 80)
    info = get_safe_code_info(code)
    
    print(f"✅ Safe: {info['is_safe']}")
    if info['error_message']:
        print(f"❌ Error: {info['error_message']}")
    if info['dangerous_items']:
        print(f"⚠️  Dangerous items: {info['dangerous_items']}")
    if info['functions']:
        print(f"📝 Functions: {info['functions']}")
    if info['classes']:
        print(f"🏢 Classes: {info['classes']}")
    print(f"📏 Code length: {info['code_length']} chars")
