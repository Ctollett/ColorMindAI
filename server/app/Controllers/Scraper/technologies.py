from bs4 import BeautifulSoup
import re

def identify_technologies(soup):
    technologies = set()
    if soup.find('script', src=re.compile(r'react', re.IGNORECASE)):
        technologies.add('React')
    if soup.find('script', src=re.compile(r'jquery', re.IGNORECASE)):
        technologies.add('jQuery')
    if soup.find('link', href=re.compile(r'bootstrap', re.IGNORECASE)):
        technologies.add('Bootstrap')
    if soup.find('script', src=re.compile(r'angular', re.IGNORECASE)):
        technologies.add('Angular')
    if soup.find('script', src=re.compile(r'vue', re.IGNORECASE)) or \
       soup.find('script', text=re.compile(r'Vue\.config', re.IGNORECASE)):
        technologies.add('Vue.js')
    if soup.find('meta', {'content': re.compile(r'wordpress', re.IGNORECASE)}) or \
       soup.find('meta', {'name': re.compile(r'generator', re.IGNORECASE), 'content': re.compile(r'WordPress', re.IGNORECASE)}):
        technologies.add('WordPress')
    if soup.find('script', src=re.compile(r'django', re.IGNORECASE)):
        technologies.add('Django')
    if soup.find('script', src=re.compile(r'flask', re.IGNORECASE)):
        technologies.add('Flask')
    if soup.find('meta', {'content': re.compile(r'rails', re.IGNORECASE)}):
        technologies.add('Ruby on Rails')
    return technologies
