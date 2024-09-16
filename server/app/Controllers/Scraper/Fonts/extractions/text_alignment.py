import re

def extract_text_alignments_from_css(css_text):
    """Extracts text alignments from CSS rules."""
    alignments = set()
    matches = re.findall(r'text-align:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        alignments.add(match.strip())
    return list(alignments)

def extract_text_alignments_from_inline_styles(soup):
    """Extracts text alignments from inline styles within an HTML document."""
    alignments = set()
    for element in soup.find_all(style=True):
        match = re.search(r'text-align:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            alignments.add(match.group(1).strip())
    return list(alignments)

def extract_text_alignments_from_styles(soup):
    """Extracts text alignments from <style> tags within an HTML document."""
    alignments = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'text-align:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                alignments.add(match.strip())
    return list(alignments)
