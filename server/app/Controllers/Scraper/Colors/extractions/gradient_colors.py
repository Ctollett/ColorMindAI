import re
import logging

def extract_gradient_colors_from_css(css):
    logging.debug("Extracting gradient colors from CSS")
    gradient_pattern = re.compile(r'linear-gradient\s*\(([^)]+)\)', re.IGNORECASE)
    gradients = gradient_pattern.findall(css)
    
    return set(gradients)

def extract_gradient_colors_from_inline_styles(soup):
    logging.debug("Extracting gradient colors from inline styles")
    gradient_colors = set()
    for element in soup.find_all(style=True):
        style = element.get('style')
        if style:
            gradients = extract_gradient_colors_from_css(style)
            gradient_colors.update(gradients)
    return gradient_colors

def extract_gradient_colors_from_styles(soup):
    logging.debug("Extracting gradient colors from <style> tags")
    gradient_colors = set()
    for style in soup.find_all('style'):
        css = style.text
        gradients = extract_gradient_colors_from_css(css)
        gradient_colors.update(gradients)
    return gradient_colors
