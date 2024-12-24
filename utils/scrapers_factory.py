from scrapers.estudosemdesign_scraper import EstudosEmDesignScraper
from scrapers.infodesign_scraper import InfoDesignScraper
from scrapers.repositorioufrn_scraper import RepositorioUfrnScraper
from scrapers.humanfactorsindesign_scraper import HumanFactorsinDesignScraper

class ScrapterFactory:
    @staticmethod
    def get_scraper(scraper_name: str):
        scrapers = {
            "estudos_em_design": EstudosEmDesignScraper(base_url="https://estudosemdesign.emnuvens.com.br/design/search/search"),
            "infodesign": InfoDesignScraper(base_url="https://www.infodesign.org.br/infodesign/search/index"),
            "repositorio_ufrn": RepositorioUfrnScraper(base_url="https://repositorio.ufrn.br/simple-search"),
            "human_factors_in_design": HumanFactorsinDesignScraper(base_url="https://www.revistas.udesc.br/index.php/hfd/search/index")
        }

        scraper = scrapers.get(scraper_name)

        if scraper is None:
            raise ValueError(f"Scraper '{scraper_name}' não encontrado.")
        
        return scraper