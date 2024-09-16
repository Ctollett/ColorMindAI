import re
import logging
import requests

def extract_secondary_colors_from_css(css):
    logging.debug("Extracting secondary colors from CSS")
    secondary_color_pattern = re.compile(r'(color|background-color|border-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = secondary_color_pattern.findall(css)
    
    return set(color[1] for color in colors)

def extract_secondary_colors_from_inline_styles(soup):
    logging.debug("Extracting secondary colors from inline styles")
    secondary_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_secondary_colors_from_css(style)
            secondary_colors.update(colors)
    return secondary_colors

def extract_secondary_colors_from_styles(soup):
    logging.debug("Extracting secondary colors from <style> tags")
    secondary_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_secondary_colors_from_css(css)
        secondary_colors.update(colors)
    return secondary_colors

def fetch_secondary_colors_from_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS for secondary colors: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        return extract_secondary_colors_from_css(css_text)
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()
