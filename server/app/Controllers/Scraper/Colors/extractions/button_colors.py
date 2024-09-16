import re

def extract_button_colors_from_inline_styles(soup):
    """
    Extract button colors from inline styles.
    """
    button_colors = set()
    for tag in soup.find_all(style=True):
        style = tag.get('style')
        colors = re.findall(r'background-color:\s*([^;]+);?', style, re.IGNORECASE)
        button_colors.update(colors)
    return button_colors

def extract_button_colors_from_styles(soup):
    """
    Extract button colors from <style> tags.
    """
    button_colors = set()
    style_tags = soup.find_all('style')
    for style in style_tags:
        css_text = style.get_text()
        colors = re.findall(r'background-color:\s*([^;]+);?', css_text, re.IGNORECASE)
        button_colors.update(colors)
    return button_colors

def extract_button_colors_from_css(css_text):
    """
    Extract button colors from external CSS text.
    """
    button_colors = set()
    colors = re.findall(r'background-color:\s*([^;]+);?', css_text, re.IGNORECASE)
    button_colors.update(colors)
    return button_colors
