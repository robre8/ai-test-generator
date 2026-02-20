from app.services.code_validator import validate_code_safety


def test_validate_code_safety_blocks_dangerous_imports():
    code = "import os\nos.system('ls')"
    is_safe, message, items = validate_code_safety(code)

    assert is_safe is False
    assert "import os" in items
    assert "peligrosas" in message


def test_validate_code_safety_allows_safe_code():
    code = "def add(a, b):\n    return a + b"
    is_safe, message, items = validate_code_safety(code)

    assert is_safe is True
    assert message == ""
    assert items == []
