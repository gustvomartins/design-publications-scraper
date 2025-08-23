from scrapers.estudosemdesign_scraper import EstudosEmDesignScraper
from scrapers.infodesign_scraper import InfoDesignScraper

from scrapers.humanfactorsindesign_scraper import HumanFactorsinDesignScraper
from scrapers.arcosdesign_scraper import ArcosDesignScraper
from scrapers.designetecnologia_scraper import DesigneTecnologiaScraper
from scrapers.triades_scraper import TriadesScraper
from scrapers.educacaografica_scraper import EducacaoGraficaScraper

class ScrapterFactory:
    @staticmethod
    def get_scraper(scraper_name: str):
        scrapers = {
            "estudos_em_design": EstudosEmDesignScraper(base_url="https://estudosemdesign.emnuvens.com.br/design/search/search"),
            "infodesign": InfoDesignScraper(base_url="https://www.infodesign.org.br/infodesign/search/index"),
            "human_factors_in_design": HumanFactorsinDesignScraper(base_url="https://www.revistas.udesc.br/index.php/hfd/search/index"),
            "arcos_design": ArcosDesignScraper(base_url="https://www.e-publicacoes.uerj.br/arcosdesign/search/index"),
            "design_e_tecnologia": DesigneTecnologiaScraper(base_url="https://www.ufrgs.br/det/index.php/det/search/search"),
            "triades": TriadesScraper(base_url="https://periodicos.ufjf.br/index.php/triades/search/search"),
            "educacao_grafica": EducacaoGraficaScraper(base_url="https://www.educacaografica.inf.br/")
        }

        scraper = scrapers.get(scraper_name)

        if scraper is None:
            raise ValueError(f"Scraper '{scraper_name}' não encontrado.")
        
        return scraper