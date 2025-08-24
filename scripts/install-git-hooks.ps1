# Script to install Git hooks for the Design Publications Scraper project (PowerShell)

Write-Host "🔧 Installing Git hooks for Design Publications Scraper..." -ForegroundColor Green

# Check if pre-commit is installed
try {
    python -c "import pre_commit" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "pre_commit not found"
    }
} catch {
    Write-Host "❌ pre-commit is not installed. Installing..." -ForegroundColor Yellow
    pip install pre-commit
}

# Install pre-commit hooks
Write-Host "📦 Installing pre-commit hooks..." -ForegroundColor Green
pre-commit install

Write-Host "✅ Git hooks installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Available hooks:" -ForegroundColor Cyan
Write-Host "  - pre-commit: Code formatting and linting" -ForegroundColor White
Write-Host ""
Write-Host "To skip hooks (not recommended):" -ForegroundColor Yellow
Write-Host "  git commit --no-verify" -ForegroundColor White
Write-Host "  git push --no-verify" -ForegroundColor White

Read-Host "Press Enter to continue"
