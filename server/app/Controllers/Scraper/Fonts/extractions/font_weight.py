import re

def extract_font_weights_from_css(css_text):
    """Extracts font weights from CSS rules."""
    weights = set()
    matches = re.findall(r'font-weight:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        weights.add(match.strip())
    return list(weights)

def extract_font_weights_from_inline_styles(soup):
    """Extracts font weights from inline styles within an HTML document."""
    weights = set()
    for element in soup.find_all(style=True):
        match = re.search(r'font-weight:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            weights.add(match.group(1).strip())
    return list(weights)

def extract_font_weights_from_styles(soup):
    """Extracts font weights from <style> tags within an HTML document."""
    weights = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'font-weight:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                weights.add(match.strip())
    return list(weights)
