import requests
from bs4 import BeautifulSoup
import cssutils

def fetch_css_stylesheets(soup, base_url):
    """Fetches and returns all CSS rules from stylesheets linked in the HTML."""
    styles = []
    for link in soup.find_all('link'):
        if 'stylesheet' in link.get('rel', []):
            href = link.get('href')
            if href:
                try:
                    response = requests.get(base_url + href)
                    sheet = cssutils.parseString(response.content)
                    styles.extend(sheet.cssRules)
                except requests.exceptions.RequestException as e:
                    print(f"Failed to fetch stylesheet: {href}")
    return styles

def extract_font_sizes_from_css(rules):
    """Extracts font sizes from CSS rules."""
    font_sizes = set()
    for rule in rules:
        if rule.type == rule.STYLE_RULE:
            for property in rule.style:
                if property.name == 'font-size':
                    font_sizes.add(property.value)
    return font_sizes

def extract_font_sizes_from_inline_styles(soup):
    """Extracts font sizes from inline styles within the HTML."""
    font_sizes = set()
    for element in soup.find_all(style=True):
        style = cssutils.parseStyle(element['style'])
        font_size = style.getPropertyValue('font-size')
        if font_size:
            font_sizes.add(font_size)
    return font_sizes

def extract_font_sizes_from_styles(soup, base_url):
    """Fetches and extracts font sizes from stylesheets linked in the HTML."""
    css_rules = fetch_css_stylesheets(soup, base_url)
    return extract_font_sizes_from_css(css_rules)
