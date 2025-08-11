@echo off
echo Setting up React Frontend...
echo.

cd react-frontend

echo Checking for Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Node.js found!
echo.

echo Installing dependencies...
npm install

if errorlevel 1 (
    echo Error installing dependencies!
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo To start the React development server, run:
echo   cd react-frontend
echo   npm start
echo.
echo Or use the provided batch file:
echo   run_react.bat
echo.
pause
