import math
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def luminance(r, g, b):
    """
    Calculate the luminance of a color using its RGB components.
    """
    a = [v / 255.0 for v in (r, g, b)]
    a = [(v / 12.92 if v <= 0.03928 else math.pow((v + 0.055) / 1.055, 2.4)) for v in a]
    luminance_value = 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]
    logging.debug(f"Luminance for RGB {r, g, b}: {luminance_value}")
    return luminance_value

def contrast_ratio(color1, color2):
    """
    Calculate the contrast ratio between two colors given as (R, G, B).
    """
    L1 = luminance(*color1)
    L2 = luminance(*color2)
    ratio = (L1 + 0.05) / (L2 + 0.05) if L1 > L2 else (L2 + 0.05) / (L1 + 0.05)
    logging.debug(f"Contrast ratio between {color1} and {color2}: {ratio}")
    return ratio


def scale_contrast_ratio_to_score(contrast_ratio):
    """
    Scale the contrast ratio to a 1-10 score.
    """
    if contrast_ratio < 1:
        score = 1
    elif contrast_ratio < 3:
        score = 2 + (contrast_ratio - 1) / 2 * 3  # Increase score more quickly between 1 and 3
    elif contrast_ratio < 4.5:
        score = 5 + (contrast_ratio - 3) / 1.5 * 2  # Increase score more quickly between 3 and 4.5
    elif contrast_ratio < 7:
        score = 7 + (contrast_ratio - 4.5) / 2.5 * 2  # Increase score more quickly between 4.5 and 7
    else:
        score = 9 + (contrast_ratio - 7) / 14 * 1  # Less increment for very high contrast ratios
    score = min(score, 10)  # Ensure the score does not exceed 10
    logging.debug(f"Score for contrast ratio {contrast_ratio}: {score}")
    return score

def average_contrast_score(colors):
    colors = list(colors)  # Convert set to list to allow indexing
    total_score = 0
    num_comparisons = 0
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            color1, color2 = colors[i], colors[j]
            ratio = contrast_ratio(color1, color2)
            score = scale_contrast_ratio_to_score(ratio)
            total_score += score
            num_comparisons += 1
    average_score = total_score / num_comparisons if num_comparisons > 0 else 0
    rounded_score = round(average_score, 2)  # Round the average score to 2 decimal places
    logging.debug(f"Average contrast score (rounded): {rounded_score}")
    return rounded_score

# Example usage:
colors = {(255, 255, 255), (0, 0, 0), (128, 128, 128)}
print(average_contrast_score(colors))


