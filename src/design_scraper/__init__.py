"""
Design Publications Scraper

A comprehensive tool for scraping design-related publications from various sources.
"""

__version__ = "1.0.0"
__author__ = "Design Scraper Team"

from .core.main import main
from .core.pipeline import Pipeline

__all__ = ["main", "Pipeline"]
