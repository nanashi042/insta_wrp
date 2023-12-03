import requests
from bs4 import BeautifulSoup
import random
import re

class Wallpaper:
    def __init__(self):
        self.wallpapers = []

    def wallpaper_urls(self):
        page_number = 1

        while True:
            try:
                with open(f"templates/file{page_number}.html", 'r', encoding='utf-8') as html_file:
                    response = html_file.read()
                    print(response)
            except FileNotFoundError:
                break

            soup = BeautifulSoup(response, 'html.parser')

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
                links.extend(matches)

        if links:
            ran_first = random.randint(0, len(links) - 1)
            return links[ran_first]
        else:
            return None

# Example usage:
wallpaper_obj = Wallpaper()
selected_link = wallpaper_obj.extract_links()
print(selected_link)
