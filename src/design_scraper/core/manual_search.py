"""
Módulo para busca manual de publicações de design.
Este módulo gerencia as operações de busca manual independente da interface Streamlit.
"""

import pandas as pd
import tempfile
import os
from ..utils.scrapers_factory import ScrapterFactory
from ..utils.data_transformer import transform_search_results
from ..utils.deduplication import run_deduplication


class ManualSearch:
    """Gerencia buscas manuais de publicações"""
    
    def __init__(self, config_path="src/design_scraper/config/manual_search_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """Carrega configuração para busca manual"""
        try:
            import yaml
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Configuração padrão se o arquivo não existir
            return {
                "manual_search": {
                    "default_max_pages": 10,
                    "default_apply_filters": True,
                    "default_run_dedup": True,
                    "max_pages_limit": 50,
                    "max_results_display": 100
                }
            }
    
    def search_publications_raw(self, selected_repos, repo_options, term, max_pages):
        """
        Executa busca manual de publicações APENAS com scraping (sem filtros ou deduplicação)
        
        Args:
            selected_repos: Lista de repositórios selecionados
            repo_options: Dicionário de opções de repositórios
            term: Termo de busca
            max_pages: Número máximo de páginas
            
        Returns:
            dict: Resultados brutos da busca com estatísticas
        """
        
        # Validações
        if not selected_repos:
            raise ValueError("Nenhum repositório selecionado")
        
        if not term.strip():
            raise ValueError("Termo de busca não pode estar vazio")
        
        max_pages = min(max_pages, self.config["manual_search"]["max_pages_limit"])
        
        # Step 1: Scraping apenas
        all_results = []
        scraping_stats = {}
        
        for repo_name in selected_repos:
            scraper_key = repo_options[repo_name]
            
            try:
                scraper = ScrapterFactory.get_scraper(scraper_key)
                results = scraper.search(term, max_pages)
                
                if results:
                    # Add metadata
                    for r in results:
                        r["fonte"] = repo_name
                        r["termo"] = term
                    all_results.extend(results)
                    scraping_stats[repo_name] = len(results)
                else:
                    scraping_stats[repo_name] = 0
                    
            except Exception as e:
                scraping_stats[repo_name] = f"Erro: {str(e)}"
        
        if not all_results:
            return {
                'success': False,
                'message': 'Nenhum resultado encontrado',
                'scraping_stats': scraping_stats
            }
        
        # Step 2: Retorna resultados brutos sem processamento
        results_df = pd.DataFrame(all_results)
        
        # Prepare results
        return {
            'success': True,
            'total_scraped': len(all_results),
            'final_results_count': len(results_df),
            'scraping_stats': scraping_stats,
            'results_df': results_df,
            'filters_applied': False,
            'dedup_applied': False
        }

    def search_publications(self, selected_repos, repo_options, term, max_pages, 
                           apply_filters=True, run_dedup=True):
        """
        Executa busca manual de publicações com processamento completo (filtros + deduplicação)
        
        Args:
            selected_repos: Lista de repositórios selecionados
            repo_options: Dicionário de opções de repositórios
            term: Termo de busca
            max_pages: Número máximo de páginas
            apply_filters: Se deve aplicar filtros
            run_dedup: Se deve executar deduplicação
            
        Returns:
            dict: Resultados da busca com estatísticas
        """
        
        # Validações
        if not selected_repos:
            raise ValueError("Nenhum repositório selecionado")
        
        if not term.strip():
            raise ValueError("Termo de busca não pode estar vazio")
        
        max_pages = min(max_pages, self.config["manual_search"]["max_pages_limit"])
        
        # Step 1: Scraping
        all_results = []
        scraping_stats = {}
        
        for repo_name in selected_repos:
            scraper_key = repo_options[repo_name]
            
            try:
                scraper = ScrapterFactory.get_scraper(scraper_key)
                results = scraper.search(term, max_pages)
                
                if results:
                    # Add metadata
                    for r in results:
                        r["fonte"] = repo_name
                        r["termo"] = term
                    all_results.extend(results)
                    scraping_stats[repo_name] = len(results)
                else:
                    scraping_stats[repo_name] = 0
                    
            except Exception as e:
                scraping_stats[repo_name] = f"Erro: {str(e)}"
        
        if not all_results:
            return {
                'success': False,
                'message': 'Nenhum resultado encontrado',
                'scraping_stats': scraping_stats
            }
        
        # Step 2: Data transformation and filtering
        results_df = pd.DataFrame(all_results)
        
        if apply_filters:
            # Create temporary file for raw results
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
                results_df.to_csv(tmp_file.name, index=False)
                tmp_raw_path = tmp_file.name
            
            # Create temporary file for filtered results
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
                tmp_filtered_path = tmp_file.name
            
            # Transform and filter
            filtered_df = transform_search_results(tmp_raw_path, tmp_filtered_path)
            
            # Clean up temp files
            os.unlink(tmp_raw_path)
            os.unlink(tmp_filtered_path)
            
            if filtered_df.empty:
                return {
                    'success': False,
                    'message': 'Nenhum resultado passou pelos filtros',
                    'scraping_stats': scraping_stats,
                    'total_scraped': len(all_results)
                }
            
            results_df = filtered_df
        
        # Step 3: Deduplication (optional)
        if run_dedup and not results_df.empty:
            # Create temporary file for results
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
                results_df.to_csv(tmp_file.name, index=False)
                tmp_results_path = tmp_file.name
            
            # Create temporary file for new records
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
                tmp_new_records_path = tmp_file.name
            
            # Run deduplication
            new_records = run_deduplication(
                filtered_results_path=tmp_results_path,
                base_db_path="data/raw/base_database.csv",
                output_path=tmp_new_records_path
            )
            
            # Clean up temp files
            os.unlink(tmp_results_path)
            os.unlink(tmp_new_records_path)
            
            results_df = new_records
        
        # Prepare results
        return {
            'success': True,
            'total_scraped': len(all_results),
            'final_results_count': len(results_df),
            'scraping_stats': scraping_stats,
            'results_df': results_df,
            'filters_applied': apply_filters,
            'dedup_applied': run_dedup
        }
    
    def export_results(self, results_df, format_type="csv", filename_prefix="manual_search"):
        """
        Exporta resultados em diferentes formatos
        
        Args:
            results_df: DataFrame com os resultados
            format_type: Tipo de formato ("csv" ou "excel")
            filename_prefix: Prefixo para o nome do arquivo
            
        Returns:
            tuple: (dados_do_arquivo, nome_do_arquivo, tipo_mime)
        """
        
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
        
        if format_type.lower() == "csv":
            data = results_df.to_csv(index=False, encoding='utf-8-sig')
            filename = f"{filename_prefix}_{timestamp}.csv"
            mime_type = "text/csv"
            
        elif format_type.lower() == "excel":
            try:
                import io
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    results_df.to_excel(writer, sheet_name='Resultados', index=False)
                data = excel_buffer.getvalue()
                filename = f"{filename_prefix}_{timestamp}.xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
            except ImportError:
                raise ImportError("openpyxl não está instalado. Instale com: pip install openpyxl")
        
        else:
            raise ValueError(f"Formato não suportado: {format_type}")
        
        return data, filename, mime_type
    
    def get_search_summary(self, results):
        """
        Gera um resumo da busca
        
        Args:
            results: Resultados da busca
            
        Returns:
            dict: Resumo da busca
        """
        
        if not results['success']:
            return {
                'status': 'Falhou',
                'message': results['message'],
                'total_scraped': results.get('total_scraped', 0)
            }
        
        summary = {
            'status': 'Sucesso',
            'total_scraped': results['total_scraped'],
            'final_results': results['final_results_count'],
            'filters_applied': results['filters_applied'],
            'dedup_applied': results['dedup_applied'],
            'repositories': list(results['scraping_stats'].keys()),
            'scraping_stats': results['scraping_stats']
        }
        
        return summary


def search_publications_manual(selected_repos, repo_options, term, max_pages, 
                              apply_filters=True, run_dedup=True):
    """
    Função de conveniência para busca manual
    
    Args:
        selected_repos: Lista de repositórios selecionados
        repo_options: Dicionário de opções de repositórios
        term: Termo de busca
        max_pages: Número máximo de páginas
        apply_filters: Se deve aplicar filtros
        run_dedup: Se deve executar deduplicação
        
    Returns:
        dict: Resultados da busca
    """
    
    searcher = ManualSearch()
    return searcher.search_publications(
        selected_repos, repo_options, term, max_pages, 
        apply_filters, run_dedup
    )
