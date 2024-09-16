import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def count_color_usage(color_data):
    """
    Count the frequency of each color across different categories.
    
    Args:
        color_data (dict): Dictionary with categories as keys and sets or lists of colors as values.
        
    Returns:
        dict: Dictionary with color frequencies.
    """
    color_counter = Counter()
    
    for category, colors in color_data.items():
        if isinstance(colors, set):
            color_counter.update(colors)
        elif isinstance(colors, list):
            color_counter.update(colors)
        else:
            logging.warning(f"Unexpected data type for category {category}: {type(colors)}")
    
    logging.debug(f"Color usage counts: {color_counter}")
    return color_counter

def analyze_color_distribution(color_data):
    """
    Analyze how colors are distributed across different categories.
    
    Args:
        color_data (dict): Dictionary with categories as keys and sets or lists of colors as values.
        
    Returns:
        dict: Dictionary with category-wise color distribution.
    """
    distribution = {}
    
    for category, colors in color_data.items():
        if isinstance(colors, set):
            distribution[category] = len(colors)
        elif isinstance(colors, list):
            distribution[category] = len(set(colors))  # Unique colors count
        else:
            logging.warning(f"Unexpected data type for category {category}: {type(colors)}")
    
    logging.debug(f"Color distribution by category: {distribution}")
    return distribution

def analyze_color_usage(color_data):
    """
    Analyze color usage including counts and distribution.
    
    Args:
        color_data (dict): Dictionary with categories as keys and sets or lists of colors as values.
        
    Returns:
        dict: Dictionary with color usage counts and distribution.
    """
    usage_counts = count_color_usage(color_data)
    distribution = analyze_color_distribution(color_data)
    
    analysis_result = {
        'color_usage_counts': usage_counts,
        'color_distribution': distribution
    }
    
    logging.debug(f"Color usage analysis result: {analysis_result}")
    return analysis_result

if __name__ == "__main__":
    # Example usage
    color_data = {
        'accent_colors': ['#ff0000', '#00ff00', '#ff0000'],
        'background_colors': ['#0000ff', '#ff0000'],
        'border_colors': ['#008000', '#ff0000'],
        'text_colors': ['#ffff00', '#ff0000']
    }
    
    analysis_results = analyze_color_usage(color_data)
    print(analysis_results)
