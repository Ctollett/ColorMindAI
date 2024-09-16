import re
import logging
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_text_colors_from_css(css):
    """Extract text colors from CSS text."""
    logging.debug("Extracting text colors from CSS")
    
    # Regex pattern to find text color
    color_pattern = re.compile(r'color\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    
    colors = set(color_pattern.findall(css))
    return colors

def extract_text_colors_from_inline_styles(soup):
    """Extract text colors from inline styles."""
    logging.debug("Extracting text colors from inline styles")
    colors = set()
    
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors.update(extract_text_colors_from_css(style))
    
    return colors

def extract_text_colors_from_styles(soup):
    """Extract text colors from <style> tags."""
    logging.debug("Extracting text colors from <style> tags")
    colors = set()
    
    for style in soup.find_all('style'):
        css = style.text
        colors.update(extract_text_colors_from_css(css))
    
    return colors

def fetch_text_colors_from_external_css(css_url, headers):
    """Fetch and extract text colors from external CSS."""
    logging.debug(f"Fetching external CSS for text colors: {css_url}")
    
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        return extract_text_colors_from_css(css_text)
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()