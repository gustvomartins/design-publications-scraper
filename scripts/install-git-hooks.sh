#!/bin/bash

# Script to install Git hooks for the Design Publications Scraper project

echo "🔧 Installing Git hooks for Design Publications Scraper..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit is not installed. Installing..."
    pip install pre-commit
fi

# Install pre-commit hooks
echo "📦 Installing pre-commit hooks..."
pre-commit install

# Create additional Git hooks if needed
echo "🔗 Setting up additional Git hooks..."

# Pre-commit hook for commit message format
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Check commit message format
commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"; then
    echo "❌ Invalid commit message format!"
    echo "   Use: <type>(<scope>): <description>"
    echo "   Types: feat, fix, docs, style, refactor, test, chore"
    echo "   Example: feat(core): add new transformer functionality"
    exit 1
fi
echo "✅ Commit message format is valid"
EOF

chmod +x .git/hooks/commit-msg

# Pre-push hook for running tests
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
echo "🧪 Running tests before push..."
if ! python -m pytest tests/unit/ --tb=short; then
    echo "❌ Tests failed! Push aborted."
    exit 1
fi
echo "✅ All tests passed!"
EOF

chmod +x .git/hooks/pre-push

echo "✅ Git hooks installed successfully!"
echo ""
echo "Available hooks:"
echo "  - pre-commit: Code formatting and linting"
echo "  - commit-msg: Commit message validation"
echo "  - pre-push: Test execution before push"
echo ""
echo "To skip hooks (not recommended):"
echo "  git commit --no-verify"
echo "  git push --no-verify"
