import pandas as pd
import uuid
from datetime import datetime
import re
import os


class DataTransformer:
    """Classe para transformação e limpeza de dados"""
    
    def __init__(self):
        # Keywords that must be present in Portuguese titles
        self.required_keywords = [
            'jornada do usuário', 'prototipagem', 'testes de usabilidade', 'persona', 
            'wireframe', 'arquitetura da informação', 'acessibilidade', 'interface intuitiva',
            'métricas de UX', 'análise heurística', 'design centrado no usuário', 'storytelling',
            'experiência emocional', 'interação humano-computador', 'feedback do usuário',
            'pesquisa qualitativa', 'pesquisa quantitativa', 'comportamento do consumidor',
            'design thinking', 'microinterações', 'psicologia cognitiva', 'empatia',
            'navegação', 'experiência multicanal', 'experiência mobile', 'experiência',
            'usuário', 'interface intuitiva', 'usabilidade', 'interação', 'sistema',
            'digital', 'informação', 'tecnologia', 'ux design', 'design ops', 'ux',
            'ergodesign', 'design participativo', 'product', 'neurodesign', 'user experience',
            'user', 'experience', 'comportamento', 'web'
        ]
        
        # Base database column structure
        self.base_columns = [
            'id', 'timestamp', 'title', 'author', 'year', 'type', 'link', 'database',
            'category', 'cover_image', '🔐 Softr Record ID'
        ]
    
    def is_portuguese_title(self, title):
        """
        Check if the title is in Portuguese by looking for Portuguese-specific characters
        and common Portuguese words
        """
        if not title or pd.isna(title):
            return False
        
        title_lower = str(title).lower()
        
        # Portuguese-specific characters
        portuguese_chars = ['á', 'à', 'ã', 'â', 'é', 'ê', 'í', 'ó', 'ô', 'õ', 'ú', 'ç', 'ñ']
        
        # Common Portuguese words
        portuguese_words = [
            'de', 'da', 'do', 'das', 'dos', 'para', 'com', 'sem', 'em', 'na', 'no',
            'nas', 'nos', 'por', 'pelo', 'pela', 'pelos', 'pelas', 'que', 'qual',
            'quais', 'como', 'onde', 'quando', 'quem', 'cujo', 'cuja', 'cujos', 'cujas',
            'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas',
            'aquele', 'aquela', 'aqueles', 'aquelas', 'mesmo', 'mesma', 'mesmos', 'mesmas',
            'próprio', 'própria', 'próprios', 'próprias', 'outro', 'outra', 'outros', 'outras',
            'todo', 'toda', 'todos', 'todas', 'algum', 'alguma', 'alguns', 'algumas',
            'nenhum', 'nenhuma', 'nenhuns', 'nenhumas', 'certo', 'certa', 'certos', 'certas',
            'vário', 'vária', 'vários', 'várias', 'pouco', 'pouca', 'poucos', 'poucas',
            'muito', 'muita', 'muitos', 'muitas', 'bastante', 'bastantes', 'demasiado',
            'demasiada', 'demasiados', 'demasiadas', 'mais', 'menos', 'melhor', 'pior',
            'maior', 'menor', 'ótimo', 'ótima', 'ótimas', 'ótimas', 'péssimo', 'péssima',
            'péssimos', 'péssimas', 'bom', 'boa', 'bons', 'boas', 'mau', 'má', 'maus', 'más'
        ]
        
        # Check for Portuguese characters
        has_portuguese_chars = any(char in title_lower for char in portuguese_chars)
        
        # Check for Portuguese words (at least 3)
        portuguese_word_count = sum(1 for word in portuguese_words if word in title_lower.split())
        
        return has_portuguese_chars or portuguese_word_count >= 3
    
    def contains_required_keywords(self, title):
        """
        Check if the title contains any of the required keywords
        """
        if not title or pd.isna(title):
            return False
        
        title_lower = str(title).lower()
        
        # Check if any required keyword is present
        for keyword in self.required_keywords:
            if keyword in title_lower:
                return True
        
        return False
    
    def filter_results(self, df):
        """
        Filter results based on Portuguese language and required keywords
        """
        if df.empty:
            return df
        
        print(f"🔍 Filtrando {len(df)} resultados...")
        
        # Filter by Portuguese language
        portuguese_mask = df['title'].apply(self.is_portuguese_title)
        portuguese_df = df[portuguese_mask]
        print(f"   📝 Títulos em português: {len(portuguese_df)}")
        
        # Filter by required keywords
        keyword_mask = portuguese_df['title'].apply(self.contains_required_keywords)
        filtered_df = portuguese_df[keyword_mask]
        print(f"   🎯 Contém palavras-chave: {len(filtered_df)}")
        
        return filtered_df
    
    def map_to_base_structure(self, df):
        """
        Map scraped data to the base database column structure
        """
        if df.empty:
            return df
        
        print(f"🔄 Mapeando {len(df)} registros para estrutura da base...")
        
        # Create new DataFrame with base structure
        mapped_df = pd.DataFrame(columns=self.base_columns)
        
        # Map existing columns
        column_mapping = {
            'title': 'title',
            'author': 'author',
            'link': 'link',
            'fonte': 'database',
            'termo': 'category'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                mapped_df[new_col] = df[old_col]
        
        # Fill missing columns with default values
        mapped_df['id'] = [str(uuid.uuid4()) for _ in range(len(mapped_df))]
        mapped_df['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        mapped_df['year'] = mapped_df.get('date', pd.Series(['N/A'] * len(mapped_df)))
        mapped_df['type'] = 'Artigo'  # Default type for scraped results
        mapped_df['cover_image'] = ''
        mapped_df['🔐 Softr Record ID'] = ''
        
        # Clean up year column
        if 'year' in mapped_df.columns:
            mapped_df['year'] = mapped_df['year'].fillna('N/A')
        
        # Ensure all required columns exist
        for col in self.base_columns:
            if col not in mapped_df.columns:
                mapped_df[col] = ''
        
        # Reorder columns to match base structure
        mapped_df = mapped_df[self.base_columns]
        
        print(f"✅ Mapeamento concluído: {len(mapped_df)} registros estruturados")
        
        return mapped_df
    
    def transform_and_filter(self, df):
        """
        Complete transformation pipeline: filter and map to base structure
        """
        if df.empty:
            return df
        
        print(f"🚀 Iniciando transformação de {len(df)} registros...")
        
        # Step 1: Filter results
        filtered_df = self.filter_results(df)
        
        if filtered_df.empty:
            print("⚠️ Nenhum resultado passou pelos filtros")
            return filtered_df
        
        # Step 2: Map to base structure
        mapped_df = self.map_to_base_structure(filtered_df)
        
        print(f"✨ Transformação concluída: {len(mapped_df)} registros válidos")
        
        return mapped_df
    
    def save_filtered_results(self, df, output_path):
        """
        Save filtered and transformed results to CSV
        """
        if df.empty:
            print("⚠️ Nenhum dado para salvar")
            return
        
        try:
            # Create directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to CSV
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"💾 Resultados filtrados salvos em: {output_path}")
            print(f"   📊 Total de registros: {len(df)}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")
    
    def get_filtering_stats(self, original_df, filtered_df):
        """
        Get statistics about the filtering process
        """
        stats = {
            'total_original': len(original_df),
            'portuguese_titles': len(original_df[original_df['title'].apply(self.is_portuguese_title)]),
            'with_keywords': len(filtered_df),
            'filtered_out': len(original_df) - len(filtered_df)
        }
        
        return stats


def transform_search_results(input_path, output_path):
    """
    Transform and filter search results from scrapers
    
    Args:
        input_path: Path to raw search results CSV
        output_path: Path to save filtered results
    """
    print("🔄 Iniciando transformação dos resultados de busca...")
    
    try:
        # Load data
        df = pd.read_csv(input_path)
        print(f"📥 Dados carregados: {len(df)} registros")
        
        # Transform and filter
        transformer = DataTransformer()
        transformed_df = transformer.transform_and_filter(df)
        
        if not transformed_df.empty:
            # Save filtered results
            transformer.save_filtered_results(transformed_df, output_path)
            
            # Show statistics
            stats = transformer.get_filtering_stats(df, transformed_df)
            print(f"\n📊 Estatísticas do filtro:")
            print(f"   Total original: {stats['total_original']}")
            print(f"   Títulos em português: {stats['portuguese_titles']}")
            print(f"   Com palavras-chave: {stats['with_keywords']}")
            print(f"   Filtrados: {stats['filtered_out']}")
        else:
            print("⚠️ Nenhum resultado válido encontrado após filtros")
        
        return transformed_df
        
    except Exception as e:
        print(f"❌ Erro na transformação: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    # Example usage
    transform_search_results(
        "data/raw/search_results.csv",
        "data/processed/filtered_results.csv"
    )
