import re
import logging
import requests
from bs4 import BeautifulSoup

def extract_background_colors_from_css(css):
    logging.debug("Extracting background colors from CSS")
    background_color_pattern = re.compile(r'background-color\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = background_color_pattern.findall(css)
    
    return set(colors)

def extract_background_colors_from_inline_styles(soup):
    logging.debug("Extracting background colors from inline styles")
    background_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_background_colors_from_css(style)
            background_colors.update(colors)
    return background_colors

def extract_background_colors_from_styles(soup):
    logging.debug("Extracting background colors from <style> tags")
    background_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_background_colors_from_css(css)
        background_colors.update(colors)
    return background_colors

def fetch_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        colors = extract_background_colors_from_css(css_text)
        return colors
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()

def get_external_css_links(soup):
    links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = link.get('href')
        if css_url:
            links.append(css_url)
    return links
