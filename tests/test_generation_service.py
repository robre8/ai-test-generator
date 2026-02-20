from app.services import test_generation_service as tgs


def test_process_code_rejects_large_input():
    large_code = "a" * (tgs.MAX_CODE_LENGTH + 1)
    result = tgs.process_code(large_code)

    assert result["status"] == "validation_error"
    assert result["error_type"] == "CodeInvalid"


def test_process_code_rejects_security_violation(monkeypatch):
    monkeypatch.setattr(tgs, "validate_code_safety", lambda code: (False, "bad", ["import os"]))

    result = tgs.process_code("import os")

    assert result["status"] == "validation_error"
    assert result["error_type"] == "SecurityViolation"


def test_process_code_timeout(monkeypatch):
    monkeypatch.setattr(tgs, "validate_code_safety", lambda code: (True, "", []))
    monkeypatch.setattr(tgs, "generate_tests_from_code", lambda code: "def test_ok():\n    assert True")
    monkeypatch.setattr(tgs, "execute_tests", lambda code, tests: {
        "output": "",
        "passed": False,
        "error": "Timeout: exceeded",
    })

    result = tgs.process_code("def add(a, b): return a + b")

    assert result["status"] == "timeout"
    assert result["error_type"] == "Timeout"


def test_process_code_success(monkeypatch):
    monkeypatch.setattr(tgs, "validate_code_safety", lambda code: (True, "", []))
    monkeypatch.setattr(tgs, "generate_tests_from_code", lambda code: "def test_ok():\n    assert True")
    monkeypatch.setattr(tgs, "execute_tests", lambda code, tests: {
        "output": "ok",
        "passed": True,
        "error": None,
    })

    result = tgs.process_code("def add(a, b): return a + b")

    assert result["status"] == "success"
    assert result["error_type"] is None
