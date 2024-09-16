from server.app.Controllers.Scraper.scraper import scrape_website
from analysis import analyze_design, classify_fonts_with_openai

def main(url):
    # Step 1: Scrape the website
    website_name, all_fonts, heading_fonts, subheading_fonts, paragraph_fonts, colors, technologies, logo_url = scrape_website(url)
    
    # Step 2: Analyze the design using GPT
    design_analysis = analyze_design(all_fonts, colors)
    
    # Output results
    print(f"Website Name: {website_name}")
    print(f"Heading Fonts: {heading_fonts}")
    print(f"Subheading Fonts: {subheading_fonts}")
    print(f"Paragraph Fonts: {paragraph_fonts}")
    print(f"Colors: {colors}")
    print(f"Technologies: {technologies}")
    print(f"Logo URL: {logo_url}")
    print(f"Design Analysis: {design_analysis}")

if __name__ == "__main__":
    url = "https://example.com"
    main(url)
