from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def search(self, term, max_pages):
        
        pass
