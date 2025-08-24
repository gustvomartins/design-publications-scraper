"""
Command Line Interface for the Design Publications Scraper.

This module provides:
- CLI commands for running scrapers
- Interactive configuration
- Command-line utilities
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from ..core.pipeline import Pipeline
from ..core.transformer import DataTransformer
from ..core.filter import ContentFilter
from ..config.config_manager import ConfigManager


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Design Publications Scraper - Sistema de scraping e catalogação de publicações de design e UX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run complete pipeline
  design-scraper run
  
  # Transform data only
  design-scraper transform data/raw/search_results.csv data/processed/transformed.csv
  
  # Filter content for curation
  design-scraper filter data/processed/transformed.csv data/processed/curation.csv
  
  # Show configuration
  design-scraper config show
  
  # Validate configuration
  design-scraper config validate
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run complete scraping pipeline")
    run_parser.add_argument(
        "--config", "-c",
        default="configs/config.yaml",
        help="Configuration file path (default: configs/config.yaml)"
    )
    
    # Transform command
    transform_parser = subparsers.add_parser("transform", help="Transform search results to base database format")
    transform_parser.add_argument("input", help="Input CSV file path")
    transform_parser.add_argument("output", help="Output CSV file path")
    transform_parser.add_argument(
        "--base-db",
        help="Optional base database path for validation"
    )
    
    # Filter command
    filter_parser = subparsers.add_parser("filter", help="Filter content for curation")
    filter_parser.add_argument("input", help="Input transformed CSV file path")
    filter_parser.add_argument("output", help="Output curation CSV file path")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subparsers = config_parser.add_subparsers(dest="config_command", help="Configuration commands")
    
    config_show_parser = config_subparsers.add_parser("show", help="Show current configuration")
    config_show_parser.add_argument(
        "--config", "-c",
        default="configs/config.yaml",
        help="Configuration file path"
    )
    
    config_validate_parser = config_subparsers.add_parser("validate", help="Validate configuration file")
    config_validate_parser.add_argument(
        "--config", "-c",
        default="configs/config.yaml",
        help="Configuration file path"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == "run":
            return _run_pipeline(args.config)
        elif args.command == "transform":
            return _transform_data(args.input, args.output, args.base_db)
        elif args.command == "filter":
            return _filter_content(args.input, args.output)
        elif args.command == "config":
            if args.config_command == "show":
                return _show_config(args.config)
            elif args.config_command == "validate":
                return _validate_config(args.config)
            else:
                config_parser.print_help()
                return 1
        else:
            parser.print_help()
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def _run_pipeline(config_path: str) -> int:
    """Run the complete scraping pipeline."""
    print("🚀 Starting Design Publications Scraper pipeline...")
    
    try:
        pipeline = Pipeline(config_path)
        pipeline.run_all_scrapers()
        print("✅ Pipeline completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return 1


def _transform_data(input_path: str, output_path: str, base_db_path: Optional[str]) -> int:
    """Transform search results data."""
    print(f"🔄 Transforming data from {input_path} to {output_path}")
    
    try:
        transformer = DataTransformer()
        result = transformer.transform_and_save_results(input_path, output_path, base_db_path)
        
        if result is not None:
            print("✅ Data transformation completed successfully!")
            return 0
        else:
            print("❌ Data transformation failed")
            return 1
            
    except Exception as e:
        print(f"❌ Data transformation error: {e}")
        return 1


def _filter_content(input_path: str, output_path: str) -> int:
    """Filter content for curation."""
    print(f"🔍 Filtering content from {input_path} to {output_path}")
    
    try:
        filter_tool = ContentFilter()
        result = filter_tool.filter_and_save_for_curation(input_path, output_path)
        
        if result is not None and not result.empty:
            print("✅ Content filtering completed successfully!")
            return 0
        else:
            print("⚠️ No relevant content found for curation")
            return 0
            
    except Exception as e:
        print(f"❌ Content filtering error: {e}")
        return 1


def _show_config(config_path: str) -> int:
    """Show current configuration."""
    print(f"📋 Configuration from: {config_path}")
    
    try:
        config_manager = ConfigManager(config_path)
        config = config_manager.load_config()
        
        print("\nConfiguration:")
        print(f"  Repositories: {len(config.get('repos', {}))}")
        print(f"  Search Terms: {len(config.get('terms', []))}")
        print(f"  Max Pages: {config.get('max_pages', 'N/A')}")
        print(f"  CSV Filename: {config.get('csv_filename', 'N/A')}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return 1


def _validate_config(config_path: str) -> int:
    """Validate configuration file."""
    print(f"🔍 Validating configuration: {config_path}")
    
    try:
        config_manager = ConfigManager(config_path)
        config = config_manager.load_config()
        
        print("✅ Configuration is valid!")
        print(f"  Repositories: {len(config.get('repos', {}))}")
        print(f"  Search Terms: {len(config.get('terms', []))}")
        print(f"  Max Pages: {config.get('max_pages', 'N/A')}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
