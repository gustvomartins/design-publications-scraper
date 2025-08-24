"""
Scrapers for various design publication sources.
"""

from .base_scraper import BaseScraper
from .arcosdesign_scraper import ArcosDesignScraper
from .designetecnologia_scraper import DesigneTecnologiaScraper
from .educacaografica_scraper import EducacaoGraficaScraper
from .estudosemdesign_scraper import EstudosEmDesignScraper
from .humanfactorsindesign_scraper import HumanFactorsinDesignScraper
from .infodesign_scraper import InfoDesignScraper
from .triades_scraper import TriadesScraper

__all__ = [
    "BaseScraper",
    "ArcosDesignScraper",
    "DesigneTecnologiaScraper",
    "EducacaoGraficaScraper",
    "EstudosEmDesignScraper",
    "HumanFactorsinDesignScraper",
    "InfoDesignScraper",
    "TriadesScraper",
]
