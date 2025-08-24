# Guia de Filtragem para Curadoria

## Visão Geral

Este documento explica o sistema de filtragem implementado para triar conteúdo antes da catalogação final. O sistema aplica critérios rigorosos de relevância e idioma para garantir que apenas conteúdo de qualidade seja enviado para análise de curadoria.

## 🎯 Objetivo da Filtragem

**NÃO** enviar conteúdo diretamente para a base de dados principal. Em vez disso:

1. **Filtrar por relevância** - Verificar se o título contém termos relacionados a design/UX
2. **Validar idioma** - Garantir que seja português/português brasileiro
3. **Gerar CSV de curadoria** - Arquivo com candidatos para análise manual
4. **Evitar spam/ruído** - Excluir conteúdo irrelevante ou de baixa qualidade

## 🔍 Critérios de Filtragem

### 1. Verificação de Relevância

#### Termos de Relevância (Design e UX)
**Termos específicos especificados pelo usuário**:
- **UX/Design Core**: `ux design`, `design thinking`, `user experience`, `design centrado no usuário`
- **Metodologias**: `jornada do usuário`, `prototipagem`, `testes de usabilidade`, `análise heurística`
- **Artefatos**: `persona`, `wireframe`, `arquitetura da informação`, `microinterações`
- **Pesquisa**: `pesquisa qualitativa`, `pesquisa quantitativa`, `feedback do usuário`
- **Psicologia**: `psicologia cognitiva`, `empatia`, `neurodesign`, `comportamento do consumidor`
- **Tecnologia**: `interface intuitiva`, `sistema`, `digital`, `web`, `mobile`
- **Conceitos**: `acessibilidade`, `experiência emocional`, `storytelling`, `navegação`

#### Pontuação de Relevância
- **+1 ponto** por cada termo relevante encontrado
- **+3 pontos** por termos de alta relevância:
  - `ux design`, `design thinking`, `user experience`
  - `jornada do usuário`, `testes de usabilidade`
  - `arquitetura da informação`, `análise heurística`
  - `design centrado no usuário`, `interação humano-computador`
- **+2 pontos** por termos especializados:
  - `pesquisa qualitativa/quantitativa`, `microinterações`, `neurodesign`

**Mínimo para aprovação**: 1 ponto ou mais

### 2. Validação de Idioma

#### Detecção Automática
- Usa biblioteca `langdetect` para identificar idioma
- Aceita: `pt` (português) e `pt-br` (português brasileiro)

#### Verificação por Padrões (Fallback)
Se a detecção automática falhar, verifica padrões específicos do português:

- **Preposições**: `do`, `da`, `de`, `em`, `para`, `por`, `com`
- **Verbos**: `é`, `está`, `ser`, `estar`, `ter`, `fazer`
- **Artigos**: `um`, `uma`, `o`, `a`, `os`, `as`
- **Pronomes**: `que`, `qual`, `quem`, `onde`, `quando`
- **Advérbios**: `não`, `sim`, `também`, `ainda`, `já`

**Mínimo para aprovação**: 2 padrões portugueses ou mais

### 3. Exclusão Automática

#### Termos de Exclusão
- `spam`, `teste automático`, `lorem ipsum`
- `placeholder`, `exemplo`, `sample`, `demo`
- `versão beta`, `rascunho`, `temporário`

#### Padrões Suspeitos
- Títulos vazios ou só espaços
- Só números e caracteres especiais
- Títulos muito curtos (1-2 caracteres)

## 📊 Fluxo de Filtragem

```
1. Dados Transformados
   ↓
2. Verificação de Exclusão
   ↓
3. Cálculo de Relevância
   ↓
4. Validação de Idioma
   ↓
5. Geração de CSV para Curadoria
```

## 🎯 Resultado da Filtragem

### Arquivo de Curadoria (`curation_candidates.csv`)

**Colunas adicionais**:
- `relevance_score` - Pontuação de relevância (1-10+)
- `language_verified` - Status do idioma (`Português` ou `Não verificado`)

**Ordenação**: Por pontuação de relevância (maior para menor)

**Conteúdo**: Apenas registros que passaram nos filtros

## 📁 Arquivos Gerados

### Pipeline Completo
1. **`search_results.csv`** - Resultados brutos dos scrapers
2. **`search_results_transformed.csv`** - Dados transformados para formato base
3. **`search_results_curation.csv`** - Candidatos filtrados para curadoria
4. **`new_records.csv`** - Novos registros após deduplicação (se aplicável)

### Estrutura de Diretórios
```
data/
├── raw/
│   ├── search_results.csv          # Resultados brutos
│   └── base_database.csv           # Base principal
└── processed/
    ├── search_results_transformed.csv  # Dados transformados
    ├── search_results_curation.csv     # Para curadoria
    └── new_records.csv                 # Novos registros únicos
```

## ⚙️ Configuração

### `configs/config.yaml`
```yaml
curation:
  curation_candidates: "data/processed/curation_candidates.csv"
  enable_auto_filtering: true
```

## 🔧 Personalização

### Adicionar Novos Termos de Relevância
```python
# Em utils/content_filter.py
self.relevant_terms.extend([
    'novo_termo_1',
    'novo_termo_2'
])
```

### Modificar Critérios de Exclusão
```python
# Em utils/content_filter.py
self.exclusion_terms.extend([
    'novo_termo_exclusao'
])
```

### Ajustar Padrões de Idioma
```python
# Em utils/content_filter.py
self.portuguese_patterns.append(r'\b(novo_padrao)\b')
```

## 📈 Monitoramento e Estatísticas

### Métricas Geradas
- **Total original**: Registros antes da filtragem
- **Para curadoria**: Registros que passaram nos filtros
- **Filtrados**: Registros descartados
- **Taxa de filtragem**: Percentual de aprovação

### Exemplo de Output
```
📊 Estatísticas da filtragem:
   Total original: 282
   Para curadoria: 156
   Filtrados: 126
   Taxa de filtragem: 55.3%
```

## 🚀 Uso no Pipeline

### Integração Automática
A filtragem é executada automaticamente após a transformação:

```python
# Em pipeline.py
curation_df = filter_and_save_for_curation(
    transformed_filename,
    curation_filename
)
```

### Execução Manual
```bash
python -c "
from utils.content_filter import filter_and_save_for_curation
filter_and_save_for_curation(
    'data/processed/transformed_results.csv',
    'data/processed/curation_candidates.csv'
)
"
```

## 🎯 Benefícios da Filtragem

### 1. Qualidade do Conteúdo
- **Elimina spam** e conteúdo irrelevante
- **Garante relevância** para design/UX
- **Valida idioma** português

### 2. Eficiência da Curadoria
- **Reduz volume** para análise manual
- **Prioriza conteúdo** por relevância
- **Facilita decisões** de curadores

### 3. Manutenção da Base
- **Evita poluição** da base principal
- **Mantém padrões** de qualidade
- **Facilita auditoria** de conteúdo

## 🔍 Exemplos de Filtragem

### ✅ Aprovados (Alta Relevância)
- "UX Design e Jornada do Usuário como Abordagem para o Design" (Score: 7+)
- "Design Thinking e Testes de Usabilidade em Aplicativos Mobile" (Score: 6+)
- "Arquitetura da Informação e Análise Heurística para Interfaces" (Score: 6+)
- "Design Centrado no Usuário: Pesquisa Qualitativa e Quantitativa" (Score: 5+)

### ❌ Rejeitados
- "Teste Automático de Sistema" (Termo de exclusão)
- "Sample Data for Analysis" (Idioma não português)
- "12345" (Padrão suspeito)

## 🚨 Tratamento de Erros

### Falhas na Detecção de Idioma
- **Fallback automático** para padrões portugueses
- **Log de avisos** para casos não resolvidos
- **Inclusão** com flag "Não verificado"

### Problemas de Processamento
- **Continua execução** para outros registros
- **Log detalhado** de erros
- **Estatísticas** de falhas

## 🔮 Próximos Passos

### 1. Validação da Filtragem
- [ ] Testar com dados reais
- [ ] Ajustar critérios conforme feedback
- [ ] Validar taxa de aprovação

### 2. Melhorias Futuras
- [ ] Machine Learning para relevância
- [ ] Detecção de idioma mais robusta
- [ ] Interface de configuração visual

### 3. Integração com Curadoria
- [ ] Sistema de aprovação/rejeição
- [ ] Feedback dos curadores
- [ ] Aprendizado contínuo

---

**Nota**: Este sistema garante que apenas conteúdo de qualidade e relevância seja enviado para curadoria, mantendo a integridade da base de dados e facilitando o trabalho dos curadores.
