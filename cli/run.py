#!/usr/bin/env python3
"""
Entry point for the Design Publications Scraper application.
This script provides a clean interface to run the automated pipeline from the root directory.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from design_scraper.core.automated_pipeline import AutomatedPipeline

if __name__ == "__main__":
    # Create and run the automated pipeline
    pipeline = AutomatedPipeline()
    result = pipeline.run()
    
    if result:
        print(f"\n✅ Pipeline executado com sucesso!")
        print(f"📊 Resumo: {result}")
    else:
        print(f"\n❌ Pipeline falhou!")
        sys.exit(1)
