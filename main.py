from utils.scrapers_factory import ScrapterFactory
from utils.export_csv import export_to_csv

def main():
    print("""Selecione o repositório ou periódico: 
          1. Estudos em Design
          2. InfoDesign
          3. Repositório Institucional UFRN
          4. Human Factors in Design""")
    choice = input("Digite o número correspondente: ")

    # Inicializa o scraper baseado na escolha do usuário
    scraper_mapping = {
        "1": "estudos_em_design",
        "2": "infodesign",
        "3": "repositorio_ufrn",
        "4": "human_factors_in_design"
    }

    scraper_name = scraper_mapping.get(choice)

    if not scraper_name:
        print("Repositório não encontrado.")
        return
    
    #Obtém instância do scraper pela fábrica
    try:
        scraper = ScrapterFactory.get_scraper(scraper_name)
    except ValueError as e:
        print(e)
        return

    # Obtém os termos de pesquisa e número de páginas
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

    # Executa a busca
    print("Buscando resultados, por favor aguarde...")
    try:
        results = scraper.search(term, max_pages)
    except Exception as e:
        print(f"Erro ao realizar a busca: {e}")
        return

    # Verifica os resultados e exporta
    if results:
        csv_filename = "search_results.csv"
        export_to_csv(csv_filename, results, fieldnames=list(results[0].keys()))
        print(f"Resultados exportados para {csv_filename}")
    else:
        print("Nenhum resultado encontrado.")

if __name__ == "__main__":
    main()
