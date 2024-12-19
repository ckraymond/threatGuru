from guru_log import gurulog
from bs4 import BeautifulSoup as bsp
import requests

class webScrape:

    def __init__(self):
        gurulog.info('Enabling web scraper')
        self.parser = 'html.parser'

    def scrape_url(self, url):
        gurulog.info(f'Scraping: {url}')

        print(url)

        try:
            raw_html = requests.get(url).text
            page_content = bsp(raw_html, self.parser)
            body_content = page_content.getText()
        except:
            body_content = None
            gurulog.error(f'Unable to retrieve URL: {url}')

        return body_content

    def scrape_url_list(self, url_list):
        url_content = []

        for url in url_list:
            content_pair = {
                'url': url,
                'content': self.scrape_url(url)
            }

            url_content.append(content_pair)

        return url_content
