import pandas as pd
import re
from typing import List, Dict, Tuple
import langdetect
from langdetect import DetectorFactory
import unicodedata


class ContentFilter:
    """Filtra conteúdo baseado em critérios de relevância e idioma"""
    
    def __init__(self):
        # Inicializa detector de idioma
        DetectorFactory.seed = 0
        
        # Termos de relevância para design e UX (especificados pelo usuário)
        self.relevant_terms = [
            # Termos específicos de UX/Design
            'jornada do usuário', 'prototipagem', 'testes de usabilidade', 'persona',
            'wireframe', 'arquitetura da informação', 'acessibilidade', 'interface intuitiva',
            'métricas de ux', 'análise heurística', 'design centrado no usuário',
            'storytelling', 'experiência emocional', 'interação humano-computador',
            'feedback do usuário', 'pesquisa qualitativa', 'pesquisa quantitativa',
            'comportamento do consumidor', 'design thinking', 'microinterações',
            'psicologia cognitiva', 'empatia', 'navegação', 'experiência multicanal',
            'experiência mobile', 'experiência', 'usuário', 'interface intuitiva',
            'usabilidade', 'interação', 'sistema', 'digital', 'informação',
            'tecnologia', 'ux design', 'design ops', 'ux', 'ergodesign',
            'design participativo', 'product', 'neurodesign', 'user experience',
            'user', 'experience', 'comportamento', 'web'
        ]
        
        # Termos de exclusão (conteúdo irrelevante)
        self.exclusion_terms = [
            'spam', 'teste automático', 'teste automatico', 'lorem ipsum',
            'placeholder', 'exemplo', 'sample', 'demo', 'versão beta',
            'versao beta', 'rascunho', 'borrador', 'temporário'
        ]
        
        # Padrões de idioma português
        self.portuguese_patterns = [
            r'\b(do|da|de|em|para|por|com|sem|sob|sobre|entre|contra|desde|até|até)\b',
            r'\b(é|está|estão|ser|estar|ter|haver|fazer|dizer|ver|ir|vir|dar|saber|poder|querer)\b',
            r'\b(um|uma|uns|umas|o|a|os|as|este|esta|estes|estas|esse|essa|esses|essas)\b',
            r'\b(que|qual|quais|quem|onde|quando|como|porque|por que|porquê|porquê)\b',
            r'\b(não|não|sim|também|tambem|ainda|já|já|sempre|nunca|agora|hoje|amanhã)\b',
            r'\b(design|usabilidade|interface|experiência|experiencia|usuario|usuário)\b',
            r'\b(tecnologia|digital|informação|informacao|visual|gráfico|grafico)\b'
        ]
    
    def filter_content(self, transformed_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Filtra conteúdo baseado em relevância e idioma
        
        Args:
            transformed_df: DataFrame com dados transformados
            
        Returns:
            Tuple com (conteúdo relevante, conteúdo filtrado para curadoria)
        """
        if transformed_df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        print("🔍 Iniciando filtragem de conteúdo...")
        
        # Aplica filtros
        relevant_content = []
        curation_content = []
        
        for _, row in transformed_df.iterrows():
            title = str(row.get('title', '')).lower()
            
            # Verifica se deve ser descartado
            if self._should_exclude(title):
                continue
            
            # Verifica relevância
            relevance_score = self._calculate_relevance(title)
            
            # Verifica idioma
            is_portuguese = self._is_portuguese(title)
            
            if relevance_score > 0 and is_portuguese:
                # Conteúdo relevante - vai para curadoria
                row_copy = row.copy()
                row_copy['relevance_score'] = relevance_score
                row_copy['language_verified'] = 'Português'
                curation_content.append(row_copy)
            elif relevance_score > 0:
                # Conteúdo relevante mas idioma não verificado
                row_copy = row.copy()
                row_copy['relevance_score'] = relevance_score
                row_copy['language_verified'] = 'Não verificado'
                curation_content.append(row_copy)
            else:
                # Conteúdo não relevante
                continue
        
        # Cria DataFrames
        if curation_content:
            curation_df = pd.DataFrame(curation_content)
            curation_df = curation_df.sort_values('relevance_score', ascending=False)
        else:
            curation_df = pd.DataFrame()
        
        print(f"📊 Filtragem concluída:")
        print(f"   Conteúdo para curadoria: {len(curation_df)} registros")
        
        return pd.DataFrame(), curation_df
    
    def _should_exclude(self, title: str) -> bool:
        """Verifica se o título deve ser excluído"""
        title_lower = title.lower()
        
        # Verifica termos de exclusão
        for term in self.exclusion_terms:
            if term.lower() in title_lower:
                return True
        
        # Verifica padrões suspeitos
        suspicious_patterns = [
            r'^\s*$',  # Título vazio ou só espaços
            r'^[0-9\s\-_]+$',  # Só números e caracteres especiais
            r'^[a-z]{1,2}\s*$',  # Títulos muito curtos
        ]
        
        for pattern in suspicious_patterns:
            if re.match(pattern, title_lower):
                return True
        
        return False
    
    def _calculate_relevance(self, title: str) -> int:
        """Calcula pontuação de relevância baseada nos termos"""
        title_lower = title.lower()
        score = 0
        
        # Conta ocorrências de termos relevantes
        for term in self.relevant_terms:
            if term.lower() in title_lower:
                score += 1
        
        # Bônus para combinações específicas
        if 'ux design' in title_lower:
            score += 3
        if 'design thinking' in title_lower:
            score += 3
        if 'user experience' in title_lower:
            score += 3
        if 'jornada do usuário' in title_lower:
            score += 3
        if 'testes de usabilidade' in title_lower:
            score += 3
        if 'arquitetura da informação' in title_lower:
            score += 3
        if 'análise heurística' in title_lower:
            score += 3
        if 'design centrado no usuário' in title_lower:
            score += 3
        if 'interação humano-computador' in title_lower:
            score += 3
        if 'pesquisa qualitativa' in title_lower or 'pesquisa quantitativa' in title_lower:
            score += 2
        if 'microinterações' in title_lower:
            score += 2
        if 'neurodesign' in title_lower:
            score += 2
        
        return score
    
    def _is_portuguese(self, title: str) -> bool:
        """Verifica se o título está em português"""
        try:
            # Tenta detectar idioma
            detected_lang = langdetect.detect(title)
            
            if detected_lang in ['pt', 'pt-br']:
                return True
            
            # Se não detectou como português, verifica padrões
            return self._check_portuguese_patterns(title)
            
        except:
            # Se falhar na detecção, usa padrões
            return self._check_portuguese_patterns(title)
    
    def _check_portuguese_patterns(self, title: str) -> bool:
        """Verifica padrões específicos do português"""
        title_lower = title.lower()
        
        # Conta padrões portugueses encontrados
        portuguese_matches = 0
        
        for pattern in self.portuguese_patterns:
            matches = len(re.findall(pattern, title_lower))
            portuguese_matches += matches
        
        # Se encontrou pelo menos 2 padrões, considera português
        return portuguese_matches >= 2
    
    def get_filtering_stats(self, original_df: pd.DataFrame, curation_df: pd.DataFrame) -> Dict:
        """Retorna estatísticas da filtragem"""
        total_original = len(original_df)
        total_curation = len(curation_df)
        
        stats = {
            'total_original': total_original,
            'total_curation': total_curation,
            'filtered_out': total_original - total_curation,
            'filtering_rate': (total_curation / total_original * 100) if total_original > 0 else 0
        }
        
        return stats


def filter_and_save_for_curation(transformed_results_path: str, 
                                curation_output_path: str) -> pd.DataFrame:
    """
    Função principal para filtrar e salvar conteúdo para curadoria
    
    Args:
        transformed_results_path: Caminho para CSV com resultados transformados
        curation_output_path: Caminho para salvar resultados filtrados para curadoria
        
    Returns:
        DataFrame com conteúdo filtrado para curadoria
    """
    print("🔍 Iniciando filtragem para curadoria...")
    
    try:
        # Carrega dados transformados
        transformed_df = pd.read_csv(transformed_results_path)
        print(f"📖 Carregados {len(transformed_df)} registros transformados")
        
        if transformed_df.empty:
            print("⚠️ Nenhum dado para filtrar")
            return pd.DataFrame()
        
        # Aplica filtros
        filter_tool = ContentFilter()
        _, curation_df = filter_tool.filter_content(transformed_df)
        
        if curation_df.empty:
            print("⚠️ Nenhum conteúdo relevante encontrado para curadoria")
            return pd.DataFrame()
        
        # Salva resultados para curadoria
        import os
        os.makedirs(os.path.dirname(curation_output_path), exist_ok=True)
        curation_df.to_csv(curation_output_path, index=False)
        
        print(f"💾 Conteúdo para curadoria salvo em: {curation_output_path}")
        
        # Mostra estatísticas
        stats = filter_tool.get_filtering_stats(transformed_df, curation_df)
        print(f"\n📊 Estatísticas da filtragem:")
        print(f"   Total original: {stats['total_original']}")
        print(f"   Para curadoria: {stats['total_curation']}")
        print(f"   Filtrados: {stats['filtered_out']}")
        print(f"   Taxa de filtragem: {stats['filtering_rate']:.1f}%")
        
        # Mostra alguns exemplos
        print(f"\n📝 Exemplos de conteúdo para curadoria:")
        for i, row in curation_df.head(3).iterrows():
            print(f"   {i+1}. {row['title'][:60]}...")
            print(f"      Relevância: {row['relevance_score']} | Idioma: {row['language_verified']}")
            print()
        
        return curation_df
        
    except Exception as e:
        print(f"❌ Erro na filtragem: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    # Exemplo de uso
    filter_and_save_for_curation(
        "data/processed/transformed_results.csv",
        "data/processed/curation_candidates.csv"
    )
