# Design Publications Scraper - Project Structure

This document describes the clean and organized structure of the Design Publications Scraper repository.

## Repository Structure

```
design-publications-scraper/
├── src/                          # Source code directory
│   └── design_scraper/          # Main package
│       ├── __init__.py          # Package initialization
│       ├── core/                # Core application logic
│       │   ├── __init__.py
│       │   ├── main.py         # Main application entry point
│       │   └── pipeline.py     # Data processing pipeline
│       ├── scrapers/            # Web scraping modules
│       │   ├── __init__.py
│       │   ├── base_scraper.py # Base scraper class
│       │   ├── arcosdesign_scraper.py
│       │   ├── designetecnologia_scraper.py
│       │   ├── designtecnologiasociedade_scraper.py
│       │   ├── educacaografica_scraper.py
│       │   ├── estudosemdesign_scraper.py
│       │   ├── humanfactorsindesign_scraper.py
│       │   ├── infodesign_scraper.py
│       │   ├── poliedro_scraper.py
│       │   ├── projetica_scraper.py
│       │   ├── sbc_scraper.py
│       │   └── triades_scraper.py
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── data_transformer.py
│       │   ├── deduplication.py
│       │   ├── export_csv.py
│       │   ├── html_parsing.py
│       │   └── scrapers_factory.py
│       ├── processors/          # Data processing modules
│       │   ├── __init__.py
│       │   └── deduplicate.py
│       ├── config/              # Configuration files
│       │   └── config.yaml
│       └── cli/                 # Command-line interface (future)
│           └── __init__.py
├── data/                        # Data storage
│   ├── raw/                     # Raw scraped data
│   └── processed/               # Processed and cleaned data
├── tests/                       # Test suite
│   └── unit/                    # Unit tests
├── docs/                        # Documentation
├── examples/                    # Usage examples
├── scripts/                     # Utility scripts
├── logs/                        # Application logs
├── .github/                     # GitHub workflows and templates
├── .vscode/                     # VS Code configuration
├── run.py                       # Root-level entry point
├── setup.py                     # Package setup and installation
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Git ignore rules
```

## Key Improvements Made

### 1. **Consolidated Source Code**
- Moved all source code into `src/design_scraper/` package
- Eliminated duplicate directories (`utils/` and `scrapers/` at root level)
- Created proper Python package structure with `__init__.py` files

### 2. **Logical Organization**
- **Core**: Main application logic and pipeline
- **Scrapers**: Individual web scraping modules
- **Utils**: Utility functions and helper classes
- **Processors**: Data processing and transformation modules
- **Config**: Configuration files

### 3. **Clean Entry Points**
- `run.py`: Simple root-level entry point
- `setup.py`: Proper package installation
- Console script entry point: `design-scraper`

### 4. **Import Structure**
- All imports now use the proper package structure
- Clean separation of concerns
- Easy to maintain and extend

## Usage

### Running the Application
```bash
# From root directory
python run.py

# Or after installation
design-scraper
```

### Development Installation
```bash
pip install -e .
```

### Importing in Code
```python
from design_scraper.core import main, Pipeline
from design_scraper.scrapers import BaseScraper
from design_scraper.utils import DataTransformer
```

## Benefits of New Structure

1. **Professional**: Follows Python packaging best practices
2. **Maintainable**: Clear separation of concerns
3. **Installable**: Can be installed as a proper Python package
4. **Extensible**: Easy to add new scrapers and utilities
5. **Testable**: Proper structure for unit testing
6. **Documented**: Clear organization makes it easy to understand

## Migration Notes

- All existing functionality has been preserved
- Import paths have been updated to use the new structure
- The `run.py` script provides backward compatibility
- Existing data and configuration files remain in place
