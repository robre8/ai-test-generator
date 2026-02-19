import subprocess
import tempfile
import shutil
import os
import uuid

def execute_tests_in_sandbox(code: str, tests: str):
    """
    Ejecuta tests en un contenedor Docker aislado.
    Esto proporciona una capa extra de seguridad.
    """
    temp_dir = tempfile.gettempdir()
    folder_name = os.path.join(temp_dir, f"test_run_{uuid.uuid4().hex}")
    os.makedirs(folder_name, exist_ok=True)

    try:
        code_path = os.path.join(folder_name, "user_code.py")
        test_path = os.path.join(folder_name, "test_generated.py")

        with open(code_path, "w") as f:
            f.write(code)

        with open(test_path, "w") as f:
            f.write(tests)

        # Intentar ejecutar en Docker si está disponible
        try:
            docker_result = _execute_in_docker(folder_name, test_path)
            if docker_result is not None:
                return docker_result
        except Exception as docker_error:
            # Si Docker falla, caer a ejecución local
            pass

        # Fallback a ejecución local
        result = subprocess.run(
            ["pytest", test_path, "-v", "--tb=short"],
            cwd=folder_name,
            capture_output=True,
            text=True,
            timeout=10
        )

        passed = result.returncode == 0

        return {
            "output": result.stdout + result.stderr,
            "passed": passed,
            "error": None,
            "sandbox": "local"
        }

    except Exception as e:
        return {
            "output": "",
            "passed": False,
            "error": str(e),
            "sandbox": "local"
        }

    finally:
        shutil.rmtree(folder_name, ignore_errors=True)


def _execute_in_docker(folder_name: str, test_path: str):
    """
    Ejecuta pytest dentro de un contenedor Docker con límites de recursos.
    Usa imagen personalizada con pytest pre-instalado para máxima seguridad.
    
    Security Features:
    - Memory limit: 256MB (previene DoS por memoria)
    - CPU limit: 0.5 (previene DoS por CPU)
    - Network: NONE (sin acceso a conexiones externas)
    - Read-only filesystem (código del usuario no puede modificarse)
    - Timeout: 15 segundos máximo
    
    Returns:
        dict: Resultado de ejecución o None si Docker no está disponible
    """
    
    # Verificar si Docker está disponible
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True, timeout=5)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None
    
    try:
        test_relative = os.path.basename(test_path)
        
        # En Docker for Windows, las rutas de Windows funcionan directamente
        docker_folder = folder_name
        
        # Intentar usar imagen personalizada con pytest pre-instalado
        # Si no existe, fallback a python:3.11-slim sin network
        docker_image = "ai-test-generator-sandbox:latest"
        
        # Verificar si la imagen existe
        image_check = subprocess.run(
            ["docker", "inspect", docker_image],
            capture_output=True,
            timeout=5
        )
        
        if image_check.returncode != 0:
            # Imagen personalizada no disponible, usar python:3.11-slim
            docker_image = "python:3.11-slim"
            # Instalar pytest en el mismo paso (requiere network temporal)
            installation_step = "pip install pytest --no-cache-dir -q && "
        else:
            # Imagen personalizada disponible, pytest ya está instalado
            installation_step = ""
        
        # Comando Docker con máxima seguridad (Nivel Producción)
        docker_cmd = [
            "docker", "run",
            "--rm",
            "--memory=256m",           # Límite de memoria (previene DoS)
            "--cpus=0.5",              # Límite de CPU (previene DoS)
            "--network=none",          # CRÍTICO: sin conexiones externas
            "--read-only",             # Sistema de archivos read-only
            "--cap-drop=ALL",          # Drop todas las capabilities
            "--security-opt=no-new-privileges",  # Previene privilege escalation
            "--pids-limit=64",         # Limita procesos (previene fork bomb)
            "-v", f"{docker_folder}:/tests:ro",  # Código read-only
            "--workdir", "/tests",
            "-v", "/tmp",              # Temp storage (writable)
            docker_image,
            "sh", "-c",
            f"{installation_step}pytest {test_relative} -v --tb=short"
        ]
        
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=15,
            encoding='utf-8',
            errors='replace'
        )

        passed = result.returncode == 0

        # Limpiar output de pip warnings
        output = (result.stdout or "") + (result.stderr or "")
        output = "\n".join([l for l in output.split("\n") 
                           if "WARNING" not in l or "pytest" in l])

        return {
            "output": output,
            "passed": passed,
            "error": None,
            "sandbox": "docker"
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "passed": False,
            "error": "Timeout: Ejecución excedió 15 segundos",
            "sandbox": "docker"
        }
    except Exception as e:
        # Si algo falla en Docker, retornar None para usar fallback local
        return None


def execute_tests(code: str, tests: str):
    """
    Ejecuta tests con sandboxing. Intenta Docker primero, cae a local si no disponible.
    """
    return execute_tests_in_sandbox(code, tests)
