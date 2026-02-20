import os
import httpx

SANDBOX_SERVICE_URL = os.getenv("SANDBOX_SERVICE_URL", "http://localhost:8001")


def execute_tests(code: str, tests: str):
    """Execute tests in remote sandbox service"""
    try:
        # Call remote sandbox service
        with httpx.Client(timeout=20.0) as client:
            response = client.post(
                f"{SANDBOX_SERVICE_URL}/execute",
                json={"code": code, "tests": tests},
            )
            response.raise_for_status()
            result = response.json()

        return {
            "output": result.get("output", ""),
            "passed": result.get("passed", False),
            "error": result.get("error"),
            "sandbox": result.get("sandbox", "remote"),
        }

    except httpx.TimeoutException:
        return {
            "output": "",
            "passed": False,
            "error": "Sandbox service timeout (20s exceeded)",
            "sandbox": "error",
        }
    except httpx.RequestError as e:
        return {
            "output": "",
            "passed": False,
            "error": f"Failed to connect to sandbox service: {str(e)}",
            "sandbox": "error",
        }
    except Exception as e:
        return {
            "output": "",
            "passed": False,
            "error": f"Unexpected error: {str(e)}",
            "sandbox": "error",
        }
