import requests

from bs4 import BeautifulSoup

import time 

from urllib.parse import urljoin


class WebCrawer:
    
    def __init__(self, base_urls):
        self.base_urls= base_urls
        self.visted_urls = set()

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'Failed to fetch Page')
            return None

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_urls,href)
            links.add(full_url)
        return links
    def crawl (self, url, depth=1):
        if depth <= 0 or url in self.visted_urls:
            return


        print(f"crawling {url}")
        self.visted_urls.add(url)
        html = self.fetch_page(url)

        if html is None:
            return

        links = self.parse_links(html)
        for link in links:
            self.crawl(link, depth - 1)
            time.sleep(1)

if __name__ == "__main__":
    base_urls="https://www.google.com"
    crawler = WebCrawer(base_urls)
    crawler.crawl(base_urls,depth=2)

