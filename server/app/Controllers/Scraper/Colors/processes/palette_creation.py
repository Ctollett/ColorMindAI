import logging
from sklearn.cluster import KMeans
import numpy as np

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ColorPaletteGenerator:
    def __init__(self, colors, num_clusters=5):
        if not colors:
            logging.error("No colors provided for palette generation.")
            raise ValueError("Colors list cannot be empty.")
        
        logging.debug(f"Received colors: {colors}")

        self.colors = np.array(colors)
        if self.colors.ndim != 2 or self.colors.shape[1] != 3:
            logging.error("Colors must be a list of RGB tuples.")
            raise ValueError("Colors must be a list of RGB tuples.")
        
        self.num_clusters = min(num_clusters, len(colors))
        logging.debug(f"Initialized with colors: {self.colors}")

    def generate_palette(self):
        """
        Generate a color palette using K-Means clustering and return it in HEX format.
        """
        try:
            kmeans = KMeans(n_clusters=self.num_clusters, random_state=0).fit(self.colors)
            palette_rgb = kmeans.cluster_centers_.astype(int)
            palette_hex = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette_rgb]
            logging.debug(f"Generated color palette in HEX: {palette_hex}")
            return palette_hex
        except Exception as e:
            logging.error(f"Error generating color palette: {e}")
            return []

