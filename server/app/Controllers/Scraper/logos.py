import requests
from bs4 import BeautifulSoup

def find_logo(soup, base_url):
    logo_selectors = [
        'header img',
        'img.logo',
        'img[alt*="logo"]',
        'img[src*="logo"]',
        'img[alt*="brand"]',
        'img[src*="brand"]'
    ]
    
    for selector in logo_selectors:
        logo = soup.select_one(selector)
        if logo:
            logo_src = logo.get('src')
            if logo_src:
                if not logo_src.startswith('http'):
                    logo_src = requests.compat.urljoin(base_url, logo_src)
                return logo_src

    favicon = soup.find('link', rel='icon')
    if favicon:
        logo_src = favicon.get('href')
        if logo_src:
            if not logo_src.startswith('http'):
                logo_src = requests.compat.urljoin(base_url, logo_src)
            return logo_src
    return None
