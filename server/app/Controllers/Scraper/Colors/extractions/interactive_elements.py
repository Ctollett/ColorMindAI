import re
import logging
from bs4 import BeautifulSoup
import requests 

def extract_interactive_element_colors_from_css(css):
    logging.debug("Extracting interactive element colors from CSS")
    interactive_elements_pattern = re.compile(r'(button|a|input|select|textarea)\s*{[^}]*}', re.IGNORECASE)
    elements = interactive_elements_pattern.findall(css)
    
    color_pattern = re.compile(r'(color|background-color|border-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    
    colors = set()
    for element in elements:
        colors.update(color_pattern.findall(element))
    
    return colors

def extract_interactive_element_colors_from_inline_styles(soup):
    logging.debug("Extracting interactive element colors from inline styles")
    colors = set()
    for element in soup.find_all(['button', 'a', 'input', 'select', 'textarea'], style=True):
        style = element.get('style')
        if style:
            colors.update(extract_interactive_element_colors_from_css(style))
    return colors

def extract_interactive_element_colors_from_styles(soup):
    logging.debug("Extracting interactive element colors from <style> tags")
    colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors.update(extract_interactive_element_colors_from_css(css))
    return colors

def fetch_interactive_element_colors_from_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS for interactive elements: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        return extract_interactive_element_colors_from_css(css_text)
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()
