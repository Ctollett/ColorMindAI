import re
from bs4 import BeautifulSoup

def extract_feedback_colors(soup):
    """
    Extracts error and success colors from both inline styles and <style> tags based on common naming conventions.
    """
    error_colors = set()
    success_colors = set()

    # Common class indicators for error and success messages
    error_indicators = ["error", "danger", "alert-danger", "invalid", "failure"]
    success_indicators = ["success", "valid", "alert-success", "passed"]

    # Helper function to parse color from styles
    def parse_colors(style_content, indicators):
        colors = set()
        for indicator in indicators:
            if indicator in style_content:
                color_matches = re.findall(r'color:\s*([^;]+)', style_content, re.IGNORECASE)
                background_matches = re.findall(r'background(?:-color)?:\s*([^;]+)', style_content, re.IGNORECASE)
                colors.update(color_matches)
                colors.update(background_matches)
        return colors

    # Extract from inline styles
    for tag in soup.find_all(style=True):
        style_content = tag['style']
        if any(indicator in style_content.lower() for indicator in error_indicators):
            error_colors.update(parse_colors(style_content, error_indicators))
        if any(indicator in style_content.lower() for indicator in success_indicators):
            success_colors.update(parse_colors(style_content, success_indicators))

    # Extract from <style> tags
    style_tags = soup.find_all('style')
    for style in style_tags:
        css_text = style.get_text().lower()
        error_colors.update(parse_colors(css_text, error_indicators))
        success_colors.update(parse_colors(css_text, success_indicators))

    return {'error_colors': error_colors, 'success_colors': success_colors}
