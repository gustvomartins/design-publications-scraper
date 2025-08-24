# 🤖 Interface de Linha de Comando (CLI)

## 🎯 **Automação e Execução em Lote**

Este diretório contém todas as ferramentas para execução automatizada do sistema de scraping **com processamento completo** (filtros + deduplicação).

**⚠️ Importante**: A CLI é responsável por todo o processamento dos dados. A interface web traz apenas resultados brutos.

## 📁 Arquivos Disponíveis

### 🚀 **`run.py` - Pipeline Principal**
Executa o pipeline completo de scraping, filtragem e deduplicação.

```bash
# Execute a partir do diretório raiz do projeto
python cli/run.py
```

**Funcionalidades:**
- ✅ **Scraping automático** de todos os repositórios configurados
- ✅ **Aplicação automática de filtros** (idioma + palavras-chave)
- ✅ **Deduplicação automática** contra base existente
- ✅ **Transformação** para estrutura padrão
- ✅ **Geração de relatórios** detalhados
- ✅ **Salvamento organizado** de arquivos

**🎯 Responsabilidade**: Processamento completo dos dados (única interface que aplica filtros e deduplicação)

### 🖥️ **`run_cli.py` - Interface CLI Interativa**
Interface de linha de comando com status e monitoramento.

```bash
# Execute a partir do diretório raiz do projeto
python cli/run_cli.py
```

**Funcionalidades:**
- ✅ Status do pipeline em tempo real
- ✅ Configuração validada antes da execução
- ✅ Logs detalhados de cada etapa
- ✅ Relatório final com estatísticas
- ✅ Tratamento de erros robusto

### 🧪 **`test_filtering.py` - Teste do Sistema**
Valida o funcionamento dos filtros e transformação de dados.

```bash
# Execute a partir do diretório raiz do projeto
python cli/test_filtering.py
```

**Funcionalidades:**
- ✅ Teste do sistema de filtros
- ✅ Validação da transformação de dados
- ✅ Verificação da deduplicação
- ✅ Relatório de funcionamento

## ⚙️ **Configuração**

Edite o arquivo `config.yaml` na raiz do projeto para:

- **Repositórios**: Escolha quais bases de dados usar
- **Termos**: Defina as palavras-chave para busca
- **Páginas**: Configure o número máximo de páginas por busca
- **Arquivos**: Personalize os nomes dos arquivos de saída

## 🔄 **Fluxo de Execução**

```
1. 📚 Carregamento de configuração
2. 🔍 Scraping de repositórios
3. 🎯 Aplicação de filtros
4. 🔄 Deduplicação
5. 💾 Salvamento de resultados
6. 📊 Relatório final
```

## 📊 **Arquivos Gerados**

- `data/raw/search_results.csv` - Resultados brutos
- `data/processed/filtered_results.csv` - Após filtros
- `data/processed/new_records.csv` - Novos registros únicos

## 🚀 **Casos de Uso**

### **Produção Automatizada**
```bash
# Agendamento via cron (Linux/Mac)
0 2 * * * cd /path/to/project && python cli/run.py

# Agendamento via Task Scheduler (Windows)
# Configure para executar python cli/run.py diariamente
```

### **Integração com Sistemas**
```bash
# Execução via script externo
python cli/run.py > logs/execution_$(date +%Y%m%d).log 2>&1

# Verificação de status
python cli/run_cli.py --status-only
```

### **Testes e Validação**
```bash
# Teste completo do sistema
python cli/test_filtering.py

# Validação de configuração
python cli/run_cli.py --validate-config
```

## 🔧 **Troubleshooting**

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

### **Como os Imports Funcionam**
Todos os scripts da CLI estão configurados com o caminho correto:

```python
# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

Isso permite que os scripts encontrem os módulos `design_scraper` corretamente.

### **Erro: Configuração não encontrada**
- Verifique se `config.yaml` existe na raiz do projeto
- Confirme se os caminhos dos arquivos estão corretos

### **Erro: Módulos não encontrados**
- Execute a partir do diretório raiz do projeto
- Verifique se todas as dependências estão instaladas

### **Erro: Arquivos de saída não criados**
- Verifique se o diretório `data/` existe
- Confirme permissões de escrita no diretório

## 📞 **Suporte**

Para problemas específicos da CLI:
1. Verifique os logs de execução
2. Execute `python cli/run_cli.py` para status detalhado
3. Use `python cli/test_filtering.py` para validação
4. Consulte a documentação principal em `../README.md`

---

**🎯 Interface CLI para automação completa e execução em lote!**
