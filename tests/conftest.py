"""
Pytest configuration and fixtures for the Design Publications Scraper tests.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

# Add src to Python path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_search_data():
    """Sample search results data for testing."""
    return pd.DataFrame({
        'title': [
            'Design de Interface para Usuários Idosos',
            'UX Design e Jornada do Usuário',
            'Testes de Usabilidade em Aplicativos Mobile',
            'Arquitetura da Informação e Análise Heurística'
        ],
        'author': [
            'João Silva',
            'Maria Santos',
            'Pedro Costa',
            'Ana Oliveira'
        ],
        'date': [
            '2023-01-15',
            '2022-12-01',
            '2023-03-20',
            '2022-11-10'
        ],
        'link': [
            'http://example1.com',
            'http://example2.com',
            'http://example3.com',
            'http://example4.com'
        ],
        'fonte': [
            'estudos_em_design',
            'infodesign',
            'human_factors_in_design',
            'arcos_design'
        ],
        'termo': [
            'usuario',
            'ux',
            'usabilidade',
            'arquitetura'
        ]
    })


@pytest.fixture
def sample_transformed_data():
    """Sample transformed data for testing."""
    return pd.DataFrame({
        'id': ['uuid1', 'uuid2', 'uuid3', 'uuid4'],
        'timestamp': [
            '24/08/2025 00:00:00',
            '24/08/2025 00:00:01',
            '24/08/2025 00:00:02',
            '24/08/2025 00:00:03'
        ],
        'title': [
            'Design de Interface para Usuários Idosos',
            'UX Design e Jornada do Usuário',
            'Testes de Usabilidade em Aplicativos Mobile',
            'Arquitetura da Informação e Análise Heurística'
        ],
        'author': [
            'João Silva',
            'Maria Santos',
            'Pedro Costa',
            'Ana Oliveira'
        ],
        'year': ['2023', '2022', '2023', '2022'],
        'type': ['Artigo', 'Artigo', 'Artigo', 'Artigo'],
        'link': [
            'http://example1.com',
            'http://example2.com',
            'http://example3.com',
            'http://example4.com'
        ],
        'database': [
            'Revista Estudos em Design',
            'InfoDesign',
            'Human Factors in Design',
            'Arcos Design'
        ],
        'category': [
            'Fundamentos',
            'Fundamentos',
            'Fundamentos',
            'Informação'
        ],
        'cover_image': ['Sem imagem', 'Sem imagem', 'Sem imagem', 'Sem imagem'],
        '🔐 Softr Record ID': ['Sem ID', 'Sem ID', 'Sem ID', 'Sem ID']
    })


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("title,author,date\n")
        f.write("Test Title,Test Author,2023\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "repos": {
            "estudos_em_design": "estudos_em_design",
            "infodesign": "infodesign"
        },
        "terms": ["usuario", "ux", "usabilidade"],
        "max_pages": 5,
        "csv_filename": "data/raw/search_results.csv",
        "data_processing": {
            "transformed_results": "data/processed/transformed_results.csv",
            "enable_auto_transform": True
        },
        "curation": {
            "curation_candidates": "data/processed/curation_candidates.csv",
            "enable_auto_filtering": True
        },
        "deduplication": {
            "base_database": "data/raw/base_database.csv",
            "new_records_output": "data/processed/new_records.csv",
            "enable_auto_dedup": True
        }
    }
