from bs4 import BeautifulSoup
import re

def extract_font_families_from_css(css_text):
    """
    Extracts all font-family declarations from a given CSS text.

    Args:
    css_text (str): A string containing CSS content.

    Returns:
    list of str: A list of unique font families found in the CSS text.
    """
    fonts = set()
    # Regular expression to find font-family declarations
    matches = re.findall(r'font-family:\s*([^;]+)', css_text, re.IGNORECASE)
    for match in matches:
        # Clean and split the fonts by comma
        individual_fonts = [font.strip().strip('"').strip("'") for font in match.split(',')]
        fonts.update(individual_fonts)

    return list(fonts)

def extract_inline_font_families(html_data):
    """
    Extracts all font-family declarations from inline styles within an HTML document.

    Args:
    html_data (str): A string containing HTML content.

    Returns:
    list of str: A list of unique font families found in the inline styles.
    """
    soup = BeautifulSoup(html_data, 'lxml')
    fonts = set()

    # Find all elements with a style attribute
    for element in soup.find_all(style=True):
        style_content = element['style']
        # Look for font-family within each style attribute
        match = re.search(r'font-family:\s*([^;]+)', style_content)
        if match:
            # Clean and split the fonts by comma
            individual_fonts = [font.strip().strip('"').strip("'") for font in match.group(1).split(',')]
            fonts.update(individual_fonts)

    return list(fonts)

def extract_font_families_from_inline_styles(soup):
    """
    Extracts all font-family declarations from inline styles within a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): A BeautifulSoup object containing parsed HTML content.

    Returns:
    list of str: A list of unique font families found in the inline styles.
    """
    return extract_inline_font_families(str(soup))

def extract_font_families_from_styles(soup):
    """
    Extracts all font-family declarations from <style> tags within an HTML document.

    Args:
    soup (BeautifulSoup): A BeautifulSoup object containing parsed HTML content.

    Returns:
    list of str: A list of unique font families found in the <style> tags.
    """
    styles = soup.find_all('style')
    fonts = set()

    for style in styles:
        style_content = style.string
        if style_content:
            matches = re.findall(r'font-family:\s*([^;]+)', style_content, re.IGNORECASE)
            for match in matches:
                # Clean and split the fonts by comma
                individual_fonts = [font.strip().strip('"').strip("'") for font in match.split(',')]
                fonts.update(individual_fonts)

    return list(fonts)
