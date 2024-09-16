import re

def extract_text_colors_from_css(css_text):
    """Extracts text colors from CSS rules."""
    colors = set()
    matches = re.findall(r'color:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        colors.add(match.strip())
    return list(colors)

def extract_text_colors_from_inline_styles(soup):
    """Extracts text colors from inline styles within an HTML document."""
    colors = set()
    for element in soup.find_all(style=True):
        match = re.search(r'color:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            colors.add(match.group(1).strip())
    return list(colors)

def extract_text_colors_from_styles(soup):
    """Extracts text colors from <style> tags within an HTML document."""
    colors = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'color:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                colors.add(match.strip())
    return list(colors)
