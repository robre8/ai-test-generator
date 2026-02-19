from .llm_service import generate_tests_from_code
from .test_execution_service import execute_tests
from .code_validator import validate_code_safety
import time

MAX_CODE_LENGTH = 5000

def process_code(code: str):
    start_time = time.time()
    
    try:
        # Validar tamaño
        if len(code) > MAX_CODE_LENGTH:
            return {
                "status": "validation_error",
                "generated_tests": "",
                "execution_output": "",
                "passed": False,
                "execution_time": round(time.time() - start_time, 2),
                "error": f"Código muy grande. Máximo: {MAX_CODE_LENGTH} caracteres, tienes: {len(code)}",
                "error_type": "CodeInvalid"
            }
        
        # Validar seguridad
        is_safe, message, dangerous_items = validate_code_safety(code)
        if not is_safe:
            return {
                "status": "validation_error",
                "generated_tests": "",
                "execution_output": "",
                "passed": False,
                "execution_time": round(time.time() - start_time, 2),
                "error": message,
                "error_type": "SecurityViolation"
            }

        # Generar tests
        tests = generate_tests_from_code(code)
        
        # Ejecutar tests
        execution_result = execute_tests(code, tests)

        # Determinar status basado en resultado
        if execution_result["error"]:
            if "Timeout" in execution_result["error"]:
                status = "timeout"
                error_type = "Timeout"
            else:
                status = "execution_error"
                error_type = "DockerError"
        elif execution_result["passed"]:
            status = "success"
            error_type = None
        else:
            status = "failed"
            error_type = "TestFailure"

        return {
            "status": status,
            "generated_tests": tests,
            "execution_output": execution_result["output"],
            "passed": execution_result["passed"],
            "execution_time": round(time.time() - start_time, 2),
            "error": execution_result["error"],
            "error_type": error_type
        }
    except Exception as e:
        return {
            "status": "execution_error",
            "generated_tests": "",
            "execution_output": "",
            "passed": False,
            "execution_time": round(time.time() - start_time, 2),
            "error": str(e),
            "error_type": "Unknown"
        }
