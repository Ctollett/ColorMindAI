import re
import logging
from bs4 import BeautifulSoup

def extract_form_field_colors_from_css(css):
    logging.debug("Extracting form field colors from CSS")
    form_field_color_pattern = re.compile(r'(input|textarea|select|button)\s*{\s*(.*?)}', re.IGNORECASE)
    color_pattern = re.compile(r'(color|background-color|border-color)\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([0-9,\s]+\)|hsla?\([0-9,\s%]+\))', re.IGNORECASE)

    form_fields = form_field_color_pattern.findall(css)
    color_dict = {}

    for field, styles in form_fields:
        colors = color_pattern.findall(styles)
        for context, color in colors:
            if color not in color_dict:
                color_dict[color] = set()
            color_dict[color].add(f'{field}-{context}')

    return color_dict

def extract_form_field_colors_from_inline_styles(soup):
    logging.debug("Extracting form field colors from inline styles")
    form_field_tags = ['input', 'textarea', 'select', 'button']
    color_dict = {}

    for tag in form_field_tags:
        for element in soup.find_all(tag):
            style = element.get('style')
            if style:
                colors = extract_form_field_colors_from_css(style)
                for color, contexts in colors.items():
                    if color not in color_dict:
                        color_dict[color] = set()
                    color_dict[color].update(contexts)

    return color_dict

def extract_form_field_colors_from_styles(soup):
    logging.debug("Extracting form field colors from <style> tags")
    form_field_tags = ['input', 'textarea', 'select', 'button']
    color_dict = {}

    for style in soup.find_all('style'):
        css = style.text
        colors = extract_form_field_colors_from_css(css)
        for color, contexts in colors.items():
            if color not in color_dict:
                color_dict[color] = set()
            color_dict[color].update(contexts)

    return color_dict
