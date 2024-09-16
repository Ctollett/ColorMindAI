import re
import logging
import requests

def fetch_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        return css_text
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return ""

def extract_colors_from_css(css_text):
    logging.debug("Extracting colors from CSS text")
    color_pattern = re.compile(r'(color|background-color|border-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = color_pattern.findall(css_text)
    
    color_dict = {}
    for context, color in colors:
        if color not in color_dict:
            color_dict[color] = set()
        color_dict[color].add(context)
    
    return color_dict

def fetch_and_extract_colors_from_external_css(css_url, headers):
    css_text = fetch_external_css(css_url, headers)
    return extract_colors_from_css(css_text)
