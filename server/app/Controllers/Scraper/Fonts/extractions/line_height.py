import re

def extract_line_heights_from_css(css_text):
    """Extracts line heights from CSS rules."""
    heights = set()
    matches = re.findall(r'line-height:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        heights.add(match.strip())
    return list(heights)

def extract_line_heights_from_inline_styles(soup):
    """Extracts line heights from inline styles within an HTML document."""
    heights = set()
    for element in soup.find_all(style=True):
        match = re.search(r'line-height:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            heights.add(match.group(1).strip())
    return list(heights)

def extract_line_heights_from_styles(soup):
    """Extracts line heights from <style> tags within an HTML document."""
    heights = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'line-height:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                heights.add(match.strip())
    return list(heights)
