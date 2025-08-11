@echo off
echo Starting Multi-Agent Data Analysis API Server...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing API dependencies...
    pip install -r api_requirements.txt
    pip install -r requirements.txt
)

echo.
echo Installing/Updating API dependencies...
pip install -r api_requirements.txt

echo.
echo Starting FastAPI server on http://localhost:8000
echo API Documentation available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn api_backend:app --host 0.0.0.0 --port 8000 --reload
