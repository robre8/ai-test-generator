import subprocess

from app.services.test_execution_service import _execute_in_docker


def test_execute_in_docker_returns_none_when_docker_missing(monkeypatch, tmp_path):
    def fake_run(*args, **kwargs):
        if args[0][:2] == ["docker", "--version"]:
            raise FileNotFoundError()
        return subprocess.CompletedProcess(args[0], 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = _execute_in_docker(str(tmp_path), str(tmp_path / "test_generated.py"))

    assert result is None
