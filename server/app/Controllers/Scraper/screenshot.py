import pyppeteer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def take_screenshot(url, path='screenshot.png'):
    logging.info(f"Taking screenshot of URL: {url}")
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot({'path': path, 'fullPage': True})
    await browser.close()
    logging.info(f"Screenshot saved to {path}")
    return path
