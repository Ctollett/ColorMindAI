import logging
import re
from .processes.contrast_ratio import average_contrast_score
from .processes.color_conversion import convert_and_normalize_colors
from .processes.harmony_analysis import evaluate_harmony
from .processes.color_consistency import evaluate_consistency
from .processes.color_mood import ColorTraitAnalyzer
from .processes.palette_creation import ColorPaletteGenerator

def is_valid_hex(color):
    return re.match(r'^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$', color) is not None

def is_valid_rgb(color):
    return re.match(r'^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$', color) is not None

def is_valid_rgba(color):
    return re.match(r'^rgba\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(0|0\.\d+|1(\.0)?)\)$', color) is not None

def validate_colors(colors):
    valid_colors = []
    for color in colors:
        if is_valid_hex(color) or is_valid_rgb(color) or is_valid_rgba(color):
            valid_colors.append(color)
        else:
            logging.warning(f"Invalid color format detected: {color}")
    return valid_colors

def normalize_hex_code(hex_code):
    """Normalize shorter hex codes or those missing a '#' to a full 6-digit hex code with a '#'."""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([ch*2 for ch in hex_code])  # Convert 'abc' to 'aabbcc'
    if len(hex_code) < 6:
        # If the hex code is like '000c', it is likely incorrect and should be handled or logged
        if re.match(r'^[0-9a-fA-F]{4}$', hex_code):
            hex_code = hex_code[:3]  # Taking the first three characters might be a safe assumption
        hex_code = hex_code.ljust(6, '0')  # Pad with zeroes if shorter than 6 characters
    return f'#{hex_code}'


def gather_all_color_values(scraped_colors):
    all_colors = []
    for color_category in scraped_colors.values():
        if isinstance(color_category, set):
            for color in color_category:
                normalized_color = normalize_hex_code(color) if '#' in color or len(color) == 3 or len(color) == 6 else color
                all_colors.append(normalized_color)
        elif isinstance(color_category, dict):  # Assuming some categories might be dictionaries
            for sub_category in color_category.values():
                if isinstance(sub_category, set):
                    for color in sub_category:
                        normalized_color = normalize_hex_code(color) if '#' in color or len(color) == 3 or len(color) == 6 else color
                        all_colors.append(normalized_color)
    return all_colors


def log_results(results):
    if results:
        logging.info("\nColor Analysis Results:")
        logging.info(f"Contrast Score: {results['contrast']:.2f} (Scale 1-10)")
        logging.info(f"Harmony Score: {results['harmony']:.2f} (Scale 1-10)")
        logging.info(f"Consistency Score: {results['consistency']:.2f} (Scale 1-10)")
        logging.info(f"Best Trait: {results['best_trait']}")  # Log only the best trait
        logging.info("\nNormalized Colors (RGB):")
        for color in results['normalized_colors']:
            logging.info(f"RGB: {color}")
        logging.info("\nGenerated Color Palette:")
        for color in results['color_palette']:
            logging.info(f"RGB: {color}")
    else:
        logging.info("No results to log.")

def process_colors(scraped_colors):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting color processing...")

    try:
        all_color_values = gather_all_color_values(scraped_colors)
        if not all_color_values:
            logging.warning("No colors found in scraped data.")
            return None  # Return None explicitly to indicate no data to process

        valid_colors = validate_colors(all_color_values)
        if not valid_colors:
            logging.warning("No valid colors found after validation. Exiting process.")
            return None

        normalized_colors = convert_and_normalize_colors(valid_colors)
        if not normalized_colors:
            logging.error("Failed to normalize colors. Check color formats.")
            return None
  

        contrast_results = average_contrast_score(normalized_colors)
        harmony_results = evaluate_harmony(normalized_colors)
        consistency_results = evaluate_consistency(normalized_colors)

        # Get only the best trait instead of all traits
        best_trait = ColorTraitAnalyzer(valid_colors).classify_colors()

        color_palette = ColorPaletteGenerator(normalized_colors).generate_palette()
        if not color_palette:
            logging.error("Failed to generate color palette.")
            return None

        results = {
            'contrast': contrast_results,
            'harmony': harmony_results,
            'consistency': consistency_results,
            'best_trait': best_trait,  # Store only the best trait
            'normalized_colors': normalized_colors,
            'color_palette': color_palette
        }

        log_results(results)
        return results

    except Exception as e:
        logging.error(f"Error processing colors: {e}")
        logging.warning("No results were retrieved or processed.")
        return None


