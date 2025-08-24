"""
Configuration management for the Design Publications Scraper.

This module handles:
- Loading configuration from YAML files
- Configuration validation
- Default configuration values
"""

import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """Initialize the configuration manager."""
        self.config_path = config_path
        self._config: Optional[Dict[str, Any]] = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
            
            # Validate configuration
            self._validate_config()
            
            return self._config
            
        except FileNotFoundError:
            print(f"⚠️ Configuration file not found: {self.config_path}")
            print("📝 Using default configuration")
            return self._get_default_config()
            
        except yaml.YAMLError as e:
            print(f"❌ Error parsing configuration file: {e}")
            print("📝 Using default configuration")
            return self._get_default_config()
    
    def _validate_config(self) -> None:
        """Validate configuration structure."""
        required_keys = ["repos", "terms", "max_pages", "csv_filename"]
        
        for key in required_keys:
            if key not in self._config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        # Validate repositories
        if not isinstance(self._config["repos"], dict):
            raise ValueError("'repos' must be a dictionary")
        
        # Validate terms
        if not isinstance(self._config["terms"], list):
            raise ValueError("'terms' must be a list")
        
        # Validate max_pages
        if not isinstance(self._config["max_pages"], int) or self._config["max_pages"] <= 0:
            raise ValueError("'max_pages' must be a positive integer")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "repos": {
                "estudos_em_design": "estudos_em_design",
                "infodesign": "infodesign",
                "human_factors_in_design": "human_factors_in_design",
                "arcos_design": "arcos_design",
                "design_e_tecnologia": "design_e_tecnologia",
                "triades": "triades",
                "educacao_grafica": "educacao_grafica"
            },
            "terms": [
                "experiencia", "usuario", "interface", "usabilidade",
                "interacao", "sistema", "ergonomia", "digital",
                "informacao", "tecnologia"
            ],
            "max_pages": 10,
            "csv_filename": "data/raw/search_results.csv",
            "data_processing": {
                "transformed_results": "data/processed/transformed_results.csv",
                "enable_auto_transform": True
            },
            "curation": {
                "curation_candidates": "data/processed/curation_candidates.csv",
                "enable_auto_filtering": True
            },
            "deduplication": {
                "base_database": "data/raw/base_database.csv",
                "new_records_output": "data/processed/new_records.csv",
                "enable_auto_dedup": True
            }
        }
    
    def get_repos(self) -> Dict[str, str]:
        """Get repositories configuration."""
        config = self.load_config()
        return config.get("repos", {})
    
    def get_terms(self) -> list[str]:
        """Get search terms."""
        config = self.load_config()
        return config.get("terms", [])
    
    def get_max_pages(self) -> int:
        """Get maximum pages to scrape."""
        config = self.load_config()
        return config.get("max_pages", 10)
    
    def get_csv_filename(self) -> str:
        """Get CSV filename for results."""
        config = self.load_config()
        return config.get("csv_filename", "data/raw/search_results.csv")
    
    def get_data_processing_config(self) -> Dict[str, Any]:
        """Get data processing configuration."""
        config = self.load_config()
        return config.get("data_processing", {})
    
    def get_curation_config(self) -> Dict[str, Any]:
        """Get curation configuration."""
        config = self.load_config()
        return config.get("curation", {})
    
    def get_deduplication_config(self) -> Dict[str, Any]:
        """Get deduplication configuration."""
        config = self.load_config()
        return config.get("deduplication", {})
    
    def reload_config(self) -> Dict[str, Any]:
        """Reload configuration from file."""
        self._config = None
        return self.load_config()
    
    def save_config(self, config: Dict[str, Any], output_path: Optional[str] = None) -> None:
        """Save configuration to file."""
        if output_path is None:
            output_path = self.config_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"💾 Configuration saved to: {output_path}")


def load_config(path: str = "configs/config.yaml") -> Dict[str, Any]:
    """Convenience function to load configuration."""
    config_manager = ConfigManager(path)
    return config_manager.load_config()
