import re
import math
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ColorTraitAnalyzer:
    def __init__(self, colors):
        self.colors = [self.convert_color(color) for color in colors if color]

    def convert_color(self, color):
        """Convert color to RGB tuple."""
        if color.startswith('rgba'):
            return self.rgba_to_rgb(color)
        elif color.startswith('rgb'):
            return self.rgb_to_rgb(color)
        elif color.startswith('#'):
            return self.hex_to_rgb(color)
        else:
            logging.error(f"Error converting color: {color} - Not a recognized format")
            return None

    def rgba_to_rgb(self, rgba):
        """Convert rgba color to rgb by ignoring the alpha value."""
        rgba_values = re.findall(r'\d+', rgba)
        if len(rgba_values) >= 3:
            r, g, b = map(int, rgba_values[:3])
            return (r, g, b)
        logging.error(f"Invalid RGBA color format: {rgba}")
        return None

    def rgb_to_rgb(self, rgb):
        """Convert rgb color to rgb tuple."""
        rgb_values = re.findall(r'\d+', rgb)
        if len(rgb_values) >= 3:
            r, g, b = map(int, rgb_values[:3])
            return (r, g, b)
        logging.error(f"Invalid RGB color format: {rgb}")
        return None

    def hex_to_rgb(self, hex_color):
        """Convert hex color to rgb tuple."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 3:
            return tuple(int(hex_color[i]*2, 16) for i in range(3))
        logging.error(f"Invalid Hex color format: {hex_color}")
        return None

    def rgb_to_hsl(self, rgb):
        """Convert RGB color to HSL."""
        r, g, b = [x / 255.0 for x in rgb]
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2
        if max_c == min_c:
            h = s = 0
        else:
            delta = max_c - min_c
            s = delta / (2 - max_c - min_c) if l > 0.5 else delta / (max_c + min_c)
            if max_c == r:
                h = (g - b) / delta + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / delta + 2
            elif max_c == b:
                h = (r - g) / delta + 4
            h /= 6
        return h * 360, s, l

    def classify_colors(self):
        """Classify colors based on predefined traits and return the trait with the highest score."""
        traits = {
            'Professional': {'hue_range': None, 'saturation_range': (0, 0.3), 'luminance_range': (0.2, 0.8)},
            'Creative': {'hue_range': None, 'saturation_range': (0.4, 1), 'luminance_range': (0.1, 0.9)},
            'Experimental': {'hue_range': None, 'saturation_range': (0.6, 1), 'luminance_range': (0, 1)},
            'Calm': {'hue_range': (180, 300), 'saturation_range': (0, 0.3), 'luminance_range': (0.7, 1)},
            'Playful': {'hue_range': (30, 90), 'saturation_range': (0.5, 1), 'luminance_range': (0.4, 0.8)},
            'Elegant': {'hue_range': None, 'saturation_range': (0.2, 0.5), 'luminance_range': (0.6, 1)},
            'Dynamic': {'hue_range': None, 'saturation_range': (0.6, 1), 'luminance_range': (0.3, 0.7)},
            'Authentic': {'hue_range': None, 'saturation_range': (0.3, 0.6), 'luminance_range': (0.2, 0.7)},
            'Inviting': {'hue_range': None, 'saturation_range': (0.2, 0.6), 'luminance_range': (0.5, 0.9)},
            'Sophisticated': {'hue_range': None, 'saturation_range': (0.4, 0.8), 'luminance_range': (0.3, 0.7)}
        }

        results = {}
        for trait, criteria in traits.items():
            score = self.evaluate_trait(criteria)
            results[trait] = score
            logging.debug(f"Trait: {trait}, Score: {score}")

        # Find the trait with the highest score
        best_trait = max(results, key=results.get, default="No Trait")
        best_score = results[best_trait]
        logging.info(f"Best trait for the site: {best_trait} with score {best_score:.2f}")

        # Return only the best trait
        return best_trait

    def evaluate_trait(self, criteria):
        """Evaluate colors against the given trait criteria."""
        count = 0
        valid_colors = [color for color in self.colors if color is not None]
        for color in valid_colors:
            if self.match_criteria(color, criteria):
                count += 1
        # Scoring is proportionate to the matching colors
        return count / len(valid_colors) if valid_colors else 0

    def match_criteria(self, color, criteria):
        """Check if a color matches the given trait criteria."""
        h, s, l = self.rgb_to_hsl(color)
        hue_range = criteria['hue_range']
        sat_range = criteria['saturation_range']
        lum_range = criteria['luminance_range']
        
        hue_match = (hue_range is None or (hue_range[0] <= h <= hue_range[1]))
        sat_match = (sat_range[0] <= s <= sat_range[1])
        lum_match = (lum_range[0] <= l <= lum_range[1])
        
        return hue_match and sat_match and lum_match
