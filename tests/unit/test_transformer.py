"""
Unit tests for the DataTransformer module.
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import tempfile
import os

from src.design_scraper.core.transformer import DataTransformer


class TestDataTransformer:
    """Test cases for DataTransformer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.transformer = DataTransformer()
        
        # Sample test data
        self.sample_data = pd.DataFrame({
            'title': ['Design de Interface para Usuários Idosos', 'UX Design e Usabilidade'],
            'author': ['João Silva', 'Maria Santos'],
            'date': ['2023-01-15', '2022-12-01'],
            'link': ['http://example1.com', 'http://example2.com'],
            'fonte': ['estudos_em_design', 'infodesign'],
            'termo': ['usuario', 'ux']
        })
    
    def test_init(self):
        """Test transformer initialization."""
        assert len(self.transformer.base_columns) == 11
        assert 'id' in self.transformer.base_columns
        assert 'title' in self.transformer.base_columns
        assert '🔐 Softr Record ID' in self.transformer.base_columns
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        # Test normal text
        assert self.transformer._clean_text("Normal text") == "Normal text"
        
        # Test text with quotes
        assert self.transformer._clean_text('"Text with quotes"') == "Text with quotes"
        
        # Test empty text
        assert self.transformer._clean_text("") == ""
        
        # Test NaN text
        assert self.transformer._clean_text(pd.NA) == ""
    
    def test_extract_year_from_string(self):
        """Test year extraction from strings."""
        # Test year pattern
        assert self.transformer._extract_year_from_string("2023") == "2023"
        
        # Test date pattern YYYY-MM-DD
        assert self.transformer._extract_year_from_string("2023-01-15") == "2023"
        
        # Test date pattern DD-MM-YYYY
        assert self.transformer._extract_year_from_string("15-01-2023") == "2023"
        
        # Test edition pattern
        assert self.transformer._extract_year_from_string("v. 31, n. 3 (2023)") == "2023"
        
        # Test invalid patterns
        assert self.transformer._extract_year_from_string("") == ""
        assert self.transformer._extract_year_from_string("invalid") == ""
    
    def test_determine_publication_type(self):
        """Test publication type determination."""
        # Test article detection
        row = pd.Series({'title': 'Design Article', 'fonte': 'estudos_em_design'})
        assert self.transformer._determine_publication_type(row) == 'Artigo'
        
        # Test book detection
        row = pd.Series({'title': 'Design Manual Book', 'fonte': 'other'})
        assert self.transformer._determine_publication_type(row) == 'Livro'
    
    def test_determine_category(self):
        """Test category determination."""
        assert self.transformer._determine_category('usuario') == 'Fundamentos'
        assert self.transformer._determine_category('tecnologia') == 'Tecnologia'
        assert self.transformer._determine_category('unknown') == 'Fundamentos'
    
    def test_determine_database(self):
        """Test database determination."""
        assert self.transformer._determine_database('estudos em design') == 'Revista Estudos em Design'
        assert self.transformer._determine_database('infodesign') == 'InfoDesign'
        assert self.transformer._determine_database('unknown_source') == 'unknown_source'
    
    def test_transform_search_results(self):
        """Test search results transformation."""
        result = self.transformer.transform_search_results(self.sample_data)
        
        assert len(result) == 2
        assert 'id' in result.columns
        assert 'timestamp' in result.columns
        assert 'relevance_score' not in result.columns  # Should not be added by transformer
        
        # Check data types
        assert result['id'].dtype == 'string'
        assert result['title'].dtype == 'string'
    
    def test_validate_transformation(self):
        """Test transformation validation."""
        # Test valid transformation
        valid_df = pd.DataFrame({
            'id': ['1', '2'],
            'title': ['Title 1', 'Title 2'],
            'link': ['http://1.com', 'http://2.com']
        })
        
        is_valid, message = self.transformer.validate_transformation(valid_df)
        assert not is_valid  # Missing required columns
        
        # Test empty DataFrame
        empty_df = pd.DataFrame()
        is_valid, message = self.transformer.validate_transformation(empty_df)
        assert not is_valid
        assert "Empty DataFrame" in message
    
    def test_get_transformation_stats(self):
        """Test transformation statistics."""
        original_df = pd.DataFrame({'col': [1, 2, 3]})
        transformed_df = pd.DataFrame({'col': [1, 2]})
        
        stats = self.transformer.get_transformation_stats(original_df, transformed_df)
        
        assert stats['original_records'] == 3
        assert stats['transformed_records'] == 2
        assert stats['missing_data'] == 1
        assert stats['success_rate'] == 66.7
    
    @patch('pandas.read_csv')
    def test_transform_and_save_results_success(self, mock_read_csv):
        """Test successful transform and save."""
        mock_read_csv.return_value = self.sample_data
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'output.csv')
            
            result = self.transformer.transform_and_save_results(
                'input.csv', output_path
            )
            
            assert result is not None
            assert len(result) == 2
    
    @patch('pandas.read_csv')
    def test_transform_and_save_results_failure(self, mock_read_csv):
        """Test failed transform and save."""
        mock_read_csv.side_effect = Exception("File not found")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'output.csv')
            
            result = self.transformer.transform_and_save_results(
                'nonexistent.csv', output_path
            )
            
            assert result is None


if __name__ == "__main__":
    pytest.main([__file__])
