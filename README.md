# Design Publications Scraper

Um sistema de web scraping para coletar publicações acadêmicas relacionadas ao design de diversos repositórios digitais.

## 📁 Estrutura do Projeto

```
design-publications-scraper/
├── 📁 scrapers/           # Módulos de scraping específicos
│   ├── base_scraper.py    # Classe base para todos os scrapers
│   ├── arcosdesign_scraper.py
│   ├── designetecnologia_scraper.py
│   ├── educacaografica_scraper.py
│   ├── estudosemdesign_scraper.py
│   ├── humanfactorsindesign_scraper.py
│   ├── infodesign_scraper.py

│   ├── triades_scraper.py
│   └── template_scraper.py
├── 📁 utils/              # Utilitários e helpers
│   ├── scrapers_factory.py
│   ├── export_csv.py
│   ├── html_parsing.py
│   └── deduplication.py   # Sistema de deduplicação
├── 📁 configs/            # Arquivos de configuração
│   └── config.yaml        # Configurações principais
├── 📁 data/               # Dados coletados e processados
│   ├── raw/               # Dados brutos (CSV, arquivos de saída)
│   └── processed/         # Dados processados e limpos
├── 📁 logs/               # Logs de execução
├── 📁 tests/              # Testes unitários e de integração
├── 📁 docs/               # Documentação adicional
├── main.py                 # Ponto de entrada principal
├── pipeline.py             # Pipeline de execução dos scrapers
├── deduplicate.py          # Script standalone de deduplicação
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd design-publications-scraper
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Edite o arquivo `configs/config.yaml` para configurar:
- **terms**: Termos de busca
- **repos**: Repositórios a serem consultados
- **max_pages**: Número máximo de páginas por busca
- **csv_filename**: Nome do arquivo de saída

## 🎯 Uso

### Execução via Pipeline
```bash
python pipeline.py
```

### Execução via Main
```bash
python main.py
```

### Deduplicação
```bash
# Deduplicação automática (via pipeline)
python pipeline.py

# Deduplicação manual
python deduplicate.py

# Criar nova base de dados
python deduplicate.py --create-base
```

## 📊 Repositórios Suportados

- **estudos_em_design**: Estudos em Design
- **infodesign**: InfoDesign

- **human_factors_in_design**: Human Factors in Design
- **arcos_design**: Arcos Design
- **design_e_tecnologia**: Design e Tecnologia
- **triades**: Triades
- **educacao_grafica**: Educação Gráfica

## 🔧 Desenvolvimento

### Adicionando um Novo Scraper

1. Crie um novo arquivo em `scrapers/`
2. Herde de `base_scraper.py`
3. Implemente o método `search()`
4. Adicione o scraper ao `ScrapterFactory`
5. Configure no `config.yaml`

### Estrutura de um Scraper

```python
from scrapers.base_scraper import BaseScraper

class MeuScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://exemplo.com")
    
    def search(self, term, max_pages=5):
        # Implementar lógica de busca
        pass
```

## 📝 Logs e Deduplicação

Os logs de execução são salvos na pasta `logs/` para facilitar o debug e monitoramento.

### Sistema de Deduplicação
O projeto inclui um sistema inteligente de deduplicação que:
- Compara novos resultados com uma base de dados existente
- Identifica apenas registros realmente novos
- Atualiza automaticamente a base de dados
- Gera relatórios de estatísticas
- Evita duplicatas baseado no campo `link` dos artigos

## 🧪 Testes

Execute os testes na pasta `tests/`:
```bash
python -m pytest tests/
```

## 📄 Licença

Este projeto está sob a licença MIT.