"""
Content filtering module for the Design Publications Scraper.

This module handles:
- Filtering content by relevance and language
- Scoring content based on UX/Design terms
- Language detection and validation
- Generating curation candidates
"""

import pandas as pd
import re
from typing import List, Dict, Tuple, Optional
import langdetect
from langdetect import DetectorFactory
import unicodedata
import os


class ContentFilter:
    """Filters content based on relevance and language criteria."""
    
    def __init__(self):
        """Initialize the content filter with detection settings."""
        # Initialize language detector
        DetectorFactory.seed = 0
        
        # Relevance terms for design and UX (specified by user)
        self.relevant_terms = [
            # Specific UX/Design terms
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
        
        # Exclusion terms (irrelevant content)
        self.exclusion_terms = [
            'spam', 'teste automático', 'teste automatico', 'lorem ipsum',
            'placeholder', 'exemplo', 'sample', 'demo', 'versão beta',
            'versao beta', 'rascunho', 'borrador', 'temporário'
        ]
        
        # Portuguese language patterns
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
        Filter content based on relevance and language.
        
        Args:
            transformed_df: DataFrame with transformed data
            
        Returns:
            Tuple with (relevant content, content filtered for curation)
        """
        if transformed_df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        print("🔍 Starting content filtering...")
        
        # Apply filters
        relevant_content = []
        curation_content = []
        
        for _, row in transformed_df.iterrows():
            title = str(row.get('title', '')).lower()
            
            # Check if should be excluded
            if self._should_exclude(title):
                continue
            
            # Check relevance
            relevance_score = self._calculate_relevance(title)
            
            # Check language
            is_portuguese = self._is_portuguese(title)
            
            if relevance_score > 0 and is_portuguese:
                # Relevant content - goes to curation
                row_copy = row.copy()
                row_copy['relevance_score'] = relevance_score
                row_copy['language_verified'] = 'Português'
                curation_content.append(row_copy)
            elif relevance_score > 0:
                # Relevant content but language not verified
                row_copy = row.copy()
                row_copy['relevance_score'] = relevance_score
                row_copy['language_verified'] = 'Não verificado'
                curation_content.append(row_copy)
            else:
                # Non-relevant content
                continue
        
        # Create DataFrames
        if curation_content:
            curation_df = pd.DataFrame(curation_content)
            curation_df = curation_df.sort_values('relevance_score', ascending=False)
        else:
            curation_df = pd.DataFrame()
        
        print(f"📊 Filtering completed:")
        print(f"   Content for curation: {len(curation_df)} records")
        
        return pd.DataFrame(), curation_df
    
    def _should_exclude(self, title: str) -> bool:
        """Check if title should be excluded."""
        title_lower = title.lower()
        
        # Check exclusion terms
        for term in self.exclusion_terms:
            if term.lower() in title_lower:
                return True
        
        # Check suspicious patterns
        suspicious_patterns = [
            r'^\s*$',  # Empty title or just spaces
            r'^[0-9\s\-_]+$',  # Just numbers and special characters
            r'^[a-z]{1,2}\s*$',  # Very short titles
        ]
        
        for pattern in suspicious_patterns:
            if re.match(pattern, title_lower):
                return True
        
        return False
    
    def _calculate_relevance(self, title: str) -> int:
        """Calculate relevance score based on terms."""
        title_lower = title.lower()
        score = 0
        
        # Count occurrences of relevant terms
        for term in self.relevant_terms:
            if term.lower() in title_lower:
                score += 1
        
        # Bonus for specific combinations
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
        """Check if title is in Portuguese."""
        try:
            # Try to detect language
            detected_lang = langdetect.detect(title)
            
            if detected_lang in ['pt', 'pt-br']:
                return True
            
            # If not detected as Portuguese, check patterns
            return self._check_portuguese_patterns(title)
            
        except:
            # If detection fails, use patterns
            return self._check_portuguese_patterns(title)
    
    def _check_portuguese_patterns(self, title: str) -> bool:
        """Check specific Portuguese patterns."""
        title_lower = title.lower()
        
        # Count Portuguese patterns found
        portuguese_matches = 0
        
        for pattern in self.portuguese_patterns:
            matches = len(re.findall(pattern, title_lower))
            portuguese_matches += matches
        
        # If found at least 2 patterns, consider Portuguese
        return portuguese_matches >= 2
    
    def get_filtering_stats(self, original_df: pd.DataFrame, curation_df: pd.DataFrame) -> Dict:
        """Return filtering statistics."""
        total_original = len(original_df)
        total_curation = len(curation_df)
        
        stats = {
            'total_original': total_original,
            'total_curation': total_curation,
            'filtered_out': total_original - total_curation,
            'filtering_rate': (total_curation / total_original * 100) if total_original > 0 else 0
        }
        
        return stats
    
    def filter_and_save_for_curation(self, transformed_results_path: str, curation_output_path: str) -> Optional[pd.DataFrame]:
        """
        Main function to filter and save content for curation.
        
        Args:
            transformed_results_path: Path to CSV with transformed results
            curation_output_path: Path to save filtered results for curation
            
        Returns:
            DataFrame with filtered content for curation
        """
        print("🔍 Starting filtering for curation...")
        
        try:
            # Load transformed data
            transformed_df = pd.read_csv(transformed_results_path)
            print(f"📖 Loaded {len(transformed_df)} transformed records")
            
            if transformed_df.empty:
                print("⚠️ No data to filter")
                return pd.DataFrame()
            
            # Apply filters
            _, curation_df = self.filter_content(transformed_df)
            
            if curation_df.empty:
                print("⚠️ No relevant content found for curation")
                return pd.DataFrame()
            
            # Save results for curation
            os.makedirs(os.path.dirname(curation_output_path), exist_ok=True)
            curation_df.to_csv(curation_output_path, index=False)
            
            print(f"💾 Content for curation saved to: {curation_output_path}")
            
            # Show statistics
            stats = self.get_filtering_stats(transformed_df, curation_df)
            print(f"\n📊 Filtering statistics:")
            print(f"   Total original: {stats['total_original']}")
            print(f"   For curation: {stats['total_curation']}")
            print(f"   Filtered out: {stats['filtered_out']}")
            print(f"   Filtering rate: {stats['filtering_rate']:.1f}%")
            
            # Show some examples
            print(f"\n📝 Examples of content for curation:")
            for i, row in curation_df.head(3).iterrows():
                print(f"   {i+1}. {row['title'][:60]}...")
                print(f"      Relevance: {row['relevance_score']} | Language: {row['language_verified']}")
                print()
            
            return curation_df
            
        except Exception as e:
            print(f"❌ Error in filtering: {e}")
            return pd.DataFrame()


# Convenience function for backward compatibility
def filter_and_save_for_curation(transformed_results_path: str, curation_output_path: str) -> Optional[pd.DataFrame]:
    """Convenience function to filter and save content for curation."""
    filter_tool = ContentFilter()
    return filter_tool.filter_and_save_for_curation(transformed_results_path, curation_output_path)
