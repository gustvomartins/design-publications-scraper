from bs4 import BeautifulSoup
import requests
from scrapers.base_scraper import BaseScraper

class TemplateRepoScraper(BaseScraper):
    def search(self, term, max_pages=5):
    
        results = []

        for page in range(max_pages):
            url = f"{self.base_url}?search={term}&page={page+1}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.contet, "htmlparser")

                for item in soup.select(".result-item"):
                    title_tag = item.find("h3")
                    author_tag = item.find("p", class_="author")
                    date_tag = item.find("p", class_="date")

                    title = title_tag.get_text(strip=True) if title_tag else "Sem título"
                    author = author_tag.get_text(strip=True) if author_tag else "Autor desconhecido"
                    link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "Sem URL"
                    date = date_tag.get_text(strip=True) if date_tag else "Data não informada"

                    results.append({
                        "title": title,
                        "author": author,
                        "link": link,
                        "date": date,
                    })
            
            else:
                print(f"Errro ao acessar a página {page + 1}: {response.status_code}")
                break

        return results