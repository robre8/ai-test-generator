from fastapi.testclient import TestClient

from app.main import app
from app.api import routes


def test_generate_tests_route_success(monkeypatch):
    def fake_process(code: str):
        return {
            "status": "success",
            "generated_tests": "def test_ok():\n    assert True",
            "execution_output": "ok",
            "passed": True,
            "execution_time": 0.1,
            "error": None,
            "error_type": None,
        }

    monkeypatch.setattr(routes, "process_code", fake_process)

    client = TestClient(app)
    response = client.post("/api/generate-tests", json={"code": "def add(a,b): return a+b"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["passed"] is True
    assert data["error"] is None


def test_validate_code_route_safe(monkeypatch):
    def fake_info(code: str):
        return {
            "is_safe": True,
            "error_message": None,
            "dangerous_items": [],
            "functions": ["add"],
            "classes": [],
            "code_length": len(code),
        }

    monkeypatch.setattr(routes, "get_safe_code_info", fake_info)

    client = TestClient(app)
    response = client.post("/api/validate-code", json={"code": "def add(a,b): return a+b"})

    assert response.status_code == 200
    data = response.json()
    assert data["is_safe"] is True
    assert data["functions"] == ["add"]
