"""
Default configuration values for the Design Publications Scraper.

This module contains default configuration values that are used
when no configuration file is provided or when validation fails.
"""

DEFAULT_CONFIG = {
    "repos": {
        "estudos_em_design": "estudos_em_design",
        "infodesign": "infodesign",
        "human_factors_in_design": "human_factors_in_design",
        "arcos_design": "arcos_design",
        "design_e_tecnologia": "design_e_tecnologia",
        "triades": "triades",
        "educacao_grafica": "educacao_grafica"
    },
    "terms": [
        "experiencia", "usuario", "interface", "usabilidade",
        "interacao", "sistema", "ergonomia", "digital",
        "informacao", "tecnologia"
    ],
    "max_pages": 10,
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

# Scraper-specific configurations
SCRAPER_CONFIGS = {
    "estudos_em_design": {
        "base_url": "https://www.e-publicacoes.uerj.br/index.php/estudosdesign",
        "search_url": "https://www.e-publicacoes.uerj.br/index.php/estudosdesign/search/results",
        "max_delay": 2
    },
    "infodesign": {
        "base_url": "https://www.abedesign.org.br/infodesign",
        "search_url": "https://www.abedesign.org.br/infodesign/search",
        "max_delay": 2
    },
    "human_factors_in_design": {
        "base_url": "https://www.humanfactorsindesign.com.br",
        "search_url": "https://www.humanfactorsindesign.com.br/search",
        "max_delay": 2
    },
    "arcos_design": {
        "base_url": "https://www.arcos.org.br",
        "search_url": "https://www.arcos.org.br/search",
        "max_delay": 2
    },
    "design_e_tecnologia": {
        "base_url": "https://www.designetecnologia.org",
        "search_url": "https://www.designetecnologia.org/search",
        "max_delay": 2
    },
    "triades": {
        "base_url": "https://www.triades.ufsc.br",
        "search_url": "https://www.triades.ufsc.br/search",
        "max_delay": 2
    },
    "educacao_grafica": {
        "base_url": "https://www.educacaografica.org",
        "search_url": "https://www.educacaografica.org/search",
        "max_delay": 2
    }
}

# Data processing configurations
DATA_PROCESSING_CONFIG = {
    "batch_size": 100,
    "max_workers": 4,
    "timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 5
}

# Curation filter configurations
CURATION_CONFIG = {
    "min_relevance_score": 1,
    "language_detection_timeout": 10,
    "max_title_length": 500,
    "exclude_patterns": [
        r'^\s*$',  # Empty titles
        r'^[0-9\s\-_]+$',  # Just numbers and special chars
        r'^[a-z]{1,2}\s*$'  # Very short titles
    ]
}

# Output configurations
OUTPUT_CONFIG = {
    "encoding": "utf-8",
    "date_format": "%d/%m/%Y %H:%M:%S",
    "csv_delimiter": ",",
    "include_timestamp": True,
    "include_metadata": True
}
