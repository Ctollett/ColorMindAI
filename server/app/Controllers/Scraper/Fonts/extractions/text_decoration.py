import re

def extract_text_decorations_from_css(css_text):
    """Extracts text decorations from CSS rules."""
    decorations = set()
    matches = re.findall(r'text-decoration:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        decorations.add(match.strip())
    return list(decorations)

def extract_text_decorations_from_inline_styles(soup):
    """Extracts text decorations from inline styles within an HTML document."""
    decorations = set()
    for element in soup.find_all(style=True):
        match = re.search(r'text-decoration:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            decorations.add(match.group(1).strip())
    return list(decorations)

def extract_text_decorations_from_styles(soup):
    """Extracts text decorations from <style> tags within an HTML document."""
    decorations = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'text-decoration:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                decorations.add(match.strip())
    return list(decorations)

