"""
Design Publications Scraper

Sistema de scraping e catalogação de publicações de design e UX
com filtragem inteligente para curadoria.
"""

__version__ = "1.0.0"
__author__ = "Design Publications Team"
__email__ = "team@design-publications.com"

from .core.pipeline import Pipeline
from .core.transformer import DataTransformer
from .core.filter import ContentFilter

__all__ = [
    "Pipeline",
    "DataTransformer", 
    "ContentFilter",
    "__version__",
    "__author__",
    "__email__",
]
