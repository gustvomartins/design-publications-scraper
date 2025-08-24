@echo off
REM Script to set up Python virtual environment for Design Publications Scraper (Windows Command Prompt)

echo 🐍 Setting up Python virtual environment for Design Publications Scraper...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Create virtual environment
if exist "venv" (
    echo ⚠️ Virtual environment already exists. Removing...
    rmdir /s /q "venv"
)

echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call "venv\Scripts\activate.bat"

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install the package in development mode
echo 📥 Installing package in development mode...
pip install -e .

REM Install development dependencies
echo 🔧 Installing development dependencies...
pip install -e ".[dev]"

REM Install pre-commit hooks
echo 📦 Installing pre-commit hooks...
pre-commit install

echo.
echo ✅ Virtual environment setup completed!
echo.
echo To activate the environment:
echo   venv\Scripts\activate.bat  # Command Prompt
echo   venv\Scripts\Activate.ps1  # PowerShell
echo.
echo To deactivate:
echo   deactivate
echo.
echo Available commands:
echo   make help                 # Show available make commands
echo   make test                 # Run tests
echo   make format               # Format code
echo   make lint                 # Run linting
echo   design-scraper --help    # Show CLI help
echo.
echo Happy coding! 🚀

pause
