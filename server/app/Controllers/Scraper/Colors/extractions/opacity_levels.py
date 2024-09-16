import re
from bs4 import BeautifulSoup

def extract_opacity_levels(soup):
    """
    Extracts opacity levels from both inline styles and <style> tags in the HTML content.
    """
    opacity_levels = set()

    # Extracting from inline styles
    for tag in soup.find_all(style=True):
        style_content = tag['style']
        opacity_matches = re.findall(r'opacity:\s*([^;]+)', style_content, re.IGNORECASE)
        rgba_matches = re.findall(r'rgba\([^)]+\)', style_content, re.IGNORECASE)
        hsla_matches = re.findall(r'hsla\([^)]+\)', style_content, re.IGNORECASE)
        opacity_levels.update(opacity_matches)
        opacity_levels.update(rgba_matches)
        opacity_levels.update(hsla_matches)

    # Extracting from <style> tags
    style_tags = soup.find_all('style')
    for style in style_tags:
        css_text = style.get_text()
        opacity_matches = re.findall(r'opacity:\s*([^;]+)', css_text, re.IGNORECASE)
        rgba_matches = re.findall(r'rgba\([^)]+\)', css_text, re.IGNORECASE)
        hsla_matches = re.findall(r'hsla\([^)]+\)', css_text, re.IGNORECASE)
        opacity_levels.update(opacity_matches)
        opacity_levels.update(rgba_matches)
        opacity_levels.update(hsla_matches)

    return opacity_levels
