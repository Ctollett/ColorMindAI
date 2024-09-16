import re
import logging
from bs4 import BeautifulSoup
import requests 
import colorsys

def extract_accent_colors_from_css(css):
    logging.debug("Extracting accent colors from CSS")
    accent_color_pattern = re.compile(r'(color|background-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = accent_color_pattern.findall(css)
    
    accent_colors = set()
    for context, color in colors:
        # Assuming accent colors are typically brighter and more saturated
        if is_accent_color(color):
            accent_colors.add(color)
    
    return accent_colors

def extract_accent_colors_from_inline_styles(soup):
    logging.debug("Extracting accent colors from inline styles")
    accent_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_accent_colors_from_css(style)
            accent_colors.update(colors)
    return accent_colors

def extract_accent_colors_from_styles(soup):
    logging.debug("Extracting accent colors from <style> tags")
    accent_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_accent_colors_from_css(css)
        accent_colors.update(colors)
    return accent_colors

def fetch_accent_colors_from_external_css(css_url, headers):
    logging.debug(f"Fetching external CSS: {css_url}")
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        css_text = response.text
        accent_colors = extract_accent_colors_from_css(css_text)
        return accent_colors
    except requests.RequestException as e:
        logging.error(f"Error fetching external CSS: {e}")
        return set()

def is_accent_color(color):
    # Simple heuristic to determine if a color is an accent color
    # Accent colors are typically more saturated and brighter
    if color.startswith('#'):
        r, g, b = hex_to_rgb(color)
        h, l, s = rgb_to_hls(r, g, b)
        return s > 0.5 and l > 0.5  # Adjust thresholds as needed
    elif color.startswith('rgb'):
        match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color)
        if match:
            r, g, b = map(int, match.groups())
            h, l, s = rgb_to_hls(r, g, b)
            return s > 0.5 and l > 0.5  # Adjust thresholds as needed
    elif color.startswith('hsl'):
        match = re.match(r'hsla?\((\d+),\s*(\d+)%?,\s*(\d+)%?', color)
        if match:
            h, s, l = map(int, match.groups())
            return s > 50 and l > 50  # Adjust thresholds as needed
    return False

def hex_to_rgb(hex_color):
    # Strip the '#' character if it's present
    hex_color = hex_color.lstrip('#')
    
    # Check if hex_color is a valid hex code
    if len(hex_color) not in {3, 6} or not all(c in '0123456789abcdefABCDEF' for c in hex_color):
        logging.error(f"Invalid hex color code: {hex_color}")
        return None  # Or handle the error as appropriate for your application

    # Convert short hex color codes to full length (e.g., 'abc' -> 'aabbcc')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)

    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hls(r, g, b):
    """ Convert RGB to HLS (Hue, Lightness, Saturation). """
    return colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)