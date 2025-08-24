"""
Configuration management for the Design Publications Scraper.

This module handles:
- Loading configuration from YAML files
- Default configuration values
- Configuration validation
"""

from .config_manager import ConfigManager
from .defaults import DEFAULT_CONFIG

__all__ = ["ConfigManager", "DEFAULT_CONFIG"]
