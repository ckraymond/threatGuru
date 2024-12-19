from newsapi import newsapi_client
from guru_log import gurulog
import os

class newsSearch:

    def __init__(self):
        self.api_key = os.environ['NEWS_API_KEY']

    def get_urls(self, subject):
        newsapi = newsapi_client.NewsApiClient(api_key=self.api_key)
        url_list = []

        gurulog.info(f'Importing news with subject: {subject}')
        all_articles = newsapi.get_everything(q=subject,
                                              from_param='2024-12-16',
                                              to='2024-12-17',
                                              language='en')

        for article in all_articles['articles']:
            url_list.append(article['url'])

        gurulog.info(f'Total articles found: {len(url_list)}')
        return url_list
