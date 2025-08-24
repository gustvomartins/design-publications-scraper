# Script to set up Python virtual environment for Design Publications Scraper (Windows)

Write-Host "🐍 Setting up Python virtual environment for Design Publications Scraper..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH. Please install Python 3.8+ first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python version
$versionOutput = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Could not determine Python version" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$requiredVersion = "3.8"
if ([version]$versionOutput -lt [version]$requiredVersion) {
    Write-Host "❌ Python $versionOutput is too old. Please install Python $requiredVersion+ first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "⚠️ Virtual environment already exists. Removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

Write-Host "📦 Creating virtual environment..." -ForegroundColor Green
python -m venv venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "⬆️ Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install the package in development mode
Write-Host "📥 Installing package in development mode..." -ForegroundColor Green
pip install -e .

# Install development dependencies
Write-Host "🔧 Installing development dependencies..." -ForegroundColor Green
pip install -e ".[dev]"

# Install pre-commit hooks
Write-Host "📦 Installing pre-commit hooks..." -ForegroundColor Green
pre-commit install

Write-Host ""
Write-Host "✅ Virtual environment setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment:" -ForegroundColor Cyan
Write-Host "  venv\Scripts\Activate.ps1  # PowerShell" -ForegroundColor White
Write-Host "  venv\Scripts\activate.bat  # Command Prompt" -ForegroundColor White
Write-Host ""
Write-Host "To deactivate:" -ForegroundColor Cyan
Write-Host "  deactivate" -ForegroundColor White
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  make help                 # Show available make commands" -ForegroundColor White
Write-Host "  make test                 # Run tests" -ForegroundColor White
Write-Host "  make format               # Format code" -ForegroundColor White
Write-Host "  make lint                 # Run linting" -ForegroundColor White
Write-Host "  design-scraper --help    # Show CLI help" -ForegroundColor White
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Green

Read-Host "Press Enter to continue"
