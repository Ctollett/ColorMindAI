import re
import math
import logging
from colour import Color

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def normalize_color_to_rgb(color):
    """Converts any CSS color to normalized RGB tuple."""
    try:
        normalized_color = Color(color)
        return tuple(int(x * 255) for x in normalized_color.rgb)
    except ValueError as e:
        logging.error(f"Invalid color format or unable to convert: {color} - {e}")
        return None

def validate_rgb(rgb_color):
    """Checks if the RGB color format is correct (each component in the range 0-255)."""
    if rgb_color and all(0 <= x <= 255 for x in rgb_color):
        return True
    return False

def is_valid_color_value(color_value):
    """Check if the extracted value is a valid color."""
    # Accepts hex codes with and without #, and 3 or 6 characters long
    hex_color_pattern = re.compile(r'^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
    rgba_color_pattern = re.compile(r'^rgba?\(\d{1,3},\d{1,3},\d{1,3}(?:,\d*\.?\d+)?\)$')
    hsla_color_pattern = re.compile(r'^hsla?\(\d{1,3},\d{1,3}%,\d{1,3}%(?:,\d*\.?\d+)?\)$')
    return bool(hex_color_pattern.match(color_value) or rgba_color_pattern.match(color_value) or hsla_color_pattern.match(color_value))


def normalize_hex_code(hex_code):
    """Normalize shorter hex codes or those missing a '#' to a full 6-digit hex code with a '#'."""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([ch*2 for ch in hex_code])  # Convert 'abc' to 'aabbcc'
    if len(hex_code) < 6:
        hex_code = hex_code.ljust(6, '0')  # Pad with zeroes if shorter than 6 characters
    return f'#{hex_code}'

def convert_to_rgb(hex_code):
    """Convert normalized hex code to RGB tuple."""
    hex_code = normalize_hex_code(hex_code)
    r, g, b = int(hex_code[1:3], 16), int(hex_code[3:5], 16), int(hex_code[5:7], 16)
    return r, g, b


def convert_color_format_to_rgb(color_str):
    """
    Converts color strings from CSS formats (RGB, RGBA, HSL, HSLA) to an RGB tuple.
    Example inputs: 'rgb(255,0,0)', 'rgba(255,0,0,0.5)', 'hsl(120,100%,50%)', 'hsla(120,100%,50%,0.3)'
    """
    try:
        # The Color library automatically strips out whitespace and lowercases the input
        c = Color(color_str)
        return tuple(int(x * 255) for x in c.rgb)  # Convert from fractional RGB to 0-255 RGB
    except ValueError as e:
        logging.error(f"Failed to convert color format: {color_str} - Error: {e}")
        return None


# Example usage
hex_input = "000c"
if is_valid_color_value(hex_input):
    rgb_output = convert_to_rgb(hex_input)
    print("RGB Output:", rgb_output)
else:
    print("Invalid Hex Code")

def convert_and_normalize_colors(color_list):
    """Processes a list of colors, converting them to a normalized RGB format and ignoring invalid colors."""
    normalized_colors = set()
    for color in color_list:
        if not is_valid_color_value(color):
            logging.error(f"Skipping invalid color format: {color}")
            continue

        if color.startswith('#') and len(color) in [4, 7]:  # Proper hex codes
            rgb_color = normalize_color_to_rgb(color)
        elif re.match(r'^[0-9a-fA-F]{3,6}$', color):  # Hex codes without '#'
            color = normalize_hex_code(color)
            rgb_color = normalize_color_to_rgb(color)
        else:
            converted_color = convert_color_format_to_rgb(color)
            rgb_color = normalize_color_to_rgb(converted_color)

        if rgb_color and validate_rgb(rgb_color):
            normalized_colors.add(rgb_color)
        else:
            logging.error(f"Failed to normalize or validate RGB values for color: {color}")

    return list(normalized_colors)

def rgba_to_hex(rgba):
    try:
        parts = [int(x) for x in re.findall(r'\d+', rgba)[:3]]
        if len(parts) == 3:
            return f'#{parts[0]:02x}{parts[1]:02x}{parts[2]:02x}'
    except Exception as e:
        logging.error(f"Failed to convert RGBA to hex: {e}")
    return None

def rgba_to_hex(rgba):
    """Convert rgba color to hex by ignoring the alpha value."""
    rgba_values = re.findall(r'\d+', rgba)
    if len(rgba_values) >= 3:
        r, g, b = map(int, rgba_values[:3])
        return f'#{r:02x}{g:02x}{b:02x}'
    logging.error(f"Invalid RGBA color format: {rgba}")
    return None

def rgb_to_hex(rgb):
    """Convert rgb color to hex."""
    rgb_values = re.findall(r'\d+', rgb)
    if len(rgb_values) >= 3:
        r, g, b = map(int, rgb_values[:3])
        return f'#{r:02x}{g:02x}{b:02x}'
    logging.error(f"Invalid RGB color format: {rgb}")
    return None

def hsla_to_hex(hsla):
    """Convert hsla color to hex by converting to rgb first."""
    hsla_values = re.findall(r'[\d.]+', hsla)
    if len(hsla_values) >= 3:
        h, s, l = map(float, hsla_values[:3])
        h = h / 360
        s = s / 100
        l = l / 100

        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1/6:
                return p + (q - p) * 6 * t
            if t < 1/2:
                return q
            if t < 2/3:
                return p + (q - p) * (2/3 - t) * 6
            return p

        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)

        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
    logging.error(f"Invalid HSLA color format: {hsla}")
    return None