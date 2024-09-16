import re

def extract_font_styles_from_css(css_text):
    """Extracts font styles from CSS rules."""
    styles = set()
    matches = re.findall(r'font-style:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        styles.add(match.strip())
    return list(styles)

def extract_font_styles_from_inline_styles(soup):
    """Extracts font styles from inline styles within an HTML document."""
    styles = set()
    for element in soup.find_all(style=True):
        match = re.search(r'font-style:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            styles.add(match.group(1).strip())
    return list(styles)

def extract_font_styles_from_styles(soup):
    """Extracts font styles from <style> tags within an HTML document."""
    styles = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'font-style:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                styles.add(match.strip())
    return list(styles)
