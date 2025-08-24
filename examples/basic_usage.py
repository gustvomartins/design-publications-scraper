#!/usr/bin/env python3
"""
Basic usage example for the Design Publications Scraper.

This example demonstrates how to use the main components:
1. Data transformation
2. Content filtering
3. Pipeline execution
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from design_scraper.core.transformer import DataTransformer
from design_scraper.core.filter import ContentFilter
from design_scraper.core.pipeline import Pipeline


def example_data_transformation():
    """Example of data transformation."""
    print("🔄 Example: Data Transformation")
    print("=" * 50)
    
    # Create transformer
    transformer = DataTransformer()
    
    # Example: Transform search results
    input_file = "data/raw/search_results.csv"
    output_file = "data/processed/example_transformed.csv"
    
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    
    try:
        result = transformer.transform_and_save_results(input_file, output_file)
        if result is not None:
            print(f"✅ Transformed {len(result)} records successfully!")
            print(f"Columns: {list(result.columns)}")
        else:
            print("❌ Transformation failed")
    except FileNotFoundError:
        print("⚠️ Input file not found - this is expected in the example")
        print("   In real usage, you would have search results to transform")
    
    print()


def example_content_filtering():
    """Example of content filtering."""
    print("🔍 Example: Content Filtering")
    print("=" * 50)
    
    # Create filter
    filter_tool = ContentFilter()
    
    # Example: Filter content for curation
    input_file = "data/processed/example_transformed.csv"
    output_file = "data/processed/example_curation.csv"
    
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    
    try:
        result = filter_tool.filter_and_save_for_curation(input_file, output_file)
        if result is not None and not result.empty:
            print(f"✅ Filtered {len(result)} records for curation!")
            print(f"Relevance scores: {result['relevance_score'].value_counts().to_dict()}")
        else:
            print("⚠️ No content found for curation")
    except FileNotFoundError:
        print("⚠️ Input file not found - this is expected in the example")
        print("   In real usage, you would have transformed data to filter")
    
    print()


def example_pipeline():
    """Example of pipeline execution."""
    print("🚀 Example: Pipeline Execution")
    print("=" * 50)
    
    # Create pipeline
    config_path = "configs/config.yaml"
    pipeline = Pipeline(config_path)
    
    print(f"Configuration: {config_path}")
    print("Pipeline components:")
    print("  - Scrapers execution")
    print("  - Data transformation")
    print("  - Content filtering")
    print("  - Deduplication")
    
    print("\nTo run the complete pipeline:")
    print("  python -m design_scraper run")
    print("  python -m design_scraper run --config configs/config.yaml")
    
    print()


def example_cli_commands():
    """Example of CLI commands."""
    print("💻 Example: CLI Commands")
    print("=" * 50)
    
    print("Available commands:")
    print()
    print("1. Run complete pipeline:")
    print("   design-scraper run")
    print("   design-scraper run --config configs/config.yaml")
    print()
    print("2. Transform data only:")
    print("   design-scraper transform input.csv output.csv")
    print("   design-scraper transform input.csv output.csv --base-db base.csv")
    print()
    print("3. Filter content for curation:")
    print("   design-scraper filter transformed.csv curation.csv")
    print()
    print("4. Configuration management:")
    print("   design-scraper config show")
    print("   design-scraper config validate")
    print()
    print("5. Get help:")
    print("   design-scraper --help")
    print("   design-scraper run --help")
    print()


def main():
    """Run all examples."""
    print("🎯 Design Publications Scraper - Basic Usage Examples")
    print("=" * 60)
    print()
    
    example_data_transformation()
    example_content_filtering()
    example_pipeline()
    example_cli_commands()
    
    print("📚 For more information, see the documentation:")
    print("   - docs/user_guide/")
    print("   - docs/api/")
    print("   - README.md")
    print()
    print("🔧 To install the package:")
    print("   pip install -e .")
    print()
    print("✅ Examples completed!")


if __name__ == "__main__":
    main()
