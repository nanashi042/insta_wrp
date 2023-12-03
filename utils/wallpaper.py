import requests
from bs4 import BeautifulSoup
import random
import  re
class Wallpaper:
    def __init__(self):
        self.session = requests.Session()
        self.wallpapers = []

    def wallpaper_urls(self):
        page_number = 1

        while True:
            response = self.session.get(f"https://www.peakpx.com/en/search?q=anime&page={page_number}")
            soup = BeautifulSoup(response.content, 'html.parser')

            for image in soup.find_all('img'):
                srcset = image.get('data-srcset')
                self.wallpapers.append(srcset)

            next_page_link = soup.find('a', class_='next-page')

            if not next_page_link:
                break

            page_number += 1

        return self.wallpapers

    def extract_links(self):
        wallpapers = self.wallpaper_urls()
        links = []

        pattern = r"(https?:\/\/[^\s]+)\.jpg"

        for link in wallpapers:
            matches = re.findall(pattern, str(link))
            if matches:
                links.append(matches)
        ran_first = random.randint(0,len(links))
        return links[ran_first][1]

