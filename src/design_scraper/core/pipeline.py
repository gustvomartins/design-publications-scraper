"""
Main pipeline for the Design Publications Scraper.

This module orchestrates the entire scraping process:
1. Execute scrapers
2. Transform data
3. Filter content for curation
4. Run deduplication
"""

import time
import os
from typing import List, Dict, Any
import pandas as pd
import yaml

from ..config.config_manager import ConfigManager
from ..utils.scrapers_factory import ScrapersFactory
from ..utils.deduplication import run_deduplication
from .transformer import DataTransformer
from .filter import ContentFilter


class Pipeline:
    """Main pipeline for orchestrating the scraping process."""
    
    def __init__(self, config_path: str = "configs/config.yaml"):
        """Initialize the pipeline with configuration."""
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        
    def run_all_scrapers(self) -> None:
        """Execute all configured scrapers and process results."""
        repos = self.config["repos"]
        terms = self.config["terms"]
        max_pages = self.config["max_pages"]
        csv_filename = self.config["csv_filename"]
        
        all_results = []
        
        for repo_name, scraper_key in repos.items():
            print(f"\n🔍 Running scraper: {repo_name}")
            scraper = ScrapersFactory.get_scraper(scraper_key)
            
            for term in terms:
                try:
                    results = scraper.search(term, max_pages)
                    if results:
                        for r in results:
                            r["fonte"] = repo_name
                            r["termo"] = term
                        all_results.extend(results)
                        print(f"   ➕ {len(results)} results for '{term}'")
                    else:
                        print(f"   ⚠️ No results for '{term}'")
                except Exception as e:
                    print(f"   ❌ Error in scraper {repo_name}: {e}")
            
            # Pause to avoid consecutive requests
            time.sleep(2)
        
        if all_results:
            self._save_and_process_results(csv_filename, all_results)
    
    def _save_and_process_results(self, filename: str, new_results: List[Dict[str, Any]]) -> None:
        """Save results and process them through the pipeline."""
        df_new = pd.DataFrame(new_results)
        if df_new.empty:
            return
        
        # Transform data to base database format
        transformed_filename = filename.replace('.csv', '_transformed.csv')
        
        # Save temporarily for transformation
        temp_filename = filename.replace('.csv', '_temp.csv')
        df_new.to_csv(temp_filename, index=False)
        
        # Transform data
        transformer = DataTransformer()
        transformed_df = transformer.transform_and_save_results(
            search_results_path=temp_filename,
            output_path=transformed_filename
        )
        
        if transformed_df is None:
            print("❌ Data transformation failed")
            return
        
        # Save original results
        try:
            df_old = pd.read_csv(filename)
        except FileNotFoundError:
            df_old = pd.DataFrame()
        
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"📂 File updated: {filename} ({len(df)} total rows)")
        
        # Save transformed data
        if transformed_df is not None:
            transformed_df.to_csv(transformed_filename, index=False)
            print(f"🔄 Transformed data saved to: {transformed_filename}")
            
            # Apply curation filtering
            curation_filename = filename.replace('.csv', '_curation.csv')
            filter_tool = ContentFilter()
            curation_df = filter_tool.filter_and_save_for_curation(
                transformed_filename,
                curation_filename
            )
            
            if curation_df is not None and not curation_df.empty:
                print(f"🎯 Content filtered for curation: {len(curation_df)} records")
            else:
                print("⚠️ No relevant content found for curation")
        
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        # Run deduplication if enabled
        if self.config.get("deduplication", {}).get("enable_auto_dedup", True):
            print(f"\n🔄 Running deduplication...")
            dedup_config = self.config.get("deduplication", {})
            
            # Use transformed data for deduplication
            if os.path.exists(transformed_filename):
                run_deduplication(
                    new_results_path=transformed_filename,
                    base_db_path=dedup_config.get("base_database", "data/raw/base_database.csv"),
                    output_path=dedup_config.get("new_records_output", "data/processed/new_records.csv")
                )
            else:
                print("⚠️ Transformed data not found for deduplication")


def run_pipeline(config_path: str = "configs/config.yaml") -> None:
    """Convenience function to run the pipeline."""
    pipeline = Pipeline(config_path)
    pipeline.run_all_scrapers()


if __name__ == "__main__":
    run_pipeline()
