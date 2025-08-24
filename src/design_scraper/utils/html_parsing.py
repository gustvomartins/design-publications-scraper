from bs4 import BeautifulSoup

def extract_text_or_default(tag, default="N/A"):

    return tag.get_text(strip=True) if tag else default

def extract_attribute_or_default(tag, attribute, default="N/A"):

    return tag[attribute] if tag and attribute in tag.attrs else default