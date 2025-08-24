"""
Data transformation module for the Design Publications Scraper.

This module handles:
- Converting search results to base database format
- Extracting years from dates
- Mapping categories and databases
- Generating unique IDs
"""

import pandas as pd
import uuid
from datetime import datetime
import re
import os
from typing import Optional


class DataTransformer:
    """Transforms search results data to match the base database structure."""
    
    def __init__(self):
        """Initialize the transformer with base columns."""
        self.base_columns = [
            'id', 'timestamp', 'title', 'author', 'year', 'type', 
            'link', 'database', 'category', 'cover_image', '🔐 Softr Record ID'
        ]
    
    def transform_search_results(self, search_results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform search results to base database format.
        
        Args:
            search_results_df: DataFrame with search results
            
        Returns:
            DataFrame transformed to base database structure
        """
        if search_results_df.empty:
            return pd.DataFrame(columns=self.base_columns)
        
        # Create transformed DataFrame
        transformed_data = []
        
        for _, row in search_results_df.iterrows():
            transformed_row = self._transform_single_record(row)
            if transformed_row:
                transformed_data.append(transformed_row)
        
        # Create final DataFrame
        transformed_df = pd.DataFrame(transformed_data, columns=self.base_columns)
        
        # Set explicit data types to avoid automatic conversion
        transformed_df = transformed_df.astype({
            'id': 'string',
            'timestamp': 'string',
            'title': 'string',
            'author': 'string',
            'year': 'string',
            'type': 'string',
            'link': 'string',
            'database': 'string',
            'category': 'string',
            'cover_image': 'string',
            '🔐 Softr Record ID': 'string'
        })
        
        print(f"🔄 Transformed {len(transformed_df)} records to base database format")
        return transformed_df
    
    def _transform_single_record(self, row: pd.Series) -> Optional[dict]:
        """Transform a single record."""
        try:
            # Extract year from date or edition
            year = self._extract_year(row)
            
            # Determine type based on content
            pub_type = self._determine_publication_type(row)
            
            # Determine category based on search term
            category = self._determine_category(row.get('termo', ''))
            
            # Determine database based on source
            database = self._determine_database(row.get('fonte', ''))
            
            transformed_record = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'title': self._clean_text(row.get('title', '')),
                'author': self._clean_text(row.get('author', '')),
                'year': year if year else 'Sem ano',
                'type': pub_type,
                'link': row.get('link', ''),
                'database': database,
                'category': category,
                'cover_image': 'Sem imagem',  # Not available in search results
                '🔐 Softr Record ID': 'Sem ID'  # Will be filled later if needed
            }
            
            return transformed_record
            
        except Exception as e:
            print(f"⚠️ Error transforming record: {e}")
            return None
    
    def _extract_year(self, row: pd.Series) -> str:
        """Extract year from a data row, checking both date and edition fields."""
        # Check date field first
        date_str = row.get('date', '')
        if not pd.isna(date_str) and date_str != '' and date_str != 'Data não informada':
            year = self._extract_year_from_string(str(date_str))
            if year:
                return year
        
        # If not found in date, check edition field
        edition_str = row.get('edition', '')
        if not pd.isna(edition_str) and edition_str != '':
            year = self._extract_year_from_string(str(edition_str))
            if year:
                return year
        
        return ''
    
    def _extract_year_from_string(self, date_str: str) -> str:
        """Extract year from a specific string."""
        if not date_str or date_str == '':
            return ''
        
        # Look for year patterns (4 digits)
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return year_match.group()
        
        # Look for edition patterns (ex: v. 31, n. 3 (2023))
        edition_match = re.search(r'\((\d{4})\)', date_str)
        if edition_match:
            return edition_match.group(1)
        
        # Look for date patterns (ex: 16-05-2018, 2022-04-04)
        date_patterns = [
            r'(\d{4})-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}-\d{2}-(\d{4})',  # DD-MM-YYYY
            r'(\d{4})-\d{2}',         # YYYY-MM
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, date_str)
            if match:
                return match.group(1)
        
        return ''
    
    def _determine_publication_type(self, row: pd.Series) -> str:
        """Determine publication type based on content."""
        title = str(row.get('title', '')).lower()
        fonte = str(row.get('fonte', '')).lower()
        
        # Check if it's an article based on source or title
        if any(journal in fonte for journal in ['revista', 'journal', 'estudos', 'infodesign', 'human factors', 'arcos', 'triades', 'educacao grafica']):
            return 'Artigo'
        
        # Check if it's a book based on title
        if any(word in title for word in ['livro', 'book', 'manual', 'guia']):
            return 'Livro'
        
        # Pattern: if it has PDF or abstract link, probably an article
        if row.get('pdf_link') or row.get('resumo_link'):
            return 'Artigo'
        
        # Pattern: if it has edition_link, probably an article
        if row.get('edition_link'):
            return 'Artigo'
        
        return 'Artigo'  # Default for search results
    
    def _determine_category(self, search_term: str) -> str:
        """Determine category based on search term."""
        term = str(search_term).lower()
        
        category_mapping = {
            'experiencia': 'Fundamentos',
            'usuario': 'Fundamentos',
            'interface': 'Visual',
            'usabilidade': 'Fundamentos',
            'interacao': 'Fundamentos',
            'sistema': 'Tecnologia',
            'ergonomia': 'Fundamentos',
            'digital': 'Tecnologia',
            'informacao': 'Informação',
            'tecnologia': 'Tecnologia',
            'inteligencia artificial': 'Tecnologia',
            'design thinking': 'Processos',
            'ux': 'Fundamentos'
        }
        
        for key, category in category_mapping.items():
            if key in term:
                return category
        
        return 'Fundamentos'  # Default category
    
    def _determine_database(self, fonte: str) -> str:
        """Determine database name based on source."""
        # Check if source is valid
        if pd.isna(fonte) or fonte == '':
            return 'Fonte não informada'
        
        fonte_lower = str(fonte).lower()
        
        database_mapping = {
            'estudos em design': 'Revista Estudos em Design',
            'infodesign': 'InfoDesign',
            'human factors in design': 'Human Factors in Design',
            'arcos design': 'Arcos Design',
            'design e tecnologia': 'Design e Tecnologia',
            'triades': 'Tríades em Revista',
            'educacao grafica': 'Educação Gráfica'
        }
        
        for key, database in database_mapping.items():
            if key in fonte_lower:
                return database
        
        return fonte  # Return original source if no mapping found
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if pd.isna(text) or text == '':
            return ''
        
        # Remove extra quotes and normalize
        cleaned = str(text).strip()
        cleaned = cleaned.replace('"', '').replace('"', '').replace('"', '')
        
        return cleaned
    
    def validate_transformation(self, transformed_df: pd.DataFrame) -> tuple[bool, str]:
        """Validate if transformation was successful."""
        if transformed_df.empty:
            return False, "Empty DataFrame"
        
        # Check if all necessary columns are present
        missing_columns = set(self.base_columns) - set(transformed_df.columns)
        if missing_columns:
            return False, f"Missing columns: {missing_columns}"
        
        # Check if there is valid data
        if transformed_df['title'].isna().all() or transformed_df['link'].isna().all():
            return False, "Essential data (title or link) is empty"
        
        return True, "Valid transformation"
    
    def get_transformation_stats(self, original_df: pd.DataFrame, transformed_df: pd.DataFrame) -> dict:
        """Return transformation statistics."""
        stats = {
            'original_records': len(original_df),
            'transformed_records': len(transformed_df),
            'success_rate': len(transformed_df) / len(original_df) * 100 if len(original_df) > 0 else 0,
            'missing_data': len(original_df) - len(transformed_df)
        }
        
        return stats
    
    def transform_and_save_results(self, search_results_path: str, output_path: str, base_db_path: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Main function to transform and save results.
        
        Args:
            search_results_path: Path to CSV with search results
            output_path: Path to save transformed results
            base_db_path: Optional path to existing database
            
        Returns:
            DataFrame with transformed results or None if failed
        """
        print("🔄 Starting data transformation...")
        
        try:
            # Load search results
            search_df = pd.read_csv(search_results_path)
            print(f"📖 Loaded {len(search_df)} search results")
            
            # Transform data
            transformed_df = self.transform_search_results(search_df)
            
            if transformed_df.empty:
                print("⚠️ No data was transformed")
                return None
            
            # Validate transformation
            is_valid, message = self.validate_transformation(transformed_df)
            if not is_valid:
                print(f"❌ Validation failed: {message}")
                return None
            
            # Save transformed results
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save with preserved data types
            transformed_df.to_csv(output_path, index=False)
            
            # Verify data was saved correctly
            verification_df = pd.read_csv(output_path)
            print(f"💾 Transformed results saved to: {output_path}")
            print(f"   Verification: {len(verification_df)} records saved")
            
            # Show statistics
            stats = self.get_transformation_stats(search_df, transformed_df)
            print(f"\n📊 Transformation statistics:")
            print(f"   Original records: {stats['original_records']}")
            print(f"   Transformed records: {stats['transformed_records']}")
            print(f"   Success rate: {stats['success_rate']:.1f}%")
            print(f"   Missing data: {stats['missing_data']}")
            
            return transformed_df
            
        except Exception as e:
            print(f"❌ Error in transformation: {e}")
            return None


# Convenience function for backward compatibility
def transform_and_save_results(search_results_path: str, output_path: str, base_db_path: Optional[str] = None) -> Optional[pd.DataFrame]:
    """Convenience function to transform and save results."""
    transformer = DataTransformer()
    return transformer.transform_and_save_results(search_results_path, output_path, base_db_path)
