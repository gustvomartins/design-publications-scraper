"""
Core functionality for the Design Publications Scraper.

This module contains the main components:
- Pipeline: Main orchestration logic
- DataTransformer: Data structure transformation
- ContentFilter: Content filtering and curation
"""

from .pipeline import Pipeline
from .transformer import DataTransformer
from .filter import ContentFilter

__all__ = ["Pipeline", "DataTransformer", "ContentFilter"]
