# API de Scraping de Periódicos de Design

Este projeto permite realizar buscas em bases de dados de periódicos e repositórios para identificar materiais relacionados ao campo do design. Ele oferece uma interface simples de linha de comando para selecionar o repositório, definir termos de pesquisa e especificar o número de páginas a serem consultadas. Os resultados da busca são exportados para um arquivo CSV.

## Funcionalidades

- **Fábrica de Scrapers:** Uma abordagem unificada para selecionar e utilizar diferentes scrapers com base no repositório escolhido, permitindo maior extensibilidade e organização.
- **Escolha de Periódicos:** Suporte para múltiplos periódicos e repositórios, como:
  - Estudos em Design
  - InfoDesign
  - Repositório Institucional UFRN
  - Human Factors in Design
  - Arcos Design
- **Busca Personalizada:** Insira termos de pesquisa específicos para buscar artigos nos periódicos ou repositórios selecionados.
- **Paginação de Resultados:** Defina o número de páginas a serem consultadas, ajustando a quantidade de resultados retornados.
- **Exportação de Resultados:** Exporte os resultados da pesquisa para um arquivo CSV no formato apropriado.

## Requisitos

- Python 3.x
- Bibliotecas adicionais:
  - `requests` (para realizar requisições HTTP)
  - `beautifulsoup4` (para scraping de dados HTML)
  - `csv` (para exportar os resultados em formato CSV)

## Instalação

1. Clone o repositório ou baixe o código.
2. Instale as dependências necessárias:
   ```
   pip install requests beautifulsoup4
   ```

## Estrutura de Diretórios

A estrutura do projeto é organizada da seguinte forma:

```
.
├── scrapers/
│   ├── __init__.py
│   ├── arcosdesign_scraper.py     # Scraper para Arcos Design
│   ├── base_scraper.py            # Classe base para scrapers
│   ├── estudosemdesign_scraper.py # Scraper para Estudos em Design
│   ├── infodesign_scraper.py      # Scraper para InfoDesign
│   ├── repositorioufrn_scraper.py # Scraper para Repositório Institucional UFRN
│   ├── humanfactorsindesign_scraper.py # Scraper para Human Factors in Design
│   └── template_scraper.py        # Template para novos scrapers
├── utils/
│   ├── __init__.py
│   ├── export_csv.py              # Função para exportar resultados para CSV
│   ├── html_parsing.py            # Função para parsing de HTML
│   ├── scrapers_factory.py        # Função para unificar seleção de scrapers
├── .gitignore                     # Arquivos a serem ignorados pelo Git
├── search_results.csv             # Arquivo CSV com os resultados da busca
├── main.py                        # Script principal para executar o scraping
└── README.md                      # Este arquivo README
```

## Como Usar

1. Execute o script `main.py` no terminal:
   ```
   python main.py
   ```

2. O script solicitará que você escolha um dos repositórios disponíveis:
   - Digite `1` para "Estudos em Design".
   - Digite `2` para "InfoDesign".
   - Digite `3` para "Repositório Institucional UFRN".
   - Digite `4` para "Human Factors in Design".
   - Digite `5` para "Arcos Design"

3. Insira os termos de pesquisa que deseja buscar na base de dados (máximo de 10 palavras). 

4. Especifique o número de páginas a serem consultadas para cada periódico.

5. O script realizará a busca e, se encontrar resultados, exportará os dados para um arquivo CSV.

6. O arquivo CSV será salvo no mesmo diretório onde o script é executado.

## Funções e Componentes

- **Fábrica de Scrapers (`ScraperFactory`)**: 
  - Centraliza a criação dos scrapers e retorna a instância apropriada com base no repositório selecionado.
  - Suporta adição fácil de novos scrapers no futuro.
- **Scrapers Específicos**:
  - `EstudosEmDesignScraper`: Scraper para o periódico "Estudos em Design".
  - `InfoDesignScraper`: Scraper para o periódico "InfoDesign".
  - `RepositorioUfrnScraper`: Scraper para o "Repositório Institucional UFRN".
  - `HumanFactorsinDesignScraper`: Scraper para o periódico "Human Factors in Design".
  - `ArcosDesignScraper`: Scraper para o periódico "Arcos Design"
- **`export_to_csv`**: Função para exportar os resultados obtidos para um arquivo CSV.

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para suas alterações.
3. Submeta um pull request com uma descrição clara do que foi adicionado ou modificado.

## Licença

Este projeto está sob a licença MIT.