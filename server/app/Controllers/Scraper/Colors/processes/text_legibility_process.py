import logging
from .contrast_ratio import contrast_ratio  # Import contrast_ratio from the previously defined module

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_contrast_ratio(hex_text_color, hex_background_color):
    """
    Calculate and return the contrast ratio between text and background colors.
    
    Args:
        hex_text_color (str): HEX color code for the text color.
        hex_background_color (str): HEX color code for the background color.
        
    Returns:
        float: The contrast ratio between text and background colors.
    """
    ratio = contrast_ratio(hex_text_color, hex_background_color)
    logging.debug(f"Contrast ratio between text color {hex_text_color} and background color {hex_background_color}: {ratio:.2f}")
    return ratio

def assess_legibility(hex_text_color, hex_background_color, min_contrast_ratio=4.5):
    """
    Assess whether the contrast ratio between text and background colors meets accessibility standards.
    
    Args:
        hex_text_color (str): HEX color code for the text color.
        hex_background_color (str): HEX color code for the background color.
        min_contrast_ratio (float): Minimum contrast ratio for accessibility (default: 4.5).
        
    Returns:
        bool: True if the contrast ratio meets or exceeds the minimum, False otherwise.
    """
    ratio = check_contrast_ratio(hex_text_color, hex_background_color)
    meets_criteria = ratio >= min_contrast_ratio
    if meets_criteria:
        logging.info(f"Text color {hex_text_color} and background color {hex_background_color} meet accessibility standards with a contrast ratio of {ratio:.2f}.")
    else:
        logging.warning(f"Text color {hex_text_color} and background color {hex_background_color} do not meet accessibility standards with a contrast ratio of {ratio:.2f}.")
    return meets_criteria

if __name__ == "__main__":
    # Example usage
    text_color = '#ffffff'  # White text color
    background_color = '#000000'  # Black background color
    min_ratio = 4.5  # Minimum contrast ratio for normal text

    result = assess_legibility(text_color, background_color, min_ratio)
    print(f"Legibility assessment result: {result}")
