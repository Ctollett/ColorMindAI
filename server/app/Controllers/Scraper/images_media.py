import re
import requests
from bs4 import BeautifulSoup

def extract_images(soup, base_url):
    images = set()
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and not img_url.startswith('data:'):
            if not img_url.startswith('http'):
                img_url = requests.compat.urljoin(base_url, img_url)
            images.add(img_url)
    return images

def extract_videos(soup, base_url):
    videos = set()
    for video in soup.find_all('video'):
        video_url = video.get('src')
        if video_url:
            if not video_url.startswith('http'):
                video_url = requests.compat.urljoin(base_url, video_url)
            videos.add(video_url)
    return videos

def identify_hero_image(soup, base_url):
    hero_selectors = [
        'header img',
        'img.hero',
        'img.banner',
        'div.hero img',
        'div.banner img'
    ]
    
    for selector in hero_selectors:
        hero_img = soup.select_one(selector)
        if hero_img:
            hero_src = hero_img.get('src')
            if hero_src:
                if not hero_src.startswith('http'):
                    hero_src = requests.compat.urljoin(base_url, hero_src)
                return hero_src
    return None
