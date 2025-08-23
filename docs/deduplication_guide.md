# Guia de Deduplicação

Este guia explica como usar a funcionalidade de deduplicação do projeto.

## 🎯 O que é a Deduplicação?

A deduplicação compara novos resultados de scraping com uma base de dados existente e identifica apenas os registros que são realmente novos, evitando duplicatas.

## 🚀 Como Funciona

### 1. **Execução Automática**
Quando você executa o pipeline (`python pipeline.py`), a deduplicação acontece automaticamente após o scraping.

### 2. **Execução Manual**
Você pode executar a deduplicação independentemente usando o script dedicado:

```bash
# Deduplicação básica
python deduplicate.py

# Especificando arquivos personalizados
python deduplicate.py --new-results data/raw/meus_resultados.csv --base-db data/raw/minha_base.csv

# Criando uma nova base de dados
python deduplicate.py --create-base
```

## 📁 Estrutura de Arquivos

```
data/
├── raw/
│   ├── search_results.csv      # Resultados do scraping atual
│   └── base_database.csv       # Base de dados existente
└── processed/
    └── new_records.csv         # Apenas registros novos
```

## ⚙️ Configuração

No arquivo `configs/config.yaml`:

```yaml
deduplication:
  base_database: "data/raw/base_database.csv"
  new_records_output: "data/processed/new_records.csv"
  enable_auto_dedup: true
```

## 🔧 Funcionalidades

### **Deduplicator Class**
- **`find_new_records()`**: Encontra registros novos
- **`_remove_duplicates()`**: Remove duplicatas baseado no campo 'link'
- **`_update_base_database()`**: Atualiza a base de dados
- **`get_statistics()`**: Retorna estatísticas da base

### **Critérios de Deduplicação**
- **Campo principal**: `link` (URL do artigo)
- **Lógica**: Se o link já existe na base, o registro é considerado duplicado
- **Resultado**: Apenas registros com links únicos são considerados novos

## 📊 Exemplo de Uso

### Primeira Execução
```bash
python pipeline.py
# Resultado: Todos os registros são considerados novos
# Base de dados criada automaticamente
```

### Execuções Subsequentes
```bash
python pipeline.py
# Resultado: Apenas registros realmente novos são identificados
# Base de dados atualizada automaticamente
```

### Deduplicação Manual
```bash
# Verificar apenas os novos registros
python deduplicate.py

# Criar uma nova base a partir de resultados existentes
python deduplicate.py --create-base
```

## 🎛️ Opções de Linha de Comando

```bash
python deduplicate.py [OPÇÕES]

OPÇÕES:
  --new-results PATH    Arquivo com novos resultados
  --base-db PATH        Base de dados existente
  --output PATH         Arquivo de saída para novos registros
  --create-base         Cria nova base de dados
  -h, --help           Mostra esta mensagem de ajuda
```

## 📈 Estatísticas

A deduplicação fornece estatísticas úteis:
- Total de registros na base
- Número de fontes únicas
- Número de termos únicos
- Quantidade de registros novos encontrados

## 🔍 Debug e Troubleshooting

### Verificar Campos
Certifique-se de que o CSV tenha o campo `link` para deduplicação correta.

### Logs
A deduplicação fornece logs detalhados para facilitar o debug.

### Erros Comuns
- **Arquivo não encontrado**: Verifique os caminhos dos arquivos
- **Campo 'link' ausente**: Adicione o campo ou modifique a lógica de deduplicação
- **Permissões**: Verifique permissões de escrita nas pastas de saída

## 🚀 Próximos Passos

- Implementar critérios de deduplicação adicionais (título, autores, etc.)
- Adicionar suporte para diferentes formatos de arquivo
- Implementar backup automático da base de dados
- Adicionar interface web para visualização dos resultados
