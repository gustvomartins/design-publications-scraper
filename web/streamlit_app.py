#!/usr/bin/env python3
"""
Interface Streamlit standalone para o Design Publications Scraper.
Este arquivo pode ser executado diretamente com: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import io
import sys
import os
import tempfile

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import required modules
try:
    from design_scraper.core.manual_search import ManualSearch
    from design_scraper.utils.scrapers_factory import ScrapterFactory
    from design_scraper.utils.data_transformer import transform_search_results
    from design_scraper.utils.deduplication import run_deduplication
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.info("💡 Certifique-se de que todos os módulos estão instalados corretamente.")
    st.stop()

def streamlit_app():
    st.set_page_config(
        page_title="Design Publications Scraper",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Scraper de Periódicos de Design")
    st.markdown("---")
    
    # Informação sobre a separação de responsabilidades
    st.info("""
    **ℹ️ Interface Web - Apenas Scraping**
    
    Esta interface traz resultados brutos dos scrapers, sem filtros ou deduplicação.
    Para processamento completo (filtros + deduplicação), use o pipeline automatizado via CLI.
    """)
    
    # Initialize manual search
    searcher = ManualSearch()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Repository selection (multiple choice)
        repo_options = {
            "Estudos em Design": "estudos_em_design",
            "InfoDesign": "infodesign", 
            "Human Factors in Design": "human_factors_in_design",
            "Arcos Design": "arcos_design",
            "Design e Tecnologia": "design_e_tecnologia",
            "Tríades em Revista": "triades",
            "Educação Gráfica": "educacao_grafica"
        }
        
        st.subheader("📚 Selecionar Repositórios")
        selected_repos = st.multiselect(
            "Escolha uma ou mais bases de dados:",
            options=list(repo_options.keys()),
            default=["Estudos em Design"]
        )
        
        # Search configuration
        st.subheader("🔍 Configuração da Busca")
        term = st.text_input(
            "Termos de pesquisa (máximo 10 palavras):",
            placeholder="Ex: experiência do usuário, usabilidade, interface"
        )
        
        max_pages = st.slider(
            "Número de páginas por busca:",
            min_value=1, max_value=50, value=10
        )
        
        # Execute button
        if st.button("🚀 Executar Busca", type="primary", use_container_width=True):
            if not selected_repos:
                st.error("❌ Selecione pelo menos um repositório!")
                return
            if not term.strip():
                st.error("❌ O termo de pesquisa não pode estar vazio!")
                return
            
            execute_manual_search(searcher, selected_repos, repo_options, term, max_pages)

def execute_manual_search(searcher, selected_repos, repo_options, term, max_pages):
    """Executa a busca manual com base nas configurações selecionadas"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Execute search (apenas scraping, sem filtros ou deduplicação)
        status_text.text("🔍 Executando busca...")
        progress_bar.progress(0.3)
        
        results = searcher.search_publications_raw(
            selected_repos, repo_options, term, max_pages
        )
        
        progress_bar.progress(0.8)
        
        if not results['success']:
            st.error(f"❌ {results['message']}")
            if 'total_scraped' in results and results['total_scraped'] > 0:
                st.info(f"📊 Total de resultados scraped: {results['total_scraped']}")
            return
        
        # Step 2: Display results
        progress_bar.progress(1.0)
        status_text.text("✅ Busca concluída!")
        
        display_results(searcher, results)
        
    except Exception as e:
        st.error(f"❌ Erro durante a busca: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Erro na busca")

def display_results(searcher, results):
    """Exibe os resultados e opções de download"""
    
    st.markdown("---")
    st.header("📊 Resultados da Busca")
    
    # Get search summary
    summary = searcher.get_search_summary(results)
    
    # Summary statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Scraped", summary['total_scraped'])
    
    with col2:
        st.metric("Resultados Finais", summary['final_results'])
    
    # Repository statistics
    if summary['scraping_stats']:
        st.subheader("📚 Estatísticas por Repositório")
        stats_df = pd.DataFrame([
            {'Repositório': repo, 'Resultados': count} 
            for repo, count in summary['scraping_stats'].items()
            if isinstance(count, int)
        ])
        if not stats_df.empty:
            st.bar_chart(stats_df.set_index('Repositório'))
    
    # Results table
    st.subheader("📋 Lista de Resultados")
    
    results_df = results['results_df']
    
    # Format display columns
    display_df = results_df.copy()
    if 'timestamp' in display_df.columns:
        display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Show results with pagination
    max_display = 100
    if len(display_df) > max_display:
        st.info(f"Mostrando primeiros {max_display} resultados de {len(display_df)}. Use o download para ver todos.")
        display_df = display_df.head(max_display)
    
    st.dataframe(display_df, use_container_width=True)
    
    # Download options
    st.subheader("💾 Download dos Resultados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV download
        try:
            csv_data, csv_filename, csv_mime = searcher.export_results(
                results_df, "csv", "design_publications"
            )
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=csv_filename,
                mime=csv_mime
            )
        except Exception as e:
            st.error(f"❌ Erro ao gerar CSV: {e}")
    
    with col2:
        # Excel download
        try:
            excel_data, excel_filename, excel_mime = searcher.export_results(
                results_df, "excel", "design_publications"
            )
            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=excel_filename,
                mime=excel_mime
            )
        except ImportError:
            st.info("📊 Excel não disponível (instale openpyxl)")
        except Exception as e:
            st.error(f"❌ Erro ao gerar Excel: {e}")
    
    # Return results for programmatic access
    return results_df

if __name__ == "__main__":
    streamlit_app()
