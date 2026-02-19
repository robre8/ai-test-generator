@echo off
REM Build the sandbox Docker image with pytest pre-installed

echo.
echo ========================================
echo Building Docker Sandbox Image
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH
    echo Please install Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo.
echo [1/2] Building image: ai-test-generator-sandbox:latest
echo This may take a few minutes on first run...
echo.

docker build -t ai-test-generator-sandbox:latest -f Dockerfile.sandbox .

if errorlevel 1 (
    echo.
    echo Error: Failed to build Docker image
    pause
    exit /b 1
)

echo.
echo [2/2] Verifying image...
docker inspect ai-test-generator-sandbox:latest >nul 2>&1

if errorlevel 1 (
    echo.
    echo Error: Image build failed verification
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ Success! Image built successfully
echo ========================================
echo.
echo Image details:
docker images ai-test-generator-sandbox:latest
echo.
echo Next steps:
echo 1. Start the backend: python -m uvicorn app.main:app --port 8000
echo 2. Tests will now use the optimized sandbox image
echo.
pause
