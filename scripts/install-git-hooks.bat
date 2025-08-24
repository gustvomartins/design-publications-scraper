@echo off
REM Script to install Git hooks for the Design Publications Scraper project (Windows)

echo 🔧 Installing Git hooks for Design Publications Scraper...

REM Check if pre-commit is installed
python -c "import pre_commit" >nul 2>&1
if errorlevel 1 (
    echo ❌ pre-commit is not installed. Installing...
    pip install pre-commit
)

REM Install pre-commit hooks
echo 📦 Installing pre-commit hooks...
pre-commit install

echo ✅ Git hooks installed successfully!
echo.
echo Available hooks:
echo   - pre-commit: Code formatting and linting
echo.
echo To skip hooks (not recommended):
echo   git commit --no-verify
echo   git push --no-verify

pause
