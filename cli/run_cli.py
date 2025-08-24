#!/usr/bin/env python3
"""
Command-line entry point for the Design Publications Scraper application.
This script provides a clean CLI interface for the automated pipeline.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from design_scraper.core.automated_pipeline import AutomatedPipeline

def main():
    """Main CLI function"""
    print("🚀 Design Publications Scraper - Pipeline Automatizado")
    print("=" * 60)
    
    try:
        # Create and run the automated pipeline
        pipeline = AutomatedPipeline()
        
        # Show pipeline status before running
        print("📊 Status do Pipeline:")
        status = pipeline.get_status()
        for key, value in status.items():
            print(f"   • {key}: {value}")
        
        print("\n" + "=" * 60)
        
        # Run the pipeline
        result = pipeline.run()
        
        if result:
            print("\n✅ Pipeline executado com sucesso!")
            print(f"📊 Resumo final:")
            for key, value in result.items():
                print(f"   • {key}: {value}")
        else:
            print("\n❌ Pipeline falhou ou não retornou resultados!")
            return 1
        
    except Exception as e:
        print(f"\n❌ Erro executando pipeline: {e}")
        print("\nPara debugging, você pode executar:")
        print("  python test_filtering.py")
        print("  python src/design_scraper/core/automated_pipeline.py")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
