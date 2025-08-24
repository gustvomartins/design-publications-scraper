from bs4 import BeautifulSoup
import requests
from scrapers.base_scraper import BaseScraper

class EstudosEmDesignScraper(BaseScraper):
    def search(self, term, max_pages=5):
        results = []

        for page in range(max_pages):
            # Formata a URL com o termo de pesquisa
            url = (
                f"{self.base_url}?query={term}&searchJournal=1&authors=&title=&abstract=&galleyFullText=&suppFiles=&discipline=&subject=&type=&coverage=&indexTerms=&dateFromMonth=&dateFromDay=&dateFromYear=&dateToMonth=&dateToDay=&dateToYear=&orderBy=&orderDir=&searchPage={page + 1}#results"
            )
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Seleciona as linhas da tabela
                rows = soup.select("table.listing > tr[valign='top']")

                for row in rows:
                    # Edição: Pegando o link e texto da edição
                    edition_tag = row.select_one("td:nth-child(1) a")
                    edition = edition_tag.get_text(strip=True) if edition_tag else "Edição não informada"
                    edition_link = edition_tag["href"] if edition_tag else "Sem link"

                    # Título: Captura o título do artigo
                    title_tag = row.select_one("td:nth-child(2)")
                    title = title_tag.get_text(strip=True) if title_tag else "Título não informado"

                    # Autor: Extrai o autor, presente na linha abaixo (com colspan)
                    author_tag = row.find_next_sibling("tr")
                    author = author_tag.get_text(strip=True) if author_tag else "Autor desconhecido"

                    # Links adicionais (Resumo, PDF): Identifica os links presentes
                    links_tag = row.select("td:nth-child(3) a")
                    resumo_link = None
                    pdf_link = None
                    for link in links_tag:
                        if "article/view" in link["href"]:
                            resumo_link = link["href"]
                        elif "article/view" in link["href"]:
                            pdf_link = link["href"]
                    
                    results.append({
                        "title": title,
                        "author": author,
                        "edition": edition,
                        "edition_link": edition_link,
                        "resumo_link": resumo_link or "Sem resumo",
                        "pdf_link": pdf_link or "Sem PDF"
                    })
            else:
                print(f"Erro ao acessar a página {page + 1}: {response.status_code}")
                break

        return results
