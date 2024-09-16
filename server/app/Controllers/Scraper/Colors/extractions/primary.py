import re
import logging
import requests

def extract_primary_colors_from_css(css):
    logging.debug("Extracting primary colors from CSS")
    primary_color_pattern = re.compile(r'(color|background-color|border-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = primary_color_pattern.findall(css)
    
    return set(color[1] for color in colors)

def extract_primary_colors_from_inline_styles(soup):
    logging.debug("Extracting primary colors from inline styles")
    primary_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_primary_colors_from_css(style)
            primary_colors.update(colors)
    return primary_colors

def extract_primary_colors_from_styles(soup):
    logging.debug("Extracting primary colors from <style> tags")
    primary_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_primary_colors_from_css(css)
        primary_colors.update(colors)
    return primary_colors

def fetch_primary_colors_from_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS for primary colors: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        return extract_primary_colors_from_css(css_text)
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()
