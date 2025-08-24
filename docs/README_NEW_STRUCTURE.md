# 🚀 Design Publications Scraper - Nova Estrutura

Este projeto agora oferece **dois cenários distintos** para scraping de publicações de design:

## 📋 Cenários Disponíveis

### 1. 🔍 **Busca Manual com Interface Streamlit**
- Interface web interativa
- Seleção múltipla de bases de dados
- Configuração personalizada de filtros
- Download em CSV e Excel
- Visualização em tempo real dos resultados

### 2. 🤖 **Pipeline Automatizado**
- Execução automática baseada em configuração YAML
- Processamento em lote
- Integração com sistemas automatizados
- Logs detalhados de execução

## 🏗️ Nova Estrutura do Projeto

```
design-publications-scraper/
├── 📁 src/design_scraper/
│   ├── 📁 core/
│   │   ├── 🔍 main.py                    # Interface Streamlit
│   │   ├── 🤖 automated_pipeline.py      # Pipeline automatizado
│   │   ├── 🔗 pipeline.py                # Interface unificada
│   │   └── 🔍 manual_search.py           # Lógica de busca manual
│   ├── 📁 config/
│   │   ├── config.yaml                   # Configuração do pipeline
│   │   └── manual_search_config.yaml     # Configuração da busca manual
│   ├── 📁 scrapers/                      # Módulos de scraping
│   └── 📁 utils/                         # Utilitários compartilhados
├── 🚀 run.py                             # Pipeline automatizado
├── 🖥️ run_cli.py                         # Pipeline CLI
├── 🌐 run_streamlit.py                   # Interface Streamlit
└── 🧪 test_filtering.py                  # Testes do sistema
```

## 🚀 Como Usar

### 🌐 **Interface Streamlit (Busca Manual)**

#### Opção 1: Execução direta
```bash
streamlit run src/design_scraper/core/main.py
```

#### Opção 2: Script dedicado
```bash
python run_streamlit.py
```

#### Características:
- ✅ **Seleção múltipla** de repositórios
- ✅ **Configuração flexível** de parâmetros
- ✅ **Filtros opcionais** (idioma + palavras-chave)
- ✅ **Deduplicação opcional**
- ✅ **Download em CSV e Excel**
- ✅ **Visualização interativa** dos resultados
- ✅ **Estatísticas por repositório**

### 🤖 **Pipeline Automatizado**

#### Opção 1: Script principal
```bash
python run.py
```

#### Opção 2: Interface CLI
```bash
python run_cli.py
```

#### Opção 3: Execução direta
```bash
python src/design_scraper/core/automated_pipeline.py
```

#### Características:
- ✅ **Execução automática** baseada em configuração
- ✅ **Processamento em lote** de múltiplos repositórios
- ✅ **Logs detalhados** de execução
- ✅ **Integração** com sistemas automatizados
- ✅ **Configuração via YAML**

## ⚙️ Configuração

### 📊 **Pipeline Automatizado** (`src/design_scraper/config/config.yaml`)
```yaml
repos:
  "Estudos em Design": "estudos_em_design"
  "InfoDesign": "infodesign"
  # ... outros repositórios

terms:
  - "experiencia"
  - "usuario"
  - "interface"
  # ... outros termos

max_pages: 10

raw_results_filename: "data/raw/search_results.csv"
filtered_results_filename: "data/processed/filtered_results.csv"
new_records_filename: "data/processed/new_records.csv"
```

### 🔍 **Busca Manual** (`src/design_scraper/config/manual_search_config.yaml`)
```yaml
manual_search:
  default_max_pages: 10
  default_apply_filters: true
  default_run_dedup: true
  max_pages_limit: 50
  max_results_display: 100
  # ... outras configurações
```

## 🔄 Fluxo de Trabalho

### 🌐 **Busca Manual (Streamlit)**
1. **Configuração**: Seleção de repositórios e parâmetros
2. **Execução**: Scraping dos repositórios selecionados
3. **Processamento**: Filtros e deduplicação (opcional)
4. **Visualização**: Resultados em tabela interativa
5. **Download**: Exportação em CSV ou Excel

### 🤖 **Pipeline Automatizado**
1. **Configuração**: Carregamento do arquivo YAML
2. **Execução**: Scraping automático de todos os repositórios
3. **Processamento**: Filtros e deduplicação automáticos
4. **Saída**: Arquivos CSV organizados por etapa
5. **Logs**: Relatório detalhado de execução

## 📊 Funcionalidades Compartilhadas

### 🎯 **Sistema de Filtros**
- **Detecção de idioma**: Apenas títulos em português
- **Filtros de palavras-chave**: 50+ termos relacionados a UX/Design
- **Transformação de dados**: Estrutura compatível com base de dados

### 🔍 **Sistema de Deduplicação**
- **Baseado em links**: Identificação única de publicações
- **Não automático**: Novos registros salvos separadamente
- **Revisão manual**: Controle total sobre atualizações

### 📁 **Estrutura de Arquivos**
```
data/
├── 📁 raw/
│   ├── base_database.csv          # Base de dados principal
│   └── search_results.csv         # Resultados brutos
└── 📁 processed/
    ├── filtered_results.csv       # Resultados filtrados
    └── new_records.csv           # Novos registros únicos
```

## 🛠️ Instalação e Dependências

### 📦 **Dependências Principais**
```bash
pip install -r requirements.txt
```

### 📊 **Dependências Opcionais**
```bash
# Para exportação Excel
pip install openpyxl

# Para interface Streamlit
pip install streamlit
```

## 🧪 Testes

### 🔍 **Teste do Sistema de Filtros**
```bash
python test_filtering.py
```

### 🤖 **Teste do Pipeline Automatizado**
```bash
python run_cli.py
```

### 🌐 **Teste da Interface Streamlit**
```bash
python run_streamlit.py
```

## 📈 Vantagens da Nova Estrutura

### ✅ **Separação de Responsabilidades**
- Interface Streamlit focada na experiência do usuário
- Pipeline automatizado para execução em lote
- Módulos reutilizáveis e testáveis

### ✅ **Flexibilidade**
- Busca manual para exploração e pesquisa
- Pipeline automatizado para produção e integração
- Configuração independente para cada cenário

### ✅ **Manutenibilidade**
- Código organizado e modular
- Configurações centralizadas
- Fácil extensão de funcionalidades

### ✅ **Escalabilidade**
- Suporte a múltiplos repositórios
- Processamento em lote eficiente
- Integração com sistemas externos

## 🚀 Próximos Passos

### 🔮 **Funcionalidades Futuras**
- [ ] API REST para integração
- [ ] Dashboard de métricas
- [ ] Agendamento de execuções
- [ ] Notificações por email
- [ ] Integração com bases de dados externas

### 🛠️ **Melhorias Técnicas**
- [ ] Cache de resultados
- [ ] Processamento paralelo
- [ ] Validação de dados
- [ ] Testes automatizados
- [ ] Documentação da API

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs de execução
2. Execute os testes de validação
3. Consulte a documentação específica de cada módulo
4. Verifique as configurações YAML

---

**🎯 A nova estrutura oferece o melhor dos dois mundos: flexibilidade para pesquisa manual e automação para produção!**
