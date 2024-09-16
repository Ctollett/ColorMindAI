import re
import logging
from collections import Counter

def extract_color_patterns_from_css(css):
    """
    Extracts recurring color patterns from CSS.
    """
    logging.debug("Extracting color patterns from CSS")
    color_pattern = re.compile(r'(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)
    colors = color_pattern.findall(css)
    color_counter = Counter(colors)
    return color_counter

def extract_color_patterns_from_inline_styles(soup):
    """
    Extracts recurring color patterns from inline styles in HTML soup.
    """
    logging.debug("Extracting color patterns from inline styles")
    color_counter = Counter()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            colors = extract_color_patterns_from_css(style)
            color_counter.update(colors)
    return color_counter

def extract_color_patterns_from_styles(soup):
    """
    Extracts recurring color patterns from <style> tags in HTML soup.
    """
    logging.debug("Extracting color patterns from <style> tags")
    color_counter = Counter()
    for style in soup.find_all('style'):
        css = style.text
        colors = extract_color_patterns_from_css(css)
        color_counter.update(colors)
    return color_counter

