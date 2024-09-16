import logging
import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin

# Import existing extraction functions
from .extractions.accent import extract_accent_colors_from_css, extract_accent_colors_from_inline_styles, extract_accent_colors_from_styles
from .extractions.background_colors import extract_background_colors_from_css, extract_background_colors_from_inline_styles, extract_background_colors_from_styles
from .extractions.border_colors import extract_border_colors_from_css, extract_border_colors_from_inline_styles, extract_border_colors_from_styles
from .extractions.color_patterns import extract_color_patterns_from_css, extract_color_patterns_from_inline_styles, extract_color_patterns_from_styles
from .extractions.form_field_colors import extract_form_field_colors_from_css, extract_form_field_colors_from_inline_styles, extract_form_field_colors_from_styles
from .extractions.gradient_colors import extract_gradient_colors_from_css, extract_gradient_colors_from_inline_styles, extract_gradient_colors_from_styles
from .extractions.interactive_elements import extract_interactive_element_colors_from_css, extract_interactive_element_colors_from_inline_styles, extract_interactive_element_colors_from_styles
from .extractions.mouse_state_colors import extract_mouse_state_colors_from_css, extract_mouse_state_colors_from_inline_styles, extract_mouse_state_colors_from_styles
from .extractions.notification_colors import extract_notification_colors_from_css, extract_notification_colors_from_inline_styles, extract_notification_colors_from_styles
from .extractions.primary import extract_primary_colors_from_css, extract_primary_colors_from_inline_styles, extract_primary_colors_from_styles, fetch_primary_colors_from_external_css
from .extractions.secondary import extract_secondary_colors_from_css, extract_secondary_colors_from_inline_styles, extract_secondary_colors_from_styles, fetch_secondary_colors_from_external_css
from .extractions.text_colors import extract_text_colors_from_css, extract_text_colors_from_inline_styles, extract_text_colors_from_styles
from .extractions.text_and_background import extract_text_and_background_colors_from_css as extract_background_colors_from_css_for_text, extract_text_and_background_colors_from_inline_styles as extract_background_colors_from_inline_styles_for_text, extract_text_and_background_colors_from_styles as extract_background_colors_from_styles_for_text
from .extractions.button_colors import extract_button_colors_from_css, extract_button_colors_from_inline_styles, extract_button_colors_from_styles
from .extractions.error_colors import extract_feedback_colors
from .extractions.shadows_overlays import extract_shadows_and_overlays
from .extractions.opacity_levels import extract_opacity_levels


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_external_css(css_url, headers):

    try:
        response = requests.get(css_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
 
        return ""

def get_external_css_links(soup):
    links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = link.get('href')
        if css_url:
            links.append(css_url)
    return links

def fetch_and_extract_colors_from_external_css(css_url, headers):
    css_text = fetch_external_css(css_url, headers)
    accent_colors = extract_accent_colors_from_css(css_text)
    background_colors = extract_background_colors_from_css(css_text)
    border_colors = extract_border_colors_from_css(css_text)
    color_patterns = extract_color_patterns_from_css(css_text)
    form_field_colors = extract_form_field_colors_from_css(css_text)
    gradient_colors = extract_gradient_colors_from_css(css_text)
    interactive_element_colors = extract_interactive_element_colors_from_css(css_text)
    mouse_state_colors = extract_mouse_state_colors_from_css(css_text)
    notification_colors = extract_notification_colors_from_css(css_text)
    primary_colors = extract_primary_colors_from_css(css_text)
    secondary_colors = extract_secondary_colors_from_css(css_text)
    text_colors = extract_text_colors_from_css(css_text)
    return (accent_colors, background_colors, border_colors, color_patterns, form_field_colors,
            gradient_colors, interactive_element_colors, mouse_state_colors, notification_colors,
            primary_colors, secondary_colors, text_colors)

def scrape_colors(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract inline and <style> tag colors
    inline_accent_colors = extract_accent_colors_from_inline_styles(soup)
    style_accent_colors = extract_accent_colors_from_styles(soup)
    inline_background_colors = extract_background_colors_from_inline_styles(soup)
    style_background_colors = extract_background_colors_from_styles(soup)
    inline_border_colors = extract_border_colors_from_inline_styles(soup)
    style_border_colors = extract_border_colors_from_styles(soup)
    inline_color_patterns = extract_color_patterns_from_inline_styles(soup)
    style_color_patterns = extract_color_patterns_from_styles(soup)
    inline_form_field_colors = extract_form_field_colors_from_inline_styles(soup)
    style_form_field_colors = extract_form_field_colors_from_styles(soup)
    inline_gradient_colors = extract_gradient_colors_from_inline_styles(soup)
    style_gradient_colors = extract_gradient_colors_from_styles(soup)
    inline_interactive_element_colors = extract_interactive_element_colors_from_inline_styles(soup)
    style_interactive_element_colors = extract_interactive_element_colors_from_styles(soup)
    inline_mouse_state_colors = extract_mouse_state_colors_from_inline_styles(soup)
    style_mouse_state_colors = extract_mouse_state_colors_from_styles(soup)
    inline_notification_colors = extract_notification_colors_from_inline_styles(soup)
    style_notification_colors = extract_notification_colors_from_styles(soup)
    inline_primary_colors = extract_primary_colors_from_inline_styles(soup)
    style_primary_colors = extract_primary_colors_from_styles(soup)
    inline_secondary_colors = extract_secondary_colors_from_inline_styles(soup)
    style_secondary_colors = extract_secondary_colors_from_styles(soup)
    
    inline_text_colors = extract_text_colors_from_inline_styles(soup)
    style_text_colors = extract_text_colors_from_styles(soup)
    inline_background_colors_for_text = extract_background_colors_from_inline_styles_for_text(soup)
    style_background_colors_for_text = extract_background_colors_from_styles_for_text(soup)

    inline_button_colors = extract_button_colors_from_inline_styles(soup)
    style_button_colors = extract_button_colors_from_styles(soup)

    feedback_colors = extract_feedback_colors(soup)
    shadows_and_overlays = extract_shadows_and_overlays(soup)
    opacity_levels = extract_opacity_levels(soup)

    # Fetch external CSS links
    external_css_links = get_external_css_links(soup)
    external_accent_colors = set()
    external_background_colors = set()
    external_border_colors = set()
    external_color_patterns = Counter()
    external_form_field_colors = set()
    external_gradient_colors = set()
    external_interactive_element_colors = set()
    external_mouse_state_colors = set()
    external_notification_colors = set()
    external_primary_colors = set()
    external_secondary_colors = set()
    external_text_colors = set()
    external_button_colors = set() 
    external_feedback_colors = {'error_colors': set(), 'success_colors': set()}
    external_shadows_and_overlays = {'shadows': set(), 'overlays': set()}
    external_opacity_levels = set()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for css_url in external_css_links:
        (accent, background, border, patterns, form_fields, gradients, interactive_elements,
         mouse_states, notifications, primary, secondary, text_colors) = fetch_and_extract_colors_from_external_css(css_url, headers)
        external_accent_colors.update(accent)
        external_background_colors.update(background)
        external_border_colors.update(border)
        external_color_patterns.update(patterns)
        external_form_field_colors.update(form_fields)
        external_gradient_colors.update(gradients)
        external_interactive_element_colors.update(interactive_elements)
        external_mouse_state_colors.update(mouse_states)
        external_notification_colors.update(notifications)
        external_primary_colors.update(primary)
        external_secondary_colors.update(secondary)
        external_text_colors.update(text_colors)
        external_button_colors.update(extract_button_colors_from_css(fetch_external_css(css_url, headers)))
        external_feedback_colors.update(extract_feedback_colors(soup))
        external_shadows_and_overlays.update(extract_shadows_and_overlays(soup))
        external_opacity_levels.update(extract_opacity_levels(soup))

    # Combine all colors
    all_accent_colors = inline_accent_colors.union(style_accent_colors, external_accent_colors)
    all_background_colors = inline_background_colors.union(style_background_colors, external_background_colors)
    all_border_colors = inline_border_colors.union(style_border_colors, external_border_colors)
    all_color_patterns = inline_color_patterns + style_color_patterns + external_color_patterns
    
    all_form_field_colors = set(inline_form_field_colors).union(style_form_field_colors, external_form_field_colors)

    all_gradient_colors = inline_gradient_colors.union(style_gradient_colors, external_gradient_colors)
    all_interactive_element_colors = inline_interactive_element_colors.union(style_interactive_element_colors, external_interactive_element_colors)
    all_mouse_state_colors = inline_mouse_state_colors.union(style_mouse_state_colors, external_mouse_state_colors)
    all_notification_colors = inline_notification_colors.union(style_notification_colors, external_notification_colors)
    all_primary_colors = inline_primary_colors.union(style_primary_colors, external_primary_colors)
    all_secondary_colors = inline_secondary_colors.union(style_secondary_colors, external_secondary_colors)
    all_text_colors = inline_text_colors.union(style_text_colors, external_text_colors)
    
    # Filtering tuples before union operation
    inline_background_colors_for_text = {c for c in inline_background_colors_for_text if isinstance(c, str)}
    style_background_colors_for_text = {c for c in style_background_colors_for_text if isinstance(c, str)}
    external_background_colors_for_text = {c for c in external_background_colors if isinstance(c, str)}

    all_background_colors_for_text = inline_background_colors_for_text.union(style_background_colors_for_text, external_background_colors_for_text)

    all_button_colors = inline_button_colors.union(style_button_colors, external_button_colors)
    all_feedback_colors = {
        'error_colors': feedback_colors['error_colors'].union(external_feedback_colors['error_colors']),
        'success_colors': feedback_colors['success_colors'].union(external_feedback_colors['success_colors'])
    }
    all_shadows_and_overlays = {
        'shadows': shadows_and_overlays['shadows'].union(external_shadows_and_overlays['shadows']),
        'overlays': shadows_and_overlays['overlays'].union(external_shadows_and_overlays['overlays'])
    }
    all_opacity_levels = opacity_levels.union(external_opacity_levels)

    return {
        'accent_colors': all_accent_colors,
        'background_colors': all_background_colors,
        'border_colors': all_border_colors,
        'color_patterns': all_color_patterns,
        'form_field_colors': all_form_field_colors,
        'gradient_colors': all_gradient_colors,
        'interactive_element_colors': all_interactive_element_colors,
        'mouse_state_colors': all_mouse_state_colors,
        'notification_colors': all_notification_colors,
        'primary_colors': all_primary_colors,
        'secondary_colors': all_secondary_colors,
        'text_colors': all_text_colors,
        'background_colors_for_text': all_background_colors_for_text,
        'button_colors': all_button_colors,
        'feedback_colors': all_feedback_colors,
        'shadows_and_overlays': all_shadows_and_overlays,
        'opacity_levels': all_opacity_levels 
    }

