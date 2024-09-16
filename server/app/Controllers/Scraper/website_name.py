from bs4 import BeautifulSoup

def get_website_name(soup, url):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()

    meta_name = soup.find('meta', attrs={'name': 'og:site_name'})
    if meta_name:
        return meta_name['content'].strip()

    return url
