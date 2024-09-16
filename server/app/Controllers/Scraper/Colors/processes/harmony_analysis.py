from colour import Color
import numpy as np

def color_wheel_position(color):
    """Convert a color to its position on the color wheel."""
    hue = Color(rgb=(color[0]/255, color[1]/255, color[2]/255)).hue
    return hue * 360

def color_distance(hue1, hue2):
    """Calculate the shortest distance between two hues on the color wheel."""
    return min(abs(hue1 - hue2), 360 - abs(hue1 - hue2))

def harmony_type(distance):
    """Determine the type of harmony based on hue distance."""
    if distance < 30:
        return 'Analogous'
    elif 150 < distance < 210:
        return 'Complementary'
    elif (distance > 30 and distance < 90) or (270 < distance < 330):
        return 'Split-Complementary'
    elif (distance > 90 and distance < 150) or (210 < distance < 270):
        return 'Triadic'
    else:
        return 'Neutral'

def calculate_harmony_scores(harmony_counts):
    """Calculate harmony scores from harmony type counts."""
    score = 0
    total = sum(harmony_counts.values())
    if total > 0:
        # Weights can be adjusted based on design principles
        weights = {
            'Complementary': 10,
            'Analogous': 8,
            'Triadic': 7,
            'Split-Complementary': 9,
            'Neutral': 1
        }
        for harmony, count in harmony_counts.items():
            score += (count / total) * weights[harmony]
    return round(score, 2)

def evaluate_harmony(colors):
    """Evaluate the harmony of a set of colors based on their positions on the color wheel."""
    hues = [color_wheel_position(color) for color in colors]
    harmony_counts = {'Analogous': 0, 'Complementary': 0, 'Triadic': 0, 'Split-Complementary': 0, 'Neutral': 0}
    for i, hue1 in enumerate(hues):
        for j in range(i + 1, len(hues)):
            distance = color_distance(hue1, hues[j])
            harmony = harmony_type(distance)
            harmony_counts[harmony] += 1
    return calculate_harmony_scores(harmony_counts)

# Example usage
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
print(evaluate_harmony(colors))
