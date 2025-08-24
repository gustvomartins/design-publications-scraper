#!/bin/bash

# Script to set up Python virtual environment for Design Publications Scraper

echo "🐍 Setting up Python virtual environment for Design Publications Scraper..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is too old. Please install Python $required_version+ first."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
if [ -d "venv" ]; then
    echo "⚠️ Virtual environment already exists. Removing..."
    rm -rf venv
fi

echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "📥 Installing package in development mode..."
pip install -e .

# Install development dependencies
echo "🔧 Installing development dependencies..."
pip install -e ".[dev]"

# Install pre-commit hooks
echo "📦 Installing pre-commit hooks..."
pre-commit install

echo ""
echo "✅ Virtual environment setup completed!"
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate  # Linux/Mac"
echo "  venv\\Scripts\\activate     # Windows"
echo ""
echo "To deactivate:"
echo "  deactivate"
echo ""
echo "Available commands:"
echo "  make help                 # Show available make commands"
echo "  make test                 # Run tests"
echo "  make format               # Format code"
echo "  make lint                 # Run linting"
echo "  design-scraper --help    # Show CLI help"
echo ""
echo "Happy coding! 🚀"
