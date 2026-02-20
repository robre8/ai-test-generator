from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import tempfile
import os
import uuid
import shutil

app = FastAPI(title="AI Test Sandbox Service", version="1.0.0")


class ExecutionRequest(BaseModel):
    code: str
    tests: str


class ExecutionResponse(BaseModel):
    output: str
    passed: bool
    error: Optional[str] = None
    sandbox: str


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5,
        )
        docker_available = result.returncode == 0
        return {"status": "healthy", "docker_available": docker_available}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/execute", response_model=ExecutionResponse)
def execute_tests(request: ExecutionRequest):
    """Execute tests in isolated Docker sandbox"""
    temp_dir = tempfile.gettempdir()
    folder_name = os.path.join(temp_dir, f"test_run_{uuid.uuid4().hex}")
    os.makedirs(folder_name, exist_ok=True)

    try:
        code_path = os.path.join(folder_name, "user_code.py")
        test_path = os.path.join(folder_name, "test_generated.py")

        with open(code_path, "w", encoding="utf-8") as f:
            f.write(request.code)

        with open(test_path, "w", encoding="utf-8") as f:
            f.write(request.tests)

        # Docker command with security constraints
        docker_cmd = [
            "docker", "run",
            "--rm",
            "--memory=256m",
            "--cpus=0.5",
            "--network=none",
            "--read-only",
            "-v", f"{folder_name}:/tests:ro",
            "-v", "/tmp",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "--pids-limit=64",
            "--workdir", "/tests",
            "ai-test-sandbox:latest",
            "sh", "-c",
            "pytest test_generated.py -v --tb=short",
        ]

        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=15,
            encoding="utf-8",
            errors="replace",
        )

        passed = result.returncode == 0
        output = (result.stdout or "") + (result.stderr or "")

        # Clean pip warnings
        output = "\n".join(
            [line for line in output.split("\n") if "WARNING" not in line or "pytest" in line]
        )

        return ExecutionResponse(
            output=output,
            passed=passed,
            error=None,
            sandbox="docker",
        )

    except subprocess.TimeoutExpired:
        return ExecutionResponse(
            output="",
            passed=False,
            error="Timeout: execution exceeded 15 seconds",
            sandbox="docker",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
    finally:
        shutil.rmtree(folder_name, ignore_errors=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
