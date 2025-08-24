import time
import os
import pandas as pd
import yaml
from utils.scrapers_factory import ScrapterFactory
from utils.deduplication import run_deduplication
from utils.data_transformer import transform_and_save_results
from utils.content_filter import filter_and_save_for_curation


def load_config(path="configs/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_results(filename, new_results):
    """Concatena novos resultados SEM remover duplicatas."""
    df_new = pd.DataFrame(new_results)
    if df_new.empty:
        return

    # Transforma os dados para o formato da base de dados
    transformed_filename = filename.replace('.csv', '_transformed.csv')
    
    # Salva temporariamente os novos resultados para transformação
    temp_filename = filename.replace('.csv', '_temp.csv')
    df_new.to_csv(temp_filename, index=False)
    
    transformed_df = transform_and_save_results(
        search_results_path=temp_filename,
        output_path=transformed_filename
    )
    
    if transformed_df is None:
        print("❌ Falha na transformação dos dados")
        return

    try:
        df_old = pd.read_csv(filename)
    except FileNotFoundError:
        df_old = pd.DataFrame()

    df = pd.concat([df_old, df_new], ignore_index=True)
    df.to_csv(filename, index=False)
    print(f"📂 Arquivo atualizado: {filename} ({len(df)} linhas no total)")
    
    # Salva também os dados transformados
    if transformed_df is not None:
        transformed_df.to_csv(transformed_filename, index=False)
        print(f"🔄 Dados transformados salvos em: {transformed_filename}")
        
        # Aplica filtragem para curadoria
        curation_filename = filename.replace('.csv', '_curation.csv')
        curation_df = filter_and_save_for_curation(
            transformed_filename,
            curation_filename
        )
        
        if curation_df is not None and not curation_df.empty:
            print(f"🎯 Conteúdo filtrado para curadoria: {len(curation_df)} registros")
        else:
            print("⚠️ Nenhum conteúdo relevante encontrado para curadoria")


def run_all_scrapers(config_path="configs/config.yaml"):
    config = load_config(config_path)

    repos = config["repos"]
    terms = config["terms"]
    max_pages = config["max_pages"]
    csv_filename = config["csv_filename"]

    all_results = []

    for repo_name, scraper_key in repos.items():
        print(f"\n🔍 Rodando scraper: {repo_name}")
        scraper = ScrapterFactory.get_scraper(scraper_key)

        for term in terms:
            try:
                results = scraper.search(term, max_pages)
                if results:
                    for r in results:
                        r["fonte"] = repo_name
                        r["termo"] = term
                    all_results.extend(results)
                    print(f"   ➕ {len(results)} resultados para '{term}'")
                else:
                    print(f"   ⚠️ Nenhum resultado para '{term}'")
            except Exception as e:
                print(f"   ❌ Erro no scraper {repo_name}: {e}")

        # Pausa para evitar requisições seguidas
        time.sleep(2)

    if all_results:
        save_results(csv_filename, all_results)
        
        # Executa deduplicação após salvar os resultados (se habilitada)
        if config.get("deduplication", {}).get("enable_auto_dedup", True):
            print(f"\n🔄 Executando deduplicação...")
            dedup_config = config.get("deduplication", {})
            
            # Usa os dados transformados para deduplicação
            transformed_filename = csv_filename.replace('.csv', '_transformed.csv')
            if os.path.exists(transformed_filename):
                run_deduplication(
                    new_results_path=transformed_filename,
                    base_db_path=dedup_config.get("base_database", "data/raw/base_database.csv"),
                    output_path=dedup_config.get("new_records_output", "data/processed/new_records.csv")
                )
            else:
                print("⚠️ Dados transformados não encontrados para deduplicação")


if __name__ == "__main__":
    run_all_scrapers()
