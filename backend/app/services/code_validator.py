import ast
import re
from typing import Tuple, List

# Módulos y funciones peligrosas
DANGEROUS_MODULES = {
    'os': 'Sistema operativo (ejecución de comandos)',
    'subprocess': 'Ejecución de procesos',
    'sys': 'Parámetros del sistema',
    'shutil': 'Operaciones de archivos',
    'pathlib': 'Rutas del sistema',
    'importlib': 'Importación dinámica',
    '__import__': 'Importación dinámica',
    'eval': 'Evaluación de código',
    'exec': 'Ejecución de código',
    'compile': 'Compilación de código',
    'open': 'Manejo de archivos',
    'input': 'Entrada de usuario',
    'socket': 'Conexiones de red',
    'requests': 'Solicitudes HTTP',
    'urllib': 'Acceso a URLs',
}

DANGEROUS_PATTERNS = [
    r'__import__',
    r'__\w+__',  # Acceso a atributos mágicos
    r'eval\s*\(',
    r'exec\s*\(',
    r'compile\s*\(',
    r'open\s*\(',
    r'\.system\(',
    r'\.popen\(',
    r'\.call\(',
    r'\.run\(',
]

def validate_code_safety(code: str) -> Tuple[bool, str, List[str]]:
    """
    Valida que el código no contenga operaciones peligrosas.
    
    Returns:
        Tuple[bool, str, List[str]]: (is_safe, message, dangerous_items)
            - is_safe: True si el código es seguro
            - message: Mensaje de error si no es seguro
            - dangerous_items: Lista de items peligrosos encontrados
    """
    dangerous_items = []
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return True, "", []  # Dejar que pytest reporte errores de sintaxis
    
    # 1. Verificar imports peligrosos
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name.split('.')[0]
                if module_name in DANGEROUS_MODULES:
                    dangerous_items.append(f"import {module_name}")
        
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module.split('.')[0] if node.module else ""
            if module_name in DANGEROUS_MODULES:
                dangerous_items.append(f"from {module_name} import ...")
    
    # 2. Verificar patrones peligrosos en el código fuente
    for pattern in DANGEROUS_PATTERNS:
        matches = re.findall(pattern, code)
        if matches:
            for match in matches:
                dangerous_items.append(match)
    
    if dangerous_items:
        items_str = ", ".join(f"'{item}'" for item in dangerous_items)
        message = f"Código contiene operaciones peligrosas: {items_str}. "
        message += "No se permite: os, subprocess, sys, open(), eval(), exec(), compiling code, network access."
        return False, message, dangerous_items
    
    return True, "", []


def get_safe_code_info(code: str) -> dict:
    """
    Analiza el código y devuelve información sobre su seguridad.
    """
    is_safe, message, dangerous_items = validate_code_safety(code)
    
    try:
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    except:
        functions = []
        classes = []
    
    return {
        "is_safe": is_safe,
        "error_message": message,
        "dangerous_items": dangerous_items,
        "functions": functions,
        "classes": classes,
        "code_length": len(code)
    }
