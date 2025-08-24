# Guia de Estrutura de Dados e Transformação

## Visão Geral

Este documento explica a diferença entre a estrutura dos dados de busca e a estrutura da base de dados principal, e como o sistema de transformação resolve essa incompatibilidade para permitir catalogação e deduplicação adequadas.

## Estruturas de Dados

### 1. Base de Dados Principal (`base_database.csv`)

A base de dados principal possui uma estrutura padronizada com as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `id` | Identificador único UUID | `b195aeb0-637a-4b47-9ff0-a690516d75dc` |
| `timestamp` | Data/hora de adição | `16/05/2025 21:11:04` |
| `title` | Título da publicação | `UX Design em Grandes Empresas` |
| `author` | Autor(es) | `Bruno Duarte` |
| `year` | Ano de publicação | `2024` |
| `type` | Tipo de publicação | `Livro`, `Artigo` |
| `link` | URL da publicação | `https://www.editorabrauer.com.br/...` |
| `database` | Fonte/database | `Editora Brauer` |
| `category` | Categorias/tags | `Processos`, `Fundamentos` |
| `cover_image` | URL da imagem | `https://framerusercontent.com/...` |
| `🔐 Softr Record ID` | ID do sistema externo | `4isigGh4nRxAm3ANV433Wa` |

### 2. Resultados de Busca (`search_results.csv`)

Os resultados de busca dos scrapers possuem uma estrutura diferente:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| `title` | Título do artigo | `Avaliação da Percepção do Idoso...` |
| `author` | Autor(es) | `Valter Oliveira Nascimento...` |
| `link` | URL do artigo | `https://www.ufrgs.br/det/...` |
| `date` | Data de publicação | `Data não informada` |
| `edition` | Informações da edição | `v. 31, n. 3 (2023)` |
| `edition_link` | Link da edição | `https://estudosemdesign.emnuvens.com.br/...` |
| `resumo_link` | Link do resumo | `https://estudosemdesign.emnuvens.com.br/...` |
| `pdf_link` | Link do PDF | `Sem PDF` |
| `fonte` | Fonte do resultado | `Estudos em Design` |
| `termo` | Termo de busca usado | `inteligência artificial` |

## Problema de Compatibilidade

**As estruturas são completamente diferentes**, o que impede:

1. **Catalogação direta**: Os campos não correspondem
2. **Deduplicação eficiente**: Comparação baseada em campos diferentes
3. **Integração com sistemas externos**: Formato incompatível
4. **Análise unificada**: Dados em formatos diferentes

## Solução: Sistema de Transformação

### Arquivo: `utils/data_transformer.py`

O sistema de transformação converte automaticamente os resultados de busca para o formato da base de dados principal.

#### Processo de Transformação

1. **Extração de Ano**: Converte `date` para `year`
2. **Determinação de Tipo**: Identifica se é `Artigo` ou `Livro`
3. **Mapeamento de Categoria**: Converte `termo` para categoria apropriada
4. **Mapeamento de Database**: Converte `fonte` para nome padronizado
5. **Geração de ID**: Cria UUID único para cada registro
6. **Timestamp**: Adiciona data/hora de processamento

#### Mapeamentos de Categoria

| Termo de Busca | Categoria |
|----------------|-----------|
| `experiencia`, `usuario`, `usabilidade` | `Fundamentos` |
| `interface` | `Visual` |
| `sistema`, `digital`, `tecnologia` | `Tecnologia` |
| `informacao` | `Informação` |
| `design thinking` | `Processos` |

#### Mapeamentos de Database

| Fonte Original | Database Padronizado |
|----------------|---------------------|
| `estudos em design` | `Revista Estudos em Design` |
| `infodesign` | `InfoDesign` |
| `human factors in design` | `Human Factors in Design` |
| `arcos design` | `Arcos Design` |
| `design e tecnologia` | `Design e Tecnologia` |
| `triades` | `Tríades em Revista` |
| `educacao grafica` | `Educação Gráfica` |

## Fluxo de Processamento Atualizado

### Pipeline Principal (`pipeline.py`)

```
1. Execução dos Scrapers
   ↓
2. Salvamento dos Resultados Brutos
   ↓
3. Transformação de Dados (NOVO)
   ↓
4. Deduplicação com Base Transformada
   ↓
5. Geração de Relatórios
```

### Arquivos Gerados

- `data/raw/search_results.csv` - Resultados brutos dos scrapers
- `data/processed/transformed_results.csv` - Dados transformados
- `data/processed/new_records.csv` - Novos registros após deduplicação

## Configuração

### `configs/config.yaml`

```yaml
data_processing:
  transformed_results: "data/processed/transformed_results.csv"
  enable_auto_transform: true

deduplication:
  base_database: "data/raw/base_database.csv"
  new_records_output: "data/processed/new_records.csv"
  enable_auto_dedup: true
```

## Validação e Testes

### Script de Teste: `test_transformation.py`

Executa a transformação em dados existentes e valida:

- ✅ Estrutura das colunas
- ✅ Presença de dados essenciais
- ✅ Qualidade da transformação
- ✅ Estatísticas de processamento

### Como Executar

```bash
python test_transformation.py
```

## Benefícios da Solução

1. **Compatibilidade Total**: Dados em formato unificado
2. **Deduplicação Eficiente**: Comparação baseada em campos idênticos
3. **Catalogação Automática**: Estrutura padronizada
4. **Integração Externa**: Formato compatível com sistemas externos
5. **Manutenibilidade**: Transformação centralizada e configurável
6. **Qualidade de Dados**: Validação e limpeza automática

## Monitoramento e Logs

O sistema gera logs detalhados durante:

- **Transformação**: Estatísticas de conversão
- **Validação**: Verificação de integridade
- **Deduplicação**: Contagem de registros únicos
- **Erros**: Tratamento de falhas com mensagens claras

## Próximos Passos

1. **Executar teste de transformação**
2. **Verificar qualidade dos dados transformados**
3. **Ajustar mapeamentos se necessário**
4. **Integrar com pipeline de produção**
5. **Monitorar performance e qualidade**

---

**Nota**: Esta solução resolve completamente o problema de incompatibilidade estrutural, permitindo que o sistema de deduplicação funcione corretamente com dados padronizados.
