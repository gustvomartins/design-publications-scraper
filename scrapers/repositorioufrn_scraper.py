from bs4 import BeautifulSoup
import requests
from scrapers.base_scraper import BaseScraper

class RepositorioUfrnScraper(BaseScraper):
    def search(self, term, max_pages):
        results = []

        for page in range(max_pages):
            start = page * 100  # Atualizado para 100
            url = (
                f"{self.base_url}?query={term}"
                f"&rpp=100&sort_by=score&order=DESC&etal=0&submit_search=Atualizar&start={str(start)}"
            )

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                for item in soup.find_all("td", attrs={"headers": "t2"}):
                    title_tag = item.find("a")
                    author_tag = item.find_next_sibling("td", attrs={"headers": "t3"})
                    date_tag = item.find_previous_sibling("td", attrs={"headers": "t1"})

                    title = title_tag.get_text() if title_tag else "Sem título"
                    author = author_tag.get_text() if author_tag else "Autor desconhecido"
                    link = title_tag['href'] if title_tag and "href" in title_tag.attrs else "Sem URL"
                    date = date_tag.get_text() if date_tag else "Data não informada"

                    results.append({
                        'title': title, 
                        'author': author, 
                        'link': link, 
                        'date': date
                        })

            else:
                print(f"Erro ao acessar a página {page + 1}: {response.status_code}")
                break

        return results
