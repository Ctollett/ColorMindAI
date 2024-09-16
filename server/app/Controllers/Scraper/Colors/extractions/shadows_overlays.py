import re
from bs4 import BeautifulSoup

def extract_shadows_and_overlays(soup):
    """
    Extracts shadow properties and overlay styles from both inline styles and <style> tags.
    """
    shadow_details = set()
    overlay_details = set()

    # Helper regex
    shadow_regex = re.compile(r'(?:box-shadow|text-shadow):\s*([^;]+)', re.IGNORECASE)
    overlay_regex = re.compile(r'background:\s*rgba\([^)]+\)', re.IGNORECASE)

    # Extract from inline styles
    for tag in soup.find_all(style=True):
        style_content = tag['style']
        shadow_matches = shadow_regex.findall(style_content)
        overlay_matches = overlay_regex.findall(style_content)
        shadow_details.update(shadow_matches)
        overlay_details.update(overlay_matches)

    # Extract from <style> tags
    style_tags = soup.find_all('style')
    for style in style_tags:
        css_text = style.get_text()
        shadow_matches = shadow_regex.findall(css_text)
        overlay_matches = overlay_regex.findall(css_text)
        shadow_details.update(shadow_matches)
        overlay_details.update(overlay_matches)

    return {'shadows': shadow_details, 'overlays': overlay_details}
