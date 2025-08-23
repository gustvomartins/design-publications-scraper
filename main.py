import sys
import streamlit as st
from utils.scrapers_factory import ScrapterFactory
from utils.export_csv import export_to_csv

def streamlit_app():
    st.title("Scraper de Periódicos de Design")

    repo_options = {
        "Estudos em Design": "estudos_em_design",
        "InfoDesign": "infodesign",
        "Repositório UFRN": "repositorio_ufrn",
        "Human Factors in Design": "human_factors_in_design",
        "Arcos Design": "arcos_design",
        "Design e Tecnologia": "design_e_tecnologia",
        "Tríades em Revista": "triades",
        "Educação Gráfica": "educacao_grafica"
    }

    repo_display = list(repo_options.keys())

    selected_repo = st.selectbox("Selecione um repositório", repo_display)

    term = st.text_input("Insira os termos de pesquisa (máximo 10 palavras): ")

    max_pages = st.number_input("Insira o número de páginas para consulta: ", min_value=1, max_value=100, value=10)

    if st.button("Buscar"):
        scraper_name = repo_options[selected_repo]
        if not term.strip():
            st.error("O termo de pesquisa não pode estar vazio.")
            return
        
        with st.spinner("Buscando resultados..."):
            success = run_scraper(scraper_name, term, max_pages)
            if success:
                st.success("Busca concluída! Arquivo 'search_results.csv' gerado.")
                with open("search_results.csv", "rb") as file:
                    st.download_button("Download CSV", file, file_name="search_results.csv", mime="text/csv")
            else:
                st.warning("Nenhum resultado encontrado ou ocorreu um erro.")

def run_scraper(scraper_name, term, max_pages):
    try:
        scraper = ScrapterFactory.get_scraper(scraper_name)
    except ValueError as e:
        return False
    if not term.strip():
        return False
    try:
        results = scraper.search(term, max_pages)
    except Exception:
        return False
    if results:
        csv_filename = "search_results.csv"
        export_to_csv(csv_filename, results, fieldnames=list(results[0].keys()))
        return True
    else:
        return False

def main():
    if "streamlit" in sys.modules:
        streamlit_app()
    else:
        print("""Selecione o repositório ou periódico: 
          1. Estudos em Design
          2. InfoDesign
          3. Repositório Institucional UFRN
          4. Human Factors in Design
          5. Arcos Design
          6. Design e Tecnologia
          7. Tríades em Revista
          8. Educação Gráfica""")
        choice = input("Digite o número correspondente: ")
        scraper_mapping = {
            "1": "estudos_em_design",
            "2": "infodesign",
            "3": "repositorio_ufrn",
            "4": "human_factors_in_design",
            "5": "arcos_design",
            "6": "design_e_tecnologia",
            "7": "triades",
            "8": "educacao_grafica"
        }
        scraper_name = scraper_mapping.get(choice)
        if not scraper_name:
            print("Repositório não encontrado.")
            return
        term = input("Insira os termos de pesquisa (máximo 10 palavras): ")
        if not term.strip():
            print("Erro: o termo de pesquisa não pode estar vazio.")
            return
        try:
            max_pages = int(input("Insira o número de páginas para consulta: "))
            if max_pages <= 0:
                raise ValueError
        except ValueError:
            print("Erro: número de páginas deve ser um inteiro positivo.")
            return
        print("Buscando resultados, por favor aguarde...")
        success = run_scraper(scraper_name, term, max_pages)
        if success:
            print(f"Resultados exportados para search_results.csv")
        else:
            print("Nenhum resultado encontrado.")

if __name__ == "__main__":
    main()
