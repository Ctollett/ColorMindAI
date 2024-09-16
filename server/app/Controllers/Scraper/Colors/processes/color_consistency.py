import logging
from collections import Counter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_consistency(colors):
    """
    Scores the color consistency based on the dominance and frequency of color usage.
    
    :param colors: A list of colors used on the website.
    :return: Consistency score from 1 to 10.
    """
    color_count = Counter(colors)
    total_colors = sum(color_count.values())
    most_common_colors = color_count.most_common(3)
    dominant_percentage = sum(freq for _, freq in most_common_colors) / total_colors

    logging.debug(f"Total colors: {total_colors}, Most common: {most_common_colors}")

    if dominant_percentage > 0.75:
        return 10  # Highly consistent
    elif dominant_percentage > 0.50:
        return 7  # Moderately consistent
    elif dominant_percentage > 0.25:
        return 4  # Somewhat consistent
    else:
        return 1  # Low consistency


