from scrapers.estudosemdesign_scraper import EstudosEmDesignScraper
from scrapers.infodesign_scraper import InfoDesignScraper
from scrapers.repositorioufrn_scraper import RepositorioUfrnScraper
from utils.export_csv import export_to_csv

def main():
    print("""Selecione o repositório ou periódico: 
          1. Estudos em Design
          2. InfoDesign
          3. Repositório Institucional UFRN""")
    choice = input("Digite o número correspondente: ")

    # Inicializa o scraper baseado na escolha do usuário
    if choice == "1":
        scraper = EstudosEmDesignScraper(base_url="https://estudosemdesign.emnuvens.com.br/design/search/search")
    elif choice == "2":
        scraper = InfoDesignScraper(base_url="https://www.infodesign.org.br/infodesign/search/index")
    elif choice == "3":
        scraper = RepositorioUfrnScraper(base_url="https://repositorio.ufrn.br/simple-search")
    else:
        print("Repositório não encontrado.")
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
