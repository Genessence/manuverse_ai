@echo off
echo Starting React Development Server...
echo.

cd react-frontend

echo Checking if dependencies are installed...
if not exist "node_modules" (
    echo Dependencies not found. Running setup...
    call ..\setup_react.bat
)

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo.
echo Make sure the API server is running on http://localhost:8000
echo Use run_api.bat to start the API server
echo.
echo Press Ctrl+C to stop the development server
echo.

npm start
