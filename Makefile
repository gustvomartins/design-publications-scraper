.PHONY: help install install-dev install-docs test test-unit test-integration lint format clean docs build install-hooks

# Default target
help:
	@echo "Design Publications Scraper - Development Commands"
	@echo "================================================"
	@echo ""
	@echo "Installation:"
	@echo "  install        Install the package in development mode"
	@echo "  install-dev    Install with development dependencies"
	@echo "  install-docs   Install with documentation dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test           Run all tests"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-cov       Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with Black"
	@echo "  type-check     Run type checking with MyPy"
	@echo ""
	@echo "Documentation:"
	@echo "  docs           Build documentation"
	@echo "  docs-serve     Serve documentation locally"
	@echo ""
	@echo "Development:"
	@echo "  install-hooks  Install pre-commit hooks"
	@echo "  clean          Clean build artifacts"
	@echo "  build          Build distribution packages"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-docs:
	pip install -e ".[docs]"

# Testing
test:
	pytest

test-unit:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-cov:
	pytest --cov=src/design_scraper --cov-report=html --cov-report=term

# Code Quality
lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

# Documentation
docs:
	cd docs/api && make html

docs-serve:
	cd docs/api/_build/html && python -m http.server 8000

# Development
install-hooks:
	pre-commit install

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

# Quick development workflow
dev: install-dev install-hooks
	@echo "Development environment ready!"
	@echo "Run 'make test' to test your changes"
	@echo "Run 'make format' to format your code"
	@echo "Run 'make lint' to check code quality"

# CI/CD pipeline
ci: lint type-check test
	@echo "All CI checks passed!"

# Release preparation
release: clean build test
	@echo "Release build completed successfully!"
