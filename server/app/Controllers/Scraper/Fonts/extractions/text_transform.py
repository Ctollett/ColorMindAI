import re

def extract_text_transforms_from_css(css_text):
    """Extracts text transforms from CSS rules."""
    transforms = set()
    matches = re.findall(r'text-transform:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        transforms.add(match.strip())
    return list(transforms)

def extract_text_transforms_from_inline_styles(soup):
    """Extracts text transforms from inline styles within an HTML document."""
    transforms = set()
    for element in soup.find_all(style=True):
        match = re.search(r'text-transform:\s*([^;]+)', element['style'], re.IGNORECASE)
        if match:
            transforms.add(match.group(1).strip())
    return list(transforms)

def extract_text_transforms_from_styles(soup):
    """Extracts text transforms from <style> tags within an HTML document."""
    transforms = set()
    for style in soup.find_all('style'):
        style_content = style.string
        if style_content:
            matches = re.findall(r'text-transform:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                transforms.add(match.strip())
    return list(transforms)
