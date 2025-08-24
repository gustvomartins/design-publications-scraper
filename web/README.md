# 🌐 Interface Web (Streamlit)

## 🎯 **Busca Manual e Exploração Interativa**

Este diretório contém a interface web para busca personalizada e exploração de resultados.

## 📁 Arquivos Disponíveis

### 🔍 **`streamlit_app.py` - Aplicação Principal**
Interface web completa para busca manual de publicações.

```bash
# Execute a partir do diretório raiz do projeto
streamlit run web/streamlit_app.py
```

**Funcionalidades:**
- ✅ **Seleção múltipla** de repositórios
- ✅ **Configuração flexível** de parâmetros de busca
- ✅ **Resultados brutos** dos scrapers (sem processamento)
- ✅ **Visualização interativa** dos resultados
- ✅ **Download** em CSV e Excel
- ✅ **Estatísticas** por repositório

**⚠️ Importante**: Esta interface traz apenas resultados brutos do scraping. Para filtros e deduplicação, use o pipeline automatizado via CLI.

### 🚀 **`run_streamlit.py` - Script de Entrada**
Script de conveniência para executar a interface web.

```bash
# Execute a partir do diretório raiz do projeto
python web/run_streamlit.py
```

**Funcionalidades:**
- ✅ Configuração automática da porta (8501)
- ✅ Configuração automática do endereço (localhost)
- ✅ Execução simplificada da interface

## 🎨 **Interface do Usuário**

### **Sidebar de Configuração**
- 📚 **Seleção de Repositórios**: Escolha quantos quiser
- 🔍 **Termos de Busca**: Digite suas palavras-chave
- 📄 **Número de Páginas**: Slider de 1 a 50
- 🔄 **Opções de Processamento**: Filtros e deduplicação

### **Área Principal**
- 📊 **Métricas**: Total scraped, resultados finais, filtros aplicados
- 📚 **Gráficos**: Estatísticas por repositório
- 📋 **Tabela de Resultados**: Dados organizados e navegáveis
- 💾 **Download**: Botões para CSV e Excel

## 🚀 **Como Usar**

### **1. Iniciar a Interface**
```bash
# Opção 1: Execução direta
streamlit run web/streamlit_app.py

# Opção 2: Script de entrada
python web/run_streamlit.py
```

### **2. Configurar a Busca**
- ✅ Selecione os repositórios desejados
- 🔍 Digite os termos de busca
- 📄 Ajuste o número de páginas
- 🔄 Configure as opções de processamento

### **3. Executar e Analisar**
- 🚀 Clique em "Executar Busca"
- 📊 Acompanhe o progresso em tempo real
- 📋 Visualize os resultados na tabela
- 💾 Faça download dos dados

## ⚙️ **Configurações Disponíveis**

### **Repositórios Suportados**
- Estudos em Design
- InfoDesign
- Human Factors in Design
- Arcos Design
- Design e Tecnologia
- Tríades em Revista
- Educação Gráfica

### **Processamento**
- **Apenas Scraping**: Resultados brutos dos repositórios
- **Sem Filtros**: Todos os resultados são retornados
- **Sem Deduplicação**: Inclui possíveis duplicatas
- **Dados Originais**: Estrutura original dos scrapers

### **Formatos de Download**
- **CSV**: Compatível com Excel e outras ferramentas
- **Excel**: Se openpyxl estiver instalado
- **Nomes**: Timestamp automático nos arquivos

## 🔧 **Personalização**

### **Modificar Repositórios**
Edite `streamlit_app.py` na seção `repo_options`:

```python
repo_options = {
    "Meu Repositório": "meu_repositorio",
    # ... outros repositórios
}
```

### **Modificar Filtros**
Edite `src/design_scraper/utils/data_transformer.py`:

```python
required_keywords = [
    "minha_palavra_chave",
    # ... outras palavras-chave
]
```

### **Modificar Interface**
- **Temas**: Personalize cores e estilos
- **Layout**: Ajuste colunas e organização
- **Validações**: Modifique regras de entrada

## 🧪 **Testes da Interface**

### **Validação de Funcionalidades**
1. ✅ **Carregamento**: Interface abre sem erros
2. ✅ **Configuração**: Sidebar funcional
3. ✅ **Busca**: Execução de pesquisa
4. ✅ **Resultados**: Exibição de dados
5. ✅ **Download**: Geração de arquivos

### **Teste de Cenários**
- 🔍 **Busca simples**: Um repositório, um termo
- 🔍 **Busca múltipla**: Vários repositórios, vários termos
- 🔍 **Filtros**: Com e sem aplicação de filtros
- 🔍 **Deduplicação**: Com e sem verificação de duplicatas

## 🔧 **Troubleshooting**

### **Erro: "No module named 'design_scraper'"**
**Causa**: Imports não conseguem encontrar os módulos
**Solução**: Execute sempre a partir do diretório raiz do projeto

```bash
# ✅ CORRETO: Execute da raiz
cd design-publications-scraper
streamlit run web/streamlit_app.py

# ❌ INCORRETO: Execute de dentro de web/
cd web
streamlit run streamlit_app.py  # Isso pode falhar
```

### **Como os Imports Funcionam**
Todos os scripts da interface web estão configurados com o caminho correto:

```python
# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

Isso permite que os scripts encontrem os módulos `design_scraper` corretamente.

### **Erro: Interface não carrega**
- Verifique se está no diretório raiz do projeto
- Confirme se Streamlit está instalado: `pip install streamlit`
- Execute: `streamlit run web/streamlit_app.py`

### **Erro: Módulos não encontrados**
- Verifique se todas as dependências estão instaladas
- Execute `pip install -r requirements.txt`
- Confirme se o diretório `src/` existe

### **Erro: Busca falha**
- Verifique a conexão com a internet
- Confirme se os repositórios estão acessíveis
- Verifique os logs de erro na interface

## 📊 **Casos de Uso**

### **Pesquisa Acadêmica**
- 🔍 Exploração de literatura específica (dados brutos)
- 📚 Análise de tendências em design (sem filtros)
- 📊 Coleta de dados para revisões sistemáticas
- 🔍 **Ideal para**: Exploração inicial e análise de dados não processados

### **Desenvolvimento de Produto**
- 🎯 Pesquisa de estado da arte
- 📋 Análise de competidores
- 🔍 Identificação de oportunidades

### **Ensino e Aprendizagem**
- 📚 Material para disciplinas
- 🔍 Exemplos práticos de pesquisa
- 📊 Estudos de caso

## 📞 **Suporte**

Para problemas específicos da interface web:
1. Verifique os logs do Streamlit
2. Confirme se todos os módulos estão funcionando
3. Teste com `python cli/test_filtering.py`
4. Consulte a documentação principal em `../README.md`

---

**🎯 Interface web para busca personalizada e exploração interativa!**
