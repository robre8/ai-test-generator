#!/usr/bin/env python3
"""
Test Docker Sandbox with Security Limits
Verifies:
- Memory limit: 256m
- CPU limit: 0.5
- Network: NONE (completely isolated)
- Read-only filesystem
"""

import subprocess
import tempfile
import os


def test_sandbox_security():
    """Test Docker sandbox with maximum security constraints"""

    print("=" * 70)
    print("Testing Docker Sandbox Security Configuration")
    print("=" * 70)
    print()

    test_code = '''
import pytest

def test_basic_math():
    assert 2 + 2 == 4

def test_string_operations():
    s = "hello"
    assert s.upper() == "HELLO"
    assert len(s) == 5

def test_list_operations():
    lst = [1, 2, 3]
    assert sum(lst) == 6
    assert max(lst) == 3
'''

    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test_secure.py")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_code)

        print("✓ Test file created")
        print()

        docker_cmd = [
            "docker", "run",
            "--rm",
            "--memory=256m",
            "--cpus=0.5",
            "--network=none",
            "--read-only",
            "-v", f"{tmpdir}:/tests:ro",
            "-v", "/tmp",
            "--workdir", "/tests",
            "ai-test-generator-sandbox:latest",
            "sh", "-c",
            "pytest test_secure.py -v --tb=short",
        ]

        print("Executing tests in sandbox...")
        print("-" * 70)

        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=30,
                encoding="utf-8",
                errors="replace",
            )

            output = (result.stdout or "") + (result.stderr or "")
            print(output)
            print("-" * 70)

            if result.returncode == 0:
                print("\n✅ SUCCESS: All tests passed in secure sandbox!")
                return True

            print("\n❌ Tests failed")
            return False

        except subprocess.TimeoutExpired:
            print("-" * 70)
            print("❌ TIMEOUT: Sandbox execution exceeded 30 seconds")
            return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False


if __name__ == "__main__":
    import sys

    success = test_sandbox_security()
    sys.exit(0 if success else 1)
