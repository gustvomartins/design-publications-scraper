"""
Pipeline automatizado para scraping de publicações de design.
Este módulo executa o processo completo de scraping, filtragem e deduplicação
baseado na configuração do arquivo YAML.
"""

import time
import pandas as pd
import yaml
import os
from ..utils.scrapers_factory import ScrapterFactory
from ..utils.deduplication import run_deduplication
from ..utils.data_transformer import transform_search_results


class AutomatedPipeline:
    """Pipeline automatizado para scraping de publicações"""
    
    def __init__(self, config_path="src/design_scraper/config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self, path=None):
        """Carrega configuração do arquivo YAML"""
        config_path = path or self.config_path
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def run(self):
        """Executa o pipeline automatizado completo"""
        print("🚀 Iniciando Pipeline Automatizado...")
        print("=" * 60)
        
        try:
            return self._run_all_scrapers()
        except Exception as e:
            print(f"❌ Erro no pipeline: {e}")
            raise
    
    def _run_all_scrapers(self):
        """Executa todos os scrapers configurados"""
        config = self.config
        
        repos = config["repos"]
        terms = config["terms"]
        max_pages = config["max_pages"]
        raw_results_filename = config.get("raw_results_filename", "data/raw/search_results.csv")
        filtered_results_filename = config.get("filtered_results_filename", "data/processed/filtered_results.csv")
        new_records_filename = config.get("new_records_filename", "data/processed/new_records.csv")
        
        all_results = []
        
        print(f"📚 Repositórios configurados: {', '.join(repos.keys())}")
        print(f"🔍 Termos de busca: {', '.join(terms)}")
        print(f"📄 Máximo de páginas por busca: {max_pages}")
        print(f"📁 Arquivo de resultados brutos: {raw_results_filename}")
        print(f"📁 Arquivo de resultados filtrados: {filtered_results_filename}")
        print(f"📁 Arquivo de novos registros: {new_records_filename}")
        print("-" * 60)
        
        # Step 1: Scraping
        for repo_name, scraper_key in repos.items():
            print(f"\n🔍 Executando scraper: {repo_name}")
            scraper = ScrapterFactory.get_scraper(scraper_key)
            
            for term in terms:
                try:
                    print(f"   🔎 Buscando por: '{term}'")
                    results = scraper.search(term, max_pages)
                    
                    if results:
                        # Add metadata
                        for r in results:
                            r["fonte"] = repo_name
                            r["termo"] = term
                        all_results.extend(results)
                        print(f"   ✅ {len(results)} resultados encontrados")
                    else:
                        print(f"   ⚠️ Nenhum resultado para '{term}'")
                        
                except Exception as e:
                    print(f"   ❌ Erro no scraper {repo_name} para '{term}': {e}")
            
            # Pausa para evitar requisições seguidas
            time.sleep(2)
        
        if not all_results:
            print("\n⚠️ Nenhum resultado encontrado pelos scrapers!")
            return None
        
        # Step 2: Save raw results
        print(f"\n💾 Salvando {len(all_results)} resultados brutos...")
        self._save_raw_results(raw_results_filename, all_results)
        
        # Step 3: Transform and filter results
        print(f"\n🔄 Transformando e filtrando resultados...")
        filtered_df = transform_search_results(raw_results_filename, filtered_results_filename)
        
        if filtered_df.empty:
            print("⚠️ Nenhum resultado passou pelos filtros aplicados!")
            return None
        
        # Step 4: Execute deduplication
        print(f"\n🔄 Executando deduplicação...")
        dedup_config = config.get("deduplication", {})
        base_db_path = dedup_config.get("base_database", "data/raw/base_database.csv")
        
        new_records = run_deduplication(
            filtered_results_path=filtered_results_filename,
            base_db_path=base_db_path,
            output_path=new_records_filename
        )
        
        # Final summary
        print(f"\n✨ Pipeline automatizado concluído com sucesso!")
        print("=" * 60)
        print(f"📊 Resultados brutos: {len(all_results)}")
        print(f"🎯 Resultados filtrados: {len(filtered_df)}")
        print(f"✨ Novos registros: {len(new_records)}")
        print(f"📁 Arquivos gerados:")
        print(f"   • {raw_results_filename}")
        print(f"   • {filtered_results_filename}")
        print(f"   • {new_records_filename}")
        
        return {
            'raw_count': len(all_results),
            'filtered_count': len(filtered_df),
            'new_records_count': len(new_records),
            'raw_file': raw_results_filename,
            'filtered_file': filtered_results_filename,
            'new_records_file': new_records_filename
        }
    
    def _save_raw_results(self, filename, new_results):
        """Salva resultados brutos dos scrapers"""
        df_new = pd.DataFrame(new_results)
        if df_new.empty:
            return
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            df_old = pd.read_csv(filename)
        except FileNotFoundError:
            df_old = pd.DataFrame()
        
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.to_csv(filename, index=False)
        print(f"   📂 Arquivo atualizado: {filename} ({len(df)} linhas no total)")
    
    def get_status(self):
        """Retorna o status atual do pipeline"""
        config = self.config
        
        # Check if output files exist
        raw_file = config.get("raw_results_filename", "data/raw/search_results.csv")
        filtered_file = config.get("filtered_results_filename", "data/processed/filtered_results.csv")
        new_records_file = config.get("new_records_filename", "data/processed/new_records.csv")
        
        status = {
            'config_loaded': bool(self.config),
            'repos_count': len(config.get("repos", {})),
            'terms_count': len(config.get("terms", [])),
            'raw_file_exists': os.path.exists(raw_file),
            'filtered_file_exists': os.path.exists(filtered_file),
            'new_records_file_exists': os.path.exists(new_records_file)
        }
        
        # Add file sizes if they exist
        for file_path in [raw_file, filtered_file, new_records_file]:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                status[f'{os.path.basename(file_path)}_size'] = size
        
        return status


def run_automated_pipeline(config_path="src/design_scraper/config/config.yaml"):
    """Função de conveniência para executar o pipeline automatizado"""
    pipeline = AutomatedPipeline(config_path)
    return pipeline.run()


if __name__ == "__main__":
    # Execução direta do pipeline
    result = run_automated_pipeline()
    if result:
        print(f"\n✅ Pipeline executado com sucesso!")
        print(f"📊 Resumo: {result}")
    else:
        print(f"\n❌ Pipeline falhou!")
