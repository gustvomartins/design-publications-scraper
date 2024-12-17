import requests
from bs4 import BeautifulSoup
import csv

def search_academic_terms(term, max_pages=5):
    base_url = f'https://repositorio.ufrn.br/simple-search?query={term}&rpp=100&sort_by=score&order=DESC&etal=0&submit_search=Atualizar&start='
    results = []
    
    for page in range(max_pages):  # Loop de paginação
        start = page * 100  # O parâmetro "start" muda de 100 em 100 (páginas de 100 resultados)
        url = base_url + str(start)
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            for item in soup.find_all('td', attrs={'headers': 't2'}):  # Altere conforme necessário
                title_tag = item.find('a')
                author_tag = item.find_next_sibling('td', attrs={'headers': 't3'})
                date_tag = item.find_previous_sibling('td', attrs={'headers': 't1'})
                
                title = title_tag.get_text() if title_tag else 'No title'
                author = author_tag.get_text() if author_tag else 'Unknown author'
                link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'No URL'
                date = date_tag.get_text() if date_tag else 'No date'

                results.append({'title': title, 'author': author, 'link': link, 'date': date})
        
        else:
            print(f"Error: {response.status_code} on page {page + 1}")
            break  # Interrompe se houver erro na requisição
    
    return results

# Inputs
term = input("Enter the search term: ")
max_pages = int(input("Enter the number of pages to scrape: "))
search_results = search_academic_terms(term, max_pages)

if isinstance(search_results, list):
    # Export CSV
    csv_file = 'search_results.csv'
    
    with open(csv_file, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'author', 'link', 'date'])
        writer.writeheader()

        for result in search_results:
            writer.writerow(result)
        
    print(f"Results have been saved to {csv_file}")
else:
    print(search_results)  # In case of error, print the error message
