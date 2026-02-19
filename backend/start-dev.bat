@echo off
REM Start backend development server

if not exist ".env" (
    echo Error: .env file not found!
    echo Please create it from .env.example and add your GROQ_API_KEY
    pause
    exit /b 1
)

echo Starting FastAPI backend...
echo.
echo 🚀 Backend running at http://localhost:8000
echo 📖 Docs at http://localhost:8000/docs
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
