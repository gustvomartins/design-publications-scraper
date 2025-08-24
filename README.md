# Design Publications Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Sistema profissional de scraping e catalogação de publicações de design e UX com filtragem inteligente para curadoria.

## 🎯 Visão Geral

O **Design Publications Scraper** é um sistema robusto e escalável para coleta, transformação e filtragem de publicações acadêmicas relacionadas a design e UX. O sistema implementa:

- **Scraping inteligente** de múltiplas fontes acadêmicas
- **Transformação automática** de dados para formato padronizado
- **Filtragem rigorosa** por relevância e idioma português
- **Pipeline integrado** com todas as etapas automatizadas
- **Interface de linha de comando** profissional
- **Sistema de testes** abrangente

## 🏗️ Estrutura do Projeto

```
design-publications-scraper/
├── src/design_scraper/           # Código fonte principal
│   ├── core/                     # Funcionalidades principais
│   │   ├── pipeline.py          # Pipeline principal
│   │   ├── transformer.py       # Transformação de dados
│   │   └── filter.py            # Filtragem de conteúdo
│   ├── scrapers/                 # Scrapers web
│   │   ├── base_scraper.py      # Classe base abstrata
│   │   ├── estudosemdesign_scraper.py
│   │   ├── infodesign_scraper.py
│   │   └── ...                  # Outros scrapers
│   ├── utils/                    # Utilitários
│   │   ├── scrapers_factory.py  # Factory para scrapers
│   │   ├── deduplication.py     # Lógica de deduplicação
│   │   └── export_csv.py        # Exportação de dados
│   ├── config/                   # Gerenciamento de configuração
│   │   ├── config_manager.py    # Gerenciador de configuração
│   │   └── defaults.py          # Configurações padrão
│   └── cli/                     # Interface de linha de comando
│       └── main.py              # CLI principal
├── tests/                        # Testes automatizados
│   ├── unit/                     # Testes unitários
│   ├── integration/              # Testes de integração
│   └── conftest.py              # Configuração do pytest
├── docs/                         # Documentação
│   ├── api/                      # Documentação da API
│   ├── user_guide/               # Guia do usuário
│   └── developer_guide/          # Guia do desenvolvedor
├── examples/                     # Exemplos de uso
├── scripts/                      # Scripts utilitários
├── configs/                      # Arquivos de configuração
├── data/                         # Dados e resultados
├── pyproject.toml               # Configuração do projeto
├── requirements.txt              # Dependências
└── README.md                    # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação do Projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/design-publications/scraper.git
   cd design-publications-scraper
   ```

2. **Instale o projeto em modo desenvolvimento:**
   ```bash
   pip install -e .
   ```

3. **Instale as dependências de desenvolvimento (opcional):**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Instale as dependências de documentação (opcional):**
   ```bash
   pip install -e ".[docs]"
   ```

## 💻 Uso

### Interface de Linha de Comando

O sistema oferece uma CLI profissional com comandos intuitivos:

#### Executar Pipeline Completo
```bash
# Executar com configuração padrão
design-scraper run

# Executar com configuração personalizada
design-scraper run --config configs/my_config.yaml
```

#### Transformar Dados Apenas
```bash
# Transformar resultados de busca
design-scraper transform input.csv output.csv

# Transformar com validação de base de dados
design-scraper transform input.csv output.csv --base-db base.csv
```

#### Filtrar Conteúdo para Curadoria
```bash
# Filtrar dados transformados
design-scraper filter transformed.csv curation.csv
```

#### Gerenciar Configuração
```bash
# Mostrar configuração atual
design-scraper config show

# Validar arquivo de configuração
design-scraper config validate
```

#### Obter Ajuda
```bash
# Ajuda geral
design-scraper --help

# Ajuda específica de comando
design-scraper run --help
```

### Uso como Módulo Python

```python
from design_scraper.core import Pipeline, DataTransformer, ContentFilter

# Executar pipeline completo
pipeline = Pipeline("configs/config.yaml")
pipeline.run_all_scrapers()

# Transformar dados
transformer = DataTransformer()
transformed_data = transformer.transform_and_save_results(
    "input.csv", "output.csv"
)

# Filtrar conteúdo
filter_tool = ContentFilter()
curation_data = filter_tool.filter_and_save_for_curation(
    "transformed.csv", "curation.csv"
)
```

### Executar como Módulo

```bash
# Executar pipeline completo
python -m design_scraper run

# Executar comando específico
python -m design_scraper transform input.csv output.csv
```

## ⚙️ Configuração

### Arquivo de Configuração

O sistema usa arquivos YAML para configuração:

```yaml
# configs/config.yaml
repos:
  estudos_em_design: estudos_em_design
  infodesign: infodesign
  human_factors_in_design: human_factors_in_design
  arcos_design: arcos_design
  design_e_tecnologia: design_e_tecnologia
  triades: triades
  educacao_grafica: educacao_grafica

terms:
  - "experiencia"
  - "usuario"
  - "interface"
  - "usabilidade"
  - "interacao"
  - "sistema"
  - "ergonomia"
  - "digital"
  - "informacao"
  - "tecnologia"

max_pages: 10
csv_filename: "data/raw/search_results.csv"

data_processing:
  transformed_results: "data/processed/transformed_results.csv"
  enable_auto_transform: true

curation:
  curation_candidates: "data/processed/curation_candidates.csv"
  enable_auto_filtering: true

deduplication:
  base_database: "data/raw/base_database.csv"
  new_records_output: "data/processed/new_records.csv"
  enable_auto_dedup: true
```

### Configurações Avançadas

O sistema suporta configurações avançadas para:

- **Scrapers**: URLs, delays, timeouts
- **Processamento**: Tamanho de lote, workers, tentativas
- **Filtragem**: Pontuação mínima, padrões de exclusão
- **Saída**: Encoding, formato de data, metadados

## 🧪 Testes

### Executar Testes

```bash
# Executar todos os testes
pytest

# Executar testes unitários
pytest tests/unit/

# Executar testes de integração
pytest tests/integration/

# Executar com cobertura
pytest --cov=src/design_scraper

# Executar testes específicos
pytest tests/unit/test_transformer.py::TestDataTransformer::test_transform_search_results
```

### Configuração de Testes

O projeto usa:
- **pytest** como framework de testes
- **pytest-cov** para cobertura de código
- **unittest.mock** para mocks e stubs
- **Fixtures** para dados de teste reutilizáveis

## 📚 Documentação

### Documentação da API

```bash
# Gerar documentação da API
cd docs/api
make html
```

### Guias do Usuário

- **Guia de Filtragem**: `docs/user_guide/curation_filtering_guide.md`
- **Resumo do Sistema**: `docs/developer_guide/complete_system_summary.md`
- **Guia de Transformação**: `docs/developer_guide/transformation_summary.md`

### Documentação do Desenvolvedor

- **Estrutura do Projeto**: Este README
- **Padrões de Código**: Configurações do Black, Flake8, MyPy
- **Arquitetura**: Organização dos módulos e classes

## 🔧 Desenvolvimento

### Padrões de Código

O projeto segue as melhores práticas de Python:

- **Black** para formatação de código
- **Flake8** para linting
- **MyPy** para verificação de tipos
- **Pre-commit** para hooks de qualidade

### Configuração de Desenvolvimento

```bash
# Instalar hooks de pre-commit
pre-commit install

# Formatar código
black src/ tests/

# Verificar tipos
mypy src/

# Executar linting
flake8 src/ tests/
```

### Estrutura de Commits

Usamos commits semânticos:
- `feat:` novas funcionalidades
- `fix:` correções de bugs
- `docs:` documentação
- `test:` testes
- `refactor:` refatoração
- `style:` formatação

## 📊 Funcionalidades

### 🕷️ Scraping Inteligente

- **Múltiplas fontes**: 7 revistas acadêmicas brasileiras
- **Scrapers especializados**: Cada fonte tem seu scraper otimizado
- **Controle de taxa**: Delays configuráveis para evitar bloqueios
- **Tratamento de erros**: Recuperação robusta de falhas

### 🔄 Transformação de Dados

- **Estrutura padronizada**: Conversão automática para formato base
- **Extração de anos**: Inteligente de campos date/edition
- **Mapeamento de categorias**: Baseado em termos de busca
- **Validação automática**: Verificação de integridade dos dados

### 🔍 Filtragem para Curadoria

- **Termos específicos**: 50+ termos de UX/Design (configuráveis)
- **Sistema de pontuação**: Bônus para termos de alta relevância
- **Detecção de idioma**: Português com fallback por padrões
- **Exclusão automática**: Spam e conteúdo irrelevante

### 📈 Pipeline Integrado

- **Orquestração automática**: Todas as etapas integradas
- **Configuração flexível**: YAML com validação
- **Logs detalhados**: Monitoramento completo do processo
- **Tratamento de erros**: Continuação robusta em caso de falhas

## 🎯 Casos de Uso

### Pesquisadores Acadêmicos

- Coleta sistemática de publicações
- Filtragem por relevância temática
- Catalogação padronizada
- Análise de tendências

### Bibliotecários e Curadores

- Triagem automática de conteúdo
- Priorização por relevância
- Validação de idioma
- Preparação para catalogação

### Desenvolvedores

- Sistema modular e extensível
- API limpa e documentada
- Testes abrangentes
- Configuração flexível

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Diretrizes de Contribuição

- Siga os padrões de código estabelecidos
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Use commits semânticos
- Mantenha a compatibilidade com versões anteriores

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Comunidade Python** por ferramentas e bibliotecas
- **Acadêmicos de Design** por feedback e validação
- **Contribuidores** por melhorias e sugestões

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/design-publications/scraper/issues)
- **Documentação**: [Documentação Online](https://design-publications-scraper.readthedocs.io/)
- **Email**: team@design-publications.com

---

**Design Publications Scraper** - Transformando a coleta e catalogação de publicações acadêmicas de design e UX. 🎨📚