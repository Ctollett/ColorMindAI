import re

def extract_text_shadows_from_css(css_text):
    """Extracts text shadows from CSS rules."""
    shadows = set()
    matches = re.findall(r'text-shadow:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        shadows.add(match.strip())
    return list(shadows)

def extract_text_shadows_from_inline_styles(soup):
    """Extracts text shadows from inline styles within an HTML document."""
    shadows = set()
    for element in soup.find_all(style=True):
        match = re.search(r'text-shadow:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            shadows.add(match.group(1).strip())
    return list(shadows)

def extract_text_shadows_from_styles(soup):
    """Extracts text shadows from <style> tags within an HTML document."""
    shadows = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'text-shadow:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                shadows.add(match.strip())
    return list(shadows)
