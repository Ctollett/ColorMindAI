import re

def extract_font_variants_from_css(css_text):
    """Extracts font variants from CSS rules."""
    variants = set()
    matches = re.findall(r'font-variant:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        variants.add(match.strip())
    return list(variants)

def extract_font_variants_from_inline_styles(soup):
    """Extracts font variants from inline styles within an HTML document."""
    variants = set()
    for element in soup.find_all(style=True):
        match = re.search(r'font-variant:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            variants.add(match.group(1).strip())
    return list(variants)

def extract_font_variants_from_styles(soup):
    """Extracts font variants from <style> tags within an HTML document."""
    variants = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'font-variant:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                variants.add(match.strip())
    return list(variants)
