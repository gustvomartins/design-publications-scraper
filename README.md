# 🔍 Design Publications Scraper

Sistema inteligente para coleta automatizada de publicações acadêmicas de Design, UX e Tecnologia de múltiplas bases de dados científicas brasileiras.

## 🏗️ Estrutura do Projeto

```
design-publications-scraper/
├── 📁 src/design_scraper/          # Core do sistema
│   ├── 📁 core/                    # Lógica principal
│   ├── 📁 config/                  # Configurações
│   ├── 📁 scrapers/                # Módulos de scraping
│   └── 📁 utils/                   # Utilitários
├── 📁 cli/                         # Interface de linha de comando
├── 📁 web/                         # Interface web (Streamlit)
├── 📁 docs/                        # Documentação
├── 📁 data/                        # Dados processados
├── 📁 tests/                       # Testes automatizados
└── 📁 requirements.txt             # Dependências Python
```

## 🚀 Como Usar

### 🤖 **Automação (CLI)**
Para execução automatizada e em lote:

```bash
# Pipeline completo
python cli/run.py

# Interface CLI interativa
python cli/run_cli.py

# Teste do sistema de filtros
python cli/test_filtering.py
```

**⚠️ Importante**: Execute sempre a partir do diretório raiz do projeto para que os imports funcionem corretamente.

### 🌐 **Interface Manual (Web)**
Para busca personalizada e exploração:

```bash
# Interface Streamlit
streamlit run web/streamlit_app.py

# Ou usando o script de entrada
python web/run_streamlit.py
```

**⚠️ Importante**: Execute sempre a partir do diretório raiz do projeto para que os imports funcionem corretamente.

**📊 Funcionalidade**: A interface web traz apenas resultados brutos dos scrapers, sem filtros ou deduplicação.

## 📋 Funcionalidades

### 🎯 **Sistema de Filtros Inteligente (Pipeline Automatizado)**
- **Detecção de idioma**: Apenas títulos em português
- **Palavras-chave**: 50+ termos relacionados a UX/Design
- **Transformação**: Estrutura compatível com base de dados

**⚠️ Nota**: Os filtros são aplicados apenas no pipeline automatizado (CLI), não na interface web.

### 🔍 **Deduplicação Automática (Pipeline Automatizado)**
- **Baseado em links**: Identificação única de publicações
- **Não sobrescreve**: Novos registros salvos separadamente
- **Revisão manual**: Controle total sobre atualizações

**⚠️ Nota**: A deduplicação é executada apenas no pipeline automatizado (CLI), não na interface web.

### 📊 **Repositórios Suportados**
- Estudos em Design
- InfoDesign
- Human Factors in Design
- Arcos Design
- Design e Tecnologia
- Tríades em Revista
- Educação Gráfica

## ⚙️ Configuração

### **Pipeline Automatizado**
Edite `src/design_scraper/config/config.yaml`:

```yaml
repos:
  "Estudos em Design": "estudos_em_design"
  "InfoDesign": "infodesign"

terms:
  - "experiencia"
  - "usuario"
  - "interface"

max_pages: 10
```

### **Interface Manual**
Configurações em `src/design_scraper/config/manual_search_config.yaml`

## 📁 Arquivos de Saída

```
data/
├── 📁 raw/
│   ├── base_database.csv          # Base principal
│   └── search_results.csv         # Resultados brutos
└── 📁 processed/
    ├── filtered_results.csv       # Após filtros
    └── new_records.csv           # Novos registros únicos
```

## 🛠️ Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd design-publications-scraper

# Instale as dependências
pip install -r requirements.txt

# Para exportação Excel (opcional)
pip install openpyxl
```

## 🧪 Testes

```bash
# Teste do sistema de filtros
python cli/test_filtering.py

# Teste do pipeline automatizado
python cli/run_cli.py

# Teste da interface web
streamlit run web/streamlit_app.py
```

## 📚 Documentação

- **`docs/ESTRUTURA_PROJETO.md`**: Documentação completa da estrutura
- **`docs/SEPARACAO_RESPONSABILIDADES.md`**: Separação entre CLI e Web
- **`docs/CORRECOES_IMPORTS.md`**: Correções técnicas realizadas
- **`src/design_scraper/`**: Código fonte com documentação inline

## 🔧 Desenvolvimento

### **Estrutura de Módulos**
- **`core/`**: Lógica principal do sistema
- **`scrapers/`**: Implementações específicas de cada repositório
- **`utils/`**: Funções utilitárias compartilhadas
- **`config/`**: Arquivos de configuração

### **Extensibilidade**
- Adicione novos scrapers em `src/design_scraper/scrapers/`
- Configure novos repositórios em `config.yaml`
- Personalize filtros em `utils/data_transformer.py`

## 🔧 Troubleshooting

### **Erro: "No module named 'design_scraper'"**
**Causa**: Imports não conseguem encontrar os módulos
**Solução**: Execute sempre a partir do diretório raiz do projeto

```bash
# ✅ CORRETO: Execute da raiz
cd design-publications-scraper
python cli/run.py

# ❌ INCORRETO: Execute de dentro de cli/
cd cli
python run.py  # Isso vai falhar
```

### **Erro: "ModuleNotFoundError"**
**Causa**: Python não consegue resolver os imports relativos
**Solução**: Todos os scripts já estão configurados com o caminho correto

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs de execução
2. Execute os testes de validação
3. Consulte a documentação em `docs/`
4. Verifique as configurações YAML

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

**🎯 Sistema completo para coleta inteligente de publicações acadêmicas de Design!**