#!/usr/bin/env python3
"""
Test script for the new filtering and transformation process.
This script demonstrates how the updated pipeline works.
"""

import sys
import os
import pandas as pd

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from design_scraper.utils.data_transformer import transform_search_results
from design_scraper.utils.deduplication import run_deduplication

def test_filtering_and_transformation():
    """Test the complete filtering and transformation pipeline"""
    
    print("🧪 Testando o novo processo de filtragem e transformação...")
    print("=" * 60)
    
    # Check if input file exists
    input_file = "data/raw/search_results.csv"
    if not os.path.exists(input_file):
        print(f"❌ Arquivo de entrada não encontrado: {input_file}")
        return
    
    # Load and check input data
    print(f"\n📥 Carregando dados de entrada: {input_file}")
    try:
        input_df = pd.read_csv(input_file)
        print(f"   📊 Total de registros de entrada: {len(input_df)}")
        print(f"   📋 Colunas: {list(input_df.columns)}")
        
        if not input_df.empty:
            print(f"   🔍 Primeiros títulos:")
            for i, title in enumerate(input_df['title'].head(5)):
                print(f"      {i+1}. {title[:80]}...")
        else:
            print("   ⚠️ Arquivo de entrada está vazio")
            return
            
    except Exception as e:
        print(f"❌ Erro ao carregar dados de entrada: {e}")
        return
    
    # Step 1: Transform and filter raw results
    print(f"\n1️⃣ Transformando e filtrando resultados brutos...")
    filtered_df = transform_search_results(
        "data/raw/search_results.csv",
        "data/processed/filtered_results.csv"
    )
    
    if filtered_df.empty:
        print("❌ Nenhum resultado foi filtrado. Verifique os dados de entrada.")
        return
    
    print(f"✅ Filtragem concluída: {len(filtered_df)} registros válidos")
    
    # Step 2: Run deduplication
    print(f"\n2️⃣ Executando deduplicação...")
    new_records = run_deduplication(
        "data/processed/filtered_results.csv",
        "data/raw/base_database.csv",
        "data/processed/new_records.csv"
    )
    
    print(f"✅ Deduplicação concluída: {len(new_records)} novos registros")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMO DO PROCESSO:")
    print(f"   • Resultados brutos: {len(input_df)}")
    print(f"   • Resultados filtrados: {len(filtered_df)}")
    print(f"   • Novos registros: {len(new_records)}")
    print(f"   • Arquivo filtrado: data/processed/filtered_results.csv")
    print(f"   • Arquivo de novos registros: data/processed/new_records.csv")
    print("\n⚠️ IMPORTANTE:")
    print("   • A base de dados NÃO foi atualizada automaticamente")
    print("   • Os novos registros foram salvos separadamente para revisão")
    print("   • Revise os registros antes de adicionar à base principal")

if __name__ == "__main__":
    test_filtering_and_transformation()
