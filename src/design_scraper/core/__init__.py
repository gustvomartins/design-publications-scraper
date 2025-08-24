"""
Core functionality for the Design Publications Scraper.
"""

from .pipeline import Pipeline
from .automated_pipeline import AutomatedPipeline
from .manual_search import ManualSearch

__all__ = ["Pipeline", "AutomatedPipeline", "ManualSearch"]
