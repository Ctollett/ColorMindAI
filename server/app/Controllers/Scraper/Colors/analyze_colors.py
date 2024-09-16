import openai
import json
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Access the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def format_color_analysis_data(results):
    """Format the processed color data into a prompt for ChatGPT."""
    prompt = (
        "You are a UX/UI expert who is analyzing data from sites. This particular analysis is over the colors utilized from the site. I want you answer this as if you are viewing the color information yourself and provide insights accordingly on the color combinations and design elements. Don't explicitly mention any of the values but simply provide an analysis. Don't number out the contrast score or any of the values, speak naturally and informatively. Start the analysis naturally as if you're beginning a blog or informative article with a brief introduction. Include information about potential design trends that the site is following regarding color:\n\n"
        f"Contrast Score: {results['contrast_ratio']:.2f} (Scale 1-10)\n"
        f"Harmony Score: {results['harmony_score']:.2f} (Scale 1-10)\n\n"
        "Best Color Trait:\n"
        f"{results['best_trait']}\n\n"
        "Normalized Colors (RGB):\n"
        f"{json.dumps(results['normalized_colors'], indent=2)}\n\n"
        "Generated Color Palette:\n"
        f"{json.dumps(results['color_palette'], indent=2)}\n\n"
        "Provide a detailed analysis of the above results, including any insights or recommendations."
    )
    return prompt

def get_chatgpt_analysis(prompt):
    """Send a prompt to ChatGPT and get the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjust as needed
            temperature=0.7  # Adjust for creativity; lower values are more focused
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"Error interacting with ChatGPT: {e}")
        return "Error: Unable to get response from ChatGPT."

def analyze_color_results(results):
    """Analyze color results using ChatGPT."""
    try:
        # Format the data into a prompt for ChatGPT
        prompt = format_color_analysis_data(results)
        logging.info("Sending prompt to ChatGPT...")
        analysis = get_chatgpt_analysis(prompt)
        logging.info("Received analysis from ChatGPT:")
        logging.info(analysis)
        return analysis
    except Exception as e:
        logging.error(f"Error analyzing results: {e}")
        return "Error: Unable to analyze results."

