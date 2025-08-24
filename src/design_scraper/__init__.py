"""
Design Publications Scraper

A comprehensive tool for scraping design-related publications from various sources.
"""

__version__ = "1.0.0"
__author__ = "Design Scraper Team"

from .core.pipeline import Pipeline
from .core.automated_pipeline import AutomatedPipeline
from .core.manual_search import ManualSearch

__all__ = ["Pipeline", "AutomatedPipeline", "ManualSearch"]
