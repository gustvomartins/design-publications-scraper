"""
Scrapers for various design publication sources.
"""

from .base_scraper import BaseScraper
from .arcosdesign_scraper import ArcosDesignScraper
from .designetecnologia_scraper import DesignETecnologiaScraper
from .designtecnologiasociedade_scraper import DesignTecnologiaSociedadeScraper
from .educacaografica_scraper import EducacaoGraficaScraper
from .estudosemdesign_scraper import EstudosEmDesignScraper
from .humanfactorsindesign_scraper import HumanFactorsInDesignScraper
from .infodesign_scraper import InfoDesignScraper
from .poliedro_scraper import PoliedroScraper
from .projetica_scraper import ProjeticaScraper
from .sbc_scraper import SBCScraper
from .triades_scraper import TriadesScraper

__all__ = [
    "BaseScraper",
    "ArcosDesignScraper",
    "DesignETecnologiaScraper",
    "DesignTecnologiaSociedadeScraper",
    "EducacaoGraficaScraper",
    "EstudosEmDesignScraper",
    "HumanFactorsInDesignScraper",
    "InfoDesignScraper",
    "PoliedroScraper",
    "ProjeticaScraper",
    "SBCScraper",
    "TriadesScraper",
]
