#!/usr/bin/env python3
"""
Script para executar deduplicação de resultados de scraping
"""

import argparse
import os
from utils.deduplication import run_deduplication


def main():
    parser = argparse.ArgumentParser(
        description="Executa deduplicação de resultados de scraping"
    )
    
    parser.add_argument(
        "--new-results", 
        default="data/raw/search_results.csv",
        help="Caminho para o CSV com novos resultados (padrão: data/raw/search_results.csv)"
    )
    
    parser.add_argument(
        "--base-db", 
        default="data/raw/base_database.csv",
        help="Caminho para a base de dados existente (padrão: data/raw/base_database.csv)"
    )
    
    parser.add_argument(
        "--output", 
        default="data/processed/new_records.csv",
        help="Caminho para salvar apenas os novos registros (padrão: data/processed/new_records.csv)"
    )
    
    parser.add_argument(
        "--create-base", 
        action="store_true",
        help="Cria uma nova base de dados a partir dos resultados atuais"
    )
    
    args = parser.parse_args()
    
    # Verifica se os arquivos existem
    if not os.path.exists(args.new_results):
        print(f"❌ Arquivo de novos resultados não encontrado: {args.new_results}")
        return
    
    if args.create_base:
        # Cria uma nova base de dados
        print("🆕 Criando nova base de dados...")
        import pandas as pd
        
        try:
            df = pd.read_csv(args.new_results)
            df.to_csv(args.base_db, index=False)
            print(f"✅ Base de dados criada em: {args.base_db}")
            print(f"   Total de registros: {len(df)}")
        except Exception as e:
            print(f"❌ Erro ao criar base de dados: {e}")
            return
    else:
        # Executa deduplicação
        run_deduplication(
            new_results_path=args.new_results,
            base_db_path=args.base_db,
            output_path=args.output
        )


if __name__ == "__main__":
    main()
