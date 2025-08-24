# 🏗️ Estrutura do Projeto Design Publications Scraper

## 📋 **Visão Geral da Organização**

Este documento detalha a estrutura limpa e organizada do projeto, seguindo as melhores práticas de organização de projetos Python.

## 🎯 **Princípio de Organização**

O projeto foi estruturado seguindo o princípio de **separação clara de responsabilidades**:

- 🤖 **`cli/`**: Automação e execução em lote
- 🌐 **`web/`**: Interface manual e exploração
- 📚 **`src/`**: Core do sistema e lógica de negócio
- 📁 **`data/`**: Dados processados e resultados
- 📖 **`docs/`**: Documentação e guias

## 📁 **Estrutura de Diretórios**

```
design-publications-scraper/
├── 📁 cli/                          # 🤖 Automação e CLI
│   ├── README.md                     # Documentação da CLI
│   ├── run.py                        # Pipeline principal
│   ├── run_cli.py                    # Interface CLI interativa
│   └── test_filtering.py             # Teste do sistema
├── 📁 web/                           # 🌐 Interface Web
│   ├── README.md                     # Documentação da Web
│   ├── streamlit_app.py              # Aplicação Streamlit
│   └── run_streamlit.py              # Script de entrada
├── 📁 src/                           # 📚 Core do Sistema
│   └── 📁 design_scraper/            # Pacote principal
│       ├── 📁 core/                  # Lógica principal
│       │   ├── automated_pipeline.py # Pipeline automatizado
│       │   ├── manual_search.py      # Busca manual
│       │   └── __init__.py
│       ├── 📁 config/                # Configurações
│       │   ├── config.yaml           # Configuração principal
│       │   └── manual_search_config.yaml
│       ├── 📁 scrapers/              # Módulos de scraping
│       │   ├── base_scraper.py       # Classe base
│       │   ├── estudosemdesign_scraper.py
│       │   ├── infodesign_scraper.py
│       │   └── __init__.py
│       ├── 📁 utils/                 # Utilitários
│       │   ├── data_transformer.py   # Filtros e transformação
│       │   ├── deduplication.py      # Deduplicação
│       │   ├── scrapers_factory.py   # Factory de scrapers
│       │   └── __init__.py
│       └── __init__.py
├── 📁 data/                          # 📊 Dados e Resultados
│   ├── 📁 raw/                       # Dados brutos
│   │   ├── base_database.csv         # Base principal
│   │   └── search_results.csv        # Resultados de busca
│   └── 📁 processed/                 # Dados processados
│       ├── filtered_results.csv      # Após filtros
│       └── new_records.csv           # Novos registros
├── 📁 docs/                          # 📖 Documentação
│   ├── README_NEW_STRUCTURE.md       # Documentação da estrutura
│   └── ESTRUTURA_PROJETO.md         # Este arquivo
├── 📁 tests/                         # 🧪 Testes
├── 📁 logs/                          # 📝 Logs de execução
├── 📁 requirements.txt                # Dependências Python
├── 📁 config.yaml                    # Configuração principal
└── 📁 README.md                      # Documentação principal
```

## 🔄 **Fluxo de Dados**

### **Pipeline Automatizado (CLI)**
```
config.yaml → automated_pipeline.py → scrapers → data_transformer.py → deduplication.py → arquivos de saída
```

### **Interface Manual (Web)**
```
streamlit_app.py → manual_search.py → scrapers → filtros → deduplicação → interface de resultados
```

## 🎯 **Separação de Responsabilidades**

### **🤖 Diretório `cli/` - Automação**
- **Propósito**: Execução automatizada e em lote
- **Usuários**: Sistemas, agendadores, produção
- **Características**: 
  - Sem interface gráfica
  - Logs detalhados
  - Configuração via arquivos
  - Execução programada

### **🌐 Diretório `web/` - Interface Manual**
- **Propósito**: Busca personalizada e exploração
- **Usuários**: Pesquisadores, estudantes, profissionais
- **Características**:
  - Interface gráfica intuitiva
  - Configuração interativa
  - Visualização de resultados
  - Download de dados

### **📚 Diretório `src/` - Core do Sistema**
- **Propósito**: Lógica de negócio compartilhada
- **Usuários**: Ambos os cenários (CLI e Web)
- **Características**:
  - Módulos reutilizáveis
  - Configuração centralizada
  - Lógica de scraping
  - Processamento de dados

## 🔧 **Configuração e Personalização**

### **Configuração Principal (`config.yaml`)**
- **Localização**: Raiz do projeto
- **Uso**: Pipeline automatizado
- **Conteúdo**: Repositórios, termos, arquivos de saída

### **Configuração Manual (`manual_search_config.yaml`)**
- **Localização**: `src/design_scraper/config/`
- **Uso**: Interface web
- **Conteúdo**: Limites, opções de interface, configurações de filtros

## 📊 **Gestão de Dados**

### **Diretório `data/raw/`**
- **`base_database.csv`**: Base de dados principal (não modificada automaticamente)
- **`search_results.csv`**: Resultados brutos dos scrapers

### **Diretório `data/processed/`**
- **`filtered_results.csv`**: Resultados após aplicação de filtros
- **`new_records.csv`**: Novos registros únicos (para revisão manual)

## 🧪 **Testes e Validação**

### **Teste do Sistema (`cli/test_filtering.py`)**
- Valida o funcionamento dos filtros
- Testa a transformação de dados
- Verifica a deduplicação
- Gera relatório de funcionamento

### **Testes Unitários (`tests/`)**
- Testes individuais de módulos
- Validação de funcionalidades específicas
- Cobertura de código

## 📝 **Logs e Monitoramento**

### **Diretório `logs/`**
- Logs de execução do pipeline
- Histórico de operações
- Debugging e troubleshooting
- Monitoramento de performance

## 🚀 **Casos de Uso por Diretório**

### **🤖 Use `cli/` quando:**
- Executar buscas em lote
- Agendar execuções automáticas
- Integrar com outros sistemas
- Produção e manutenção

### **🌐 Use `web/` quando:**
- Fazer buscas personalizadas
- Explorar resultados interativamente
- Configurar parâmetros específicos
- Download de dados específicos

### **📚 Use `src/` quando:**
- Desenvolver novas funcionalidades
- Modificar scrapers existentes
- Personalizar filtros e transformações
- Estender o sistema

## 🔄 **Manutenção e Atualizações**

### **Adicionar Novo Scraper**
1. Crie arquivo em `src/design_scraper/scrapers/`
2. Herde de `base_scraper.py`
3. Implemente método `search()`
4. Adicione ao `scrapers_factory.py`
5. Configure em `config.yaml`

### **Modificar Filtros**
1. Edite `src/design_scraper/utils/data_transformer.py`
2. Modifique lista `required_keywords`
3. Ajuste função `is_portuguese_title()`
4. Teste com `cli/test_filtering.py`

### **Personalizar Interface**
1. Edite `web/streamlit_app.py`
2. Modifique `repo_options`
3. Ajuste validações e layout
4. Teste com `streamlit run web/streamlit_app.py`

## 📞 **Suporte e Troubleshooting**

### **Problemas de Importação**
- Execute sempre da raiz do projeto
- Verifique se `src/` está no Python path
- Confirme estrutura de diretórios

### **Problemas de Configuração**
- Verifique `config.yaml` na raiz
- Confirme caminhos dos arquivos
- Valide formato YAML

### **Problemas de Execução**
- Use `cli/test_filtering.py` para validação
- Verifique logs em `logs/`
- Confirme dependências instaladas

---

**🎯 Estrutura limpa e organizada para máxima clareza e manutenibilidade!**
