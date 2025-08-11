@echo off
echo Starting Full-Stack Multi-Agent Data Analysis Application
echo ========================================================
echo.

REM Start API server in background
echo [1/2] Starting API Server...
start "API Server" cmd /k "run_api.bat"
timeout /t 3 /nobreak >nul

echo [2/2] Starting React Frontend...
start "React Frontend" cmd /k "run_react.bat"

echo.
echo Both servers are starting...
echo.
echo API Server: http://localhost:8000
echo React Frontend: http://localhost:3000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press any key to close this window (servers will continue running)
pause >nul
