@echo off
echo Setting up Multi-Agent Data Analysis System...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete! 
echo.
echo To run the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: streamlit run multi_agent_data_analysis.py
echo.
echo Note: The large mining database file is not included in the repository.
echo The app will work with sample data or your own uploaded files.
echo.
pause
