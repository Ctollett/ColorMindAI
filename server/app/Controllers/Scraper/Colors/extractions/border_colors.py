import re
import logging
import requests
from bs4 import BeautifulSoup

def extract_border_colors_from_css(css):
    logging.debug("Extracting border colors from CSS")
    border_color_pattern = re.compile(r'border-color\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = border_color_pattern.findall(css)
    
    return set(colors)

def extract_border_colors_from_inline_styles(soup):
    logging.debug("Extracting border colors from inline styles")
    border_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_border_colors_from_css(style)
            border_colors.update(colors)
    return border_colors

def extract_border_colors_from_styles(soup):
    logging.debug("Extracting border colors from <style> tags")
    border_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_border_colors_from_css(css)
        border_colors.update(colors)
    return border_colors

def fetch_border_colors_from_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        colors = extract_border_colors_from_css(css_text)
        return colors
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()
