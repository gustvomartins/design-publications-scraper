#!/usr/bin/env python3
"""
Entry point for the Design Publications Scraper application.
This script provides a clean interface to run the scraper from the root directory.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from design_scraper.core.main import main

if __name__ == "__main__":
    main()
