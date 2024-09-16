import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Import existing extraction functions for font properties
from app.Controllers.Scraper.Fonts.extractions.font_family import extract_font_families_from_css, extract_font_families_from_inline_styles, extract_font_families_from_styles
from app.Controllers.Scraper.Fonts.extractions.font_sizes import extract_font_sizes_from_css, extract_font_sizes_from_inline_styles, extract_font_sizes_from_styles
from app.Controllers.Scraper.Fonts.extractions.font_styles import extract_font_styles_from_css, extract_font_styles_from_inline_styles, extract_font_styles_from_styles
from app.Controllers.Scraper.Fonts.extractions.font_variant import extract_font_variants_from_css, extract_font_variants_from_inline_styles, extract_font_variants_from_styles
from app.Controllers.Scraper.Fonts.extractions.font_weight import extract_font_weights_from_css, extract_font_weights_from_inline_styles, extract_font_weights_from_styles
from app.Controllers.Scraper.Fonts.extractions.letter_spacing import extract_letter_spacing_from_css, extract_letter_spacing_from_inline_styles, extract_letter_spacing_from_styles
from app.Controllers.Scraper.Fonts.extractions.line_height import extract_line_heights_from_css, extract_line_heights_from_inline_styles, extract_line_heights_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_alignment import extract_text_alignments_from_css, extract_text_alignments_from_inline_styles, extract_text_alignments_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_color import extract_text_colors_from_css, extract_text_colors_from_inline_styles, extract_text_colors_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_decoration import extract_text_decorations_from_css, extract_text_decorations_from_inline_styles, extract_text_decorations_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_overflow import extract_text_overflow_from_css, extract_text_overflow_from_inline_styles, extract_text_overflow_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_shadow import extract_text_shadows_from_css, extract_text_shadows_from_inline_styles, extract_text_shadows_from_styles
from app.Controllers.Scraper.Fonts.extractions.text_transform import extract_text_transforms_from_css, extract_text_transforms_from_inline_styles, extract_text_transforms_from_styles
from app.Controllers.Scraper.Fonts.extractions.word_spacing import extract_word_spacing_from_css, extract_word_spacing_from_inline_styles, extract_word_spacing_from_styles

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_external_css(css_url, headers):
    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Failed to fetch external CSS from {css_url}: {e}")
        return ""

def get_external_css_links(soup, base_url):
    links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = link.get('href')
        if css_url:
            links.append(urljoin(base_url, css_url))
    return links

def fetch_and_extract_fonts_from_external_css(css_url, headers):
    css_text = fetch_external_css(css_url, headers)
    font_families = extract_font_families_from_css(css_text)
    font_sizes = extract_font_sizes_from_css(css_text)
    font_styles = extract_font_styles_from_css(css_text)
    font_variants = extract_font_variants_from_css(css_text)
    font_weights = extract_font_weights_from_css(css_text)
    letter_spacing = extract_letter_spacing_from_css(css_text)
    line_heights = extract_line_heights_from_css(css_text)
    text_alignments = extract_text_alignments_from_css(css_text)
    text_colors = extract_text_colors_from_css(css_text)
    text_decorations = extract_text_decorations_from_css(css_text)
    text_overflow = extract_text_overflow_from_css(css_text)
    text_shadows = extract_text_shadows_from_css(css_text)
    text_transforms = extract_text_transforms_from_css(css_text)
    word_spacing = extract_word_spacing_from_css(css_text)
    return {
        'font_families': font_families, 'font_sizes': font_sizes, 'font_styles': font_styles,
        'font_variants': font_variants, 'font_weights': font_weights, 'letter_spacing': letter_spacing,
        'line_heights': line_heights, 'text_alignments': text_alignments, 'text_colors': text_colors,
        'text_decorations': text_decorations, 'text_overflow': text_overflow, 'text_shadows': text_shadows,
        'text_transforms': text_transforms, 'word_spacing': word_spacing
    }

def scrape_fonts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    base_url = response.url

    # Inline and <style> tag fonts extraction
    inline_font_families = extract_font_families_from_inline_styles(soup)
    style_font_families = extract_font_families_from_styles(soup)
    inline_font_sizes = extract_font_sizes_from_inline_styles(soup)
    style_font_sizes = extract_font_sizes_from_styles(soup, base_url)  # Ensure base_url is passed here
    inline_font_styles = extract_font_styles_from_inline_styles(soup)
    style_font_styles = extract_font_styles_from_styles(soup)
    inline_font_variants = extract_font_variants_from_inline_styles(soup)
    style_font_variants = extract_font_variants_from_styles(soup)
    inline_font_weights = extract_font_weights_from_inline_styles(soup)
    style_font_weights = extract_font_weights_from_styles(soup)
    inline_letter_spacing = extract_letter_spacing_from_inline_styles(soup)
    style_letter_spacing = extract_letter_spacing_from_styles(soup)
    inline_line_heights = extract_line_heights_from_inline_styles(soup)
    style_line_heights = extract_line_heights_from_styles(soup)
    inline_text_alignments = extract_text_alignments_from_inline_styles(soup)
    style_text_alignments = extract_text_alignments_from_styles(soup)
    inline_text_colors = extract_text_colors_from_inline_styles(soup)
    style_text_colors = extract_text_colors_from_styles(soup)
    inline_text_decorations = extract_text_decorations_from_inline_styles(soup)
    style_text_decorations = extract_text_decorations_from_styles(soup)
    inline_text_overflow = extract_text_overflow_from_inline_styles(soup)
    style_text_overflow = extract_text_overflow_from_styles(soup)
    inline_text_shadows = extract_text_shadows_from_inline_styles(soup)
    style_text_shadows = extract_text_shadows_from_styles(soup)
    inline_text_transforms = extract_text_transforms_from_inline_styles(soup)
    style_text_transforms = extract_text_transforms_from_styles(soup)
    inline_word_spacing = extract_word_spacing_from_inline_styles(soup)
    style_word_spacing = extract_word_spacing_from_styles(soup)

    # Fetch external CSS links and extract fonts
    external_css_links = get_external_css_links(soup, base_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    all_fonts = []
    for css_url in external_css_links:
        fonts = fetch_and_extract_fonts_from_external_css(css_url, headers)
        all_fonts.append(fonts)

    # Combine all font data
    combined_fonts = {
        'font_families': set(),
        'font_sizes': set(),
        'font_styles': set(),
        'font_variants': set(),
        'font_weights': set(),
        'letter_spacing': set(),
        'line_heights': set(),
        'text_alignments': set(),
        'text_colors': set(),
        'text_decorations': set(),
        'text_overflow': set(),
        'text_shadows': set(),
        'text_transforms': set(),
        'word_spacing': set(),
    }
    # Populate combined_fonts with data from inline, style, and external sources
    combined_fonts['font_families'].update(inline_font_families)
    combined_fonts['font_families'].update(style_font_families)
    combined_fonts['font_sizes'].update(inline_font_sizes)
    combined_fonts['font_sizes'].update(style_font_sizes)
    combined_fonts['font_styles'].update(inline_font_styles)
    combined_fonts['font_styles'].update(style_font_styles)
    combined_fonts['font_variants'].update(inline_font_variants)
    combined_fonts['font_variants'].update(style_font_variants)
    combined_fonts['font_weights'].update(inline_font_weights)
    combined_fonts['font_weights'].update(style_font_weights)
    combined_fonts['letter_spacing'].update(inline_letter_spacing)
    combined_fonts['letter_spacing'].update(style_letter_spacing)
    combined_fonts['line_heights'].update(inline_line_heights)
    combined_fonts['line_heights'].update(style_line_heights)
    combined_fonts['text_alignments'].update(inline_text_alignments)
    combined_fonts['text_alignments'].update(style_text_alignments)
    combined_fonts['text_colors'].update(inline_text_colors)
    combined_fonts['text_colors'].update(style_text_colors)
    combined_fonts['text_decorations'].update(inline_text_decorations)
    combined_fonts['text_decorations'].update(style_text_decorations)
    combined_fonts['text_overflow'].update(inline_text_overflow)
    combined_fonts['text_overflow'].update(style_text_overflow)
    combined_fonts['text_shadows'].update(inline_text_shadows)
    combined_fonts['text_shadows'].update(style_text_shadows)
    combined_fonts['text_transforms'].update(inline_text_transforms)
    combined_fonts['text_transforms'].update(style_text_transforms)
    combined_fonts['word_spacing'].update(inline_word_spacing)
    combined_fonts['word_spacing'].update(style_word_spacing)
    for fonts in all_fonts:
        combined_fonts['font_families'].update(fonts['font_families'])
        combined_fonts['font_sizes'].update(fonts['font_sizes'])
        combined_fonts['font_styles'].update(fonts['font_styles'])
        combined_fonts['font_variants'].update(fonts['font_variants'])
        combined_fonts['font_weights'].update(fonts['font_weights'])
        combined_fonts['letter_spacing'].update(fonts['letter_spacing'])
        combined_fonts['line_heights'].update(fonts['line_heights'])
        combined_fonts['text_alignments'].update(fonts['text_alignments'])
        combined_fonts['text_colors'].update(fonts['text_colors'])
        combined_fonts['text_decorations'].update(fonts['text_decorations'])
        combined_fonts['text_overflow'].update(fonts['text_overflow'])
        combined_fonts['text_shadows'].update(fonts['text_shadows'])
        combined_fonts['text_transforms'].update(fonts['text_transforms'])
        combined_fonts['word_spacing'].update(fonts['word_spacing'])

    return combined_fonts

# Example of using this script
if __name__ == "__main__":
    url = 'http://example.com'
    fonts_data = scrape_fonts(url)
    print("Fonts Data Collected:", fonts_data)
