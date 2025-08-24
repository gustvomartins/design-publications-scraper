# 🎯 Separação de Responsabilidades - Design Publications Scraper

## 📋 **Visão Geral**

Este documento explica a separação clara de responsabilidades entre as duas interfaces do sistema:

1. **🤖 Pipeline Automatizado (CLI)** - Processamento completo
2. **🌐 Interface Web (Streamlit)** - Apenas scraping bruto

## 🔄 **Fluxo de Dados**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Repositórios  │───▶│   Scrapers      │───▶│  Resultados     │
│   Acadêmicos    │    │   (CLI + Web)   │    │   Brutos        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Pipeline Automatizado │
                    │   (CLI Apenas)         │
                    │                         │
                    │ 1. Filtros (idioma)    │
                    │ 2. Palavras-chave      │
                    │ 3. Deduplicação        │
                    │ 4. Transformação       │
                    └─────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │   Resultados Finais    │
                    │   (Processados)        │
                    └─────────────────────────┘
```

## 🤖 **Pipeline Automatizado (CLI)**

### **Responsabilidades**
- ✅ **Scraping completo** de todos os repositórios configurados
- ✅ **Aplicação de filtros** (idioma português + palavras-chave)
- ✅ **Deduplicação** contra base de dados existente
- ✅ **Transformação** para estrutura padrão
- ✅ **Salvamento** de arquivos processados
- ✅ **Relatórios** detalhados de execução

### **Comandos Disponíveis**
```bash
# Pipeline completo
python cli/run.py

# Interface CLI interativa
python cli/run_cli.py

# Teste do sistema
python cli/test_filtering.py
```

### **Arquivos Gerados**
- `data/raw/search_results.csv` - Resultados brutos
- `data/processed/filtered_results.csv` - Após filtros
- `data/processed/new_records.csv` - Novos registros únicos

### **Casos de Uso**
- 🔄 **Produção automatizada** (cron, agendamento)
- 📊 **Processamento em lote** de grandes volumes
- 🔍 **Análise completa** com filtros e deduplicação
- 💾 **Atualização** da base de dados principal

## 🌐 **Interface Web (Streamlit)**

### **Responsabilidades**
- ✅ **Scraping sob demanda** de repositórios selecionados
- ✅ **Resultados brutos** sem processamento
- ✅ **Visualização interativa** dos dados
- ✅ **Download** em CSV e Excel
- ✅ **Exploração rápida** de dados

### **Comandos Disponíveis**
```bash
# Interface web
streamlit run web/streamlit_app.py

# Script de entrada
python web/run_streamlit.py
```

### **Arquivos Gerados**
- **Nenhum arquivo salvo** automaticamente
- **Download manual** dos resultados
- **Dados temporários** durante a sessão

### **Casos de Uso**
- 🔍 **Exploração inicial** de literatura
- 📚 **Pesquisa acadêmica** rápida
- 🎯 **Análise exploratória** de dados
- 📊 **Verificação** de disponibilidade de dados

## 🔍 **Diferenças Técnicas**

### **Pipeline CLI**
```python
# Aplica filtros e deduplicação
results = searcher.search_publications(
    selected_repos, repo_options, term, max_pages,
    apply_filters=True,  # ✅ Sempre True
    run_dedup=True       # ✅ Sempre True
)
```

### **Interface Web**
```python
# Apenas scraping bruto
results = searcher.search_publications_raw(
    selected_repos, repo_options, term, max_pages
    # ❌ Sem filtros
    # ❌ Sem deduplicação
)
```

## 📊 **Comparação de Resultados**

| Aspecto | Pipeline CLI | Interface Web |
|---------|--------------|---------------|
| **Filtros** | ✅ Aplicados | ❌ Não aplicados |
| **Deduplicação** | ✅ Executada | ❌ Não executada |
| **Transformação** | ✅ Estrutura padrão | ❌ Estrutura original |
| **Volume** | 🔄 Todos os repositórios | 🎯 Repositórios selecionados |
| **Velocidade** | 🐌 Processamento completo | ⚡ Scraping rápido |
| **Persistência** | 💾 Arquivos salvos | 📤 Download manual |

## 🎯 **Quando Usar Cada Interface**

### **Use Pipeline CLI quando:**
- 🔄 **Automatizar** coleta de dados
- 📊 **Processar** grandes volumes
- 🎯 **Aplicar filtros** específicos
- 💾 **Atualizar** base de dados
- 📈 **Gerar relatórios** completos

### **Use Interface Web quando:**
- 🔍 **Explorar** dados rapidamente
- 📚 **Pesquisar** tópicos específicos
- 🎯 **Verificar** disponibilidade de dados
- 📊 **Analisar** tendências iniciais
- 🚀 **Prototipar** pesquisas

## 🔧 **Implementação Técnica**

### **Classe ManualSearch**
```python
class ManualSearch:
    def search_publications_raw(self, ...):
        """Apenas scraping - sem processamento"""
        # Retorna resultados brutos
        
    def search_publications(self, ...):
        """Processamento completo - com filtros e dedup"""
        # Aplica filtros e deduplicação
```

### **Separação de Métodos**
- **`search_publications_raw()`** - Interface web
- **`search_publications()`** - Pipeline CLI
- **Métodos compartilhados** - Export, configuração

## 📈 **Benefícios da Separação**

### **✅ Performance**
- **Interface web**: Resposta rápida para exploração
- **Pipeline CLI**: Processamento otimizado para volumes

### **✅ Manutenibilidade**
- **Código separado** para cada responsabilidade
- **Testes independentes** de cada funcionalidade
- **Debugging focado** em problemas específicos

### **✅ Usabilidade**
- **Interface web**: Simples e rápida para usuários finais
- **Pipeline CLI**: Robusto e completo para automação

### **✅ Escalabilidade**
- **Interface web**: Pode ser executada em paralelo
- **Pipeline CLI**: Pode ser agendado e monitorado

## 🔮 **Futuras Melhorias**

### **Interface Web**
- 📊 **Filtros básicos** (opcional)
- 🔍 **Busca avançada** por campos
- 📈 **Gráficos interativos** dos resultados

### **Pipeline CLI**
- 🤖 **Machine Learning** para filtros inteligentes
- 📊 **Métricas avançadas** de qualidade
- 🔄 **Sincronização** com bases externas

## 📞 **Suporte e Troubleshooting**

### **Problemas com Interface Web**
1. Verifique se está executando da raiz do projeto
2. Confirme se Streamlit está instalado
3. Execute `python cli/test_filtering.py` para validar scrapers

### **Problemas com Pipeline CLI**
1. Verifique configuração em `config.yaml`
2. Confirme se diretório `data/` existe
3. Execute `python cli/run_cli.py` para status detalhado

---

**🎯 Separação clara de responsabilidades para máxima eficiência e usabilidade!**

**📅 Data**: 24/08/2025
**🔧 Status**: ✅ Implementado com sucesso
**📊 Resultado**: Sistema mais organizado e eficiente
