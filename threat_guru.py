'''
This is a proof of concept around multi-layer AI enabled threat management. Overall process is:
1.) User activates the script.
2.) Script then goes through and conducts a targetted search on Google.
3.) Google information is fed to OpenAI ChatGPT 4o
4.) Information is then sent to Google Gemnini for adversarial review.
5.) Output is presented to user.
'''

from guru_log import gurulog
from news_search.news_search import newsSearch
from web_scrape.web_scrape import webScrape
from openai_api.openai_api import openAIAPI

import pprint
import numpy as np

class threatGuru:
    def __init__(self):
        # gurulog.info('Conducting news search to get URLs')
        #
        # news_api = newsSearch()
        # self.url_list = news_api.get_urls('new vulnerability')
        #
        # gurulog.info('Scrapping websites')
        # scraper = webScrape()
        # web_content = scraper.scrape_url_list(self.url_list)
        #
        # # TODO: Need to filter out those sites that block robots. Can do this through looking at content and 403 forbidden
        # web_content = self.filter_results(web_content)
        #
        # np.save('content.npy', web_content)
        #
        # web_content = np.load('content.npy', allow_pickle=True)
        # # print(len(web_content))
        # web_content = self.filter_results(web_content)
        #
        # #TODO: Add in a section summarizing each article.
        chat_gpt = openAIAPI()
        #
        # for article in web_content:
        #     article = chat_gpt.get_art_summary(article)
        #
        # np.save('content_summ.npy', web_content)

        web_content = np.load('content_summ.npy', allow_pickle=True)

        # web_content = np.load('content_summ.npy', allow_pickle=True)
        # self.print_content(web_content)

        # # Create OpenAI Query
        openai_report = chat_gpt.get_report(web_content)

        # Save information into an HTML file
        with open('test_report.html', 'w') as save_file:
            save_file.write(openai_report)
        #
        # pprint.pprint(openai_report)

    def filter_results(self, web_content):
        '''
        Takes the test content and reviews to see if we can remove those sites that are blocked
        :param test_content:
        :return: test_content:
        '''

        #TODO: There is a better way to do this. To lazy to do it.
        for arr_place in range(len(web_content)-1, -1, -1):
            line = str(web_content[arr_place]['content']).lower()
            index = line.find("403 forbidden")
            if index >= 0:
                web_content = np.delete(web_content, arr_place)

        #TODO: Look at filtering to remove extra whitespace and the like
        return web_content

    def print_content(self, content):
        for article in content:
            print(f'{article['url'][:10]} | {article['content'][:10]} | {article['summary']}')

main_loop = threatGuru()

