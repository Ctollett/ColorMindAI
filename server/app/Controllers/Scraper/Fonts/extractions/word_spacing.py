import re

def extract_word_spacing_from_css(css_text):
    """Extracts word spacing from CSS rules."""
    spacings = set()
    matches = re.findall(r'word-spacing:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        spacings.add(match.strip())
    return list(spacings)

def extract_word_spacing_from_inline_styles(soup):
    """Extracts word spacing from inline styles within an HTML document."""
    spacings = set()
    for element in soup.find_all(style=True):
        match = re.search(r'word-spacing:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            spacings.add(match.group(1).strip())
    return list(spacings)

def extract_word_spacing_from_styles(soup):
    """Extracts word spacing from <style> tags within an HTML document."""
    spacings = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'word-spacing:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                spacings.add(match.strip())
    return list(spacings)
