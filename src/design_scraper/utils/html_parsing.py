from bs4 import BeautifulSoup

class HTMLParser:
    """Classe para parsing de HTML"""
    
    @staticmethod
    def extract_text_or_default(tag, default="N/A"):
        """Extrai texto de uma tag HTML ou retorna valor padrão"""
        return tag.get_text(strip=True) if tag else default

    @staticmethod
    def extract_attribute_or_default(tag, attribute, default="N/A"):
        """Extrai atributo de uma tag HTML ou retorna valor padrão"""
        return tag[attribute] if tag and attribute in tag.attrs else default


def extract_text_or_default(tag, default="N/A"):
    """Função de conveniência para extração de texto"""
    return HTMLParser.extract_text_or_default(tag, default)

def extract_attribute_or_default(tag, attribute, default="N/A"):
    """Função de conveniência para extração de atributos"""
    return HTMLParser.extract_attribute_or_default(tag, attribute, default)