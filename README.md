# API de Scraping de Repositórios de Design

Este script permite realizar buscas nos repositórios "Estudos em Design" e "InfoDesign" para recuperar materiais relacionados ao campo do design. O script oferece uma interface simples de linha de comando para selecionar o repositório, definir termos de pesquisa e especificar o número de páginas a serem consultadas. Os resultados da busca são exportados para um arquivo CSV.

## Funcionalidades

- **Escolha de Repositório:** Permite escolher entre dois repositórios: "Estudos em Design" e "InfoDesign".
- **Busca de Termos:** O usuário pode inserir um termo de pesquisa específico, que será utilizado para buscar artigos nos repositórios selecionados.
- **Paginação de Resultados:** O usuário pode definir o número de páginas a serem consultadas, o que permite ajustar a quantidade de resultados retornados.
- **Exportação de Resultados:** Os resultados da pesquisa são exportados para um arquivo CSV.

## Requisitos

- Python 3.x
- Bibliotecas adicionais:
  - `requests` (para realizar as requisições HTTP)
  - `beautifulsoup4` (para fazer scraping de dados HTML)
  - `csv` (para exportar os resultados em formato CSV)

## Instalação

1. Clone o repositório ou baixe o código.
2. Instale as dependências necessárias:
   ```
   pip install requests beautifulsoup4
   ```

## Estrutura de Diretórios

A estrutura do projeto é a seguinte:

```
.
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py            # Classe base para scrapers
│   ├── blucher_scraper.py         # Scraper para Blucher
│   ├── estudosemdesign_scraper.py # Scraper para Estudos em Design
│   ├── humanfactorsindesign_scraper.py # Scraper para Human Factors in Design
│   ├── infodesign_scraper.py      # Scraper para InfoDesign
│   └── template_scraper.py        # Template para novos scrapers
├── utils/
│   ├── __init__.py
│   ├── export_csv.py              # Função para exportar resultados para CSV
│   ├── html_parsing.py            # Função para parsing de HTML
├── .gitignore                     # Arquivos a serem ignorados pelo Git
├── design_results.csv             # Arquivo CSV com os resultados da busca
├── main.py                        # Script principal para executar o scraping
└── README.md                      # Este arquivo README
```

## Como Usar

1. Execute o script `main.py` no terminal:
   ```
   python main.py
   ```

2. O script irá solicitar que você escolha entre dois repositórios:
   - Digite `1` para "Estudos em Design"
   - Digite `2` para "InfoDesign"
   
3. Insira os termos de pesquisa que deseja buscar nos repositórios.

4. Especifique o número de páginas a serem consultadas para cada repositório.

5. O script realizará a busca e, se encontrar resultados, exportará os dados para um arquivo CSV.

6. O arquivo CSV será salvo no mesmo diretório onde o script é executado.

## Funções

- **`EstudosEmDesignScraper`**: Scraper específico para o repositório "Estudos em Design". 
- **`InfoDesignScraper`**: Scraper específico para o repositório "InfoDesign".
- **`export_to_csv`**: Função responsável por exportar os dados obtidos da busca para um arquivo CSV.

## Contribuindo

Se você quiser contribuir para este projeto, faça um fork, crie sua branch e submeta um pull request com suas alterações. 

## Licença

Este projeto está sob a licença MIT.
