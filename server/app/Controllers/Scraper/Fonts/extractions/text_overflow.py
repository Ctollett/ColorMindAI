import re

def extract_text_overflow_from_css(css_text):
    """Extracts text overflow properties from CSS rules."""
    overflows = set()
    matches = re.findall(r'text-overflow:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        overflows.add(match.strip())
    return list(overflows)

def extract_text_overflow_from_inline_styles(soup):
    """Extracts text overflow properties from inline styles within an HTML document."""
    overflows = set()
    for element in soup.find_all(style=True):
        match = re.search(r'text-overflow:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            overflows.add(match.group(1).strip())
    return list(overflows)

def extract_text_overflow_from_styles(soup):
    """Extracts text overflow properties from <style> tags within an HTML document."""
    overflows = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'text-overflow:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                overflows.add(match.strip())
    return list(overflows)
