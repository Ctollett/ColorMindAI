import logging
import json
from app.Controllers.Scraper.Colors.scrape_colors import scrape_colors
from app.Controllers.Scraper.Colors.process_colors import process_colors
from app.Controllers.Scraper.Colors.analyze_colors import analyze_color_results
from app.Controllers.Scraper.Fonts.scrape_fonts import scrape_fonts


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_colors_and_analyze(url):
    logging.info(f"Starting to scrape and preprocess URL: {url}")

    try:
        # Step 1: Scrape the colors
        scraped_colors = scrape_colors(url)

        scraped_fonts = scrape_fonts(url)
        logging.debug(f"Scraped Fonts: {scraped_fonts}")

        # Step 2: Preprocess the scraped colors
        processed_colors = process_colors(scraped_colors)


        



        # Step 3: Analyze the processed colors
        if processed_colors:
            # Prepare the data to format as expected in the prompt
            formatted_data = {
                'contrast_ratio': processed_colors.get('contrast', 0),
                'harmony_score': processed_colors.get('harmony', 0),
                'best_trait': processed_colors.get('best_trait', 'No dominant trait'),
                'normalized_colors': processed_colors.get('normalized_colors', []),
                'color_palette': processed_colors.get('color_palette', [])
            }
            

            
            # Analyze the processed colors using ChatGPT
            analysis = analyze_color_results(formatted_data)
            return {
                'scraped_colors': scraped_colors,
                'processed_colors': processed_colors,
                'analysis': analysis
            }
        else:
            logging.warning("Processed colors are empty. Skipping analysis.")
            return None
    except Exception as e:
        logging.error(f"Error in processing and analyzing colors: {e}")
        return None

def scrape_website(url):


    try:
        # Call the function that handles the scraping and preprocessing process
        results = process_colors_and_analyze(url)

        # Log the results found
        if results:
            logging.info("Colors successfully retrieved, processed, and analyzed.")
            return results
        else:
            logging.warning("No results were retrieved, processed, or analyzed.")
            return None
    except Exception as e:
        logging.error(f"Error during scraping and preprocessing: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://www.defprojetos.com/"
    results = scrape_website(url)
    if results:
        print("Scraped Colors:", results['scraped_colors'])
        print("Scraped FONTS", results['scraped_fonts'])
        print("Processed Colors:", results['processed_colors'])
        print("ChatGPT Analysis:", results['analysis'])
