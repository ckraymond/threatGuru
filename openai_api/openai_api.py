import openai           # Needed to support the call for OpenAI API
import numpy as np
import os
import tiktoken

class openAIAPI:
    '''
    Wrapper class for all Open AI API calls to ChatGPT
    '''

    def __init__(self, model = 'gpt-4o-mini', temp = 0):
        self.model = model
        self.temp = temp

    def create_art_query(self, art_content):
        '''
        This function is intended to be uses to summarize each internet article.
        :param art_content:
        :return:
        '''
        messages = []
        messages.append({"role": "system", "content": """Response should be in text format."""})
        messages.append({"role": "user", "content": """Create a summary of the article below for someone who is
         interested in cyber threats and activities. Ensure that you are only using what is in the article and be sure
         to include key facts and figures such as CVNs, names, locates, and dates."""})
        messages.append({"role": "user", "content": """The following lines contain the internet article you will be 
        summarizing. It is in HTML format."""})
        messages.append({"role": "user", "content": str(art_content)})

        return messages

    def create_query(self, web_content):
        # Strip out the content
        temp_web_content = np.array([])
        for item in web_content:
            temp_item = {
                'url': item['url'],
                'summary': item['summary']
            }
            temp_web_content = np.append(temp_web_content, temp_item)

        web_content_string = np.array2string(temp_web_content)
        messages = []
        messages.append({"role": "system", "content": """Response should be in html format with 
        stylistic functions to make it appear pleasant."""})
        messages.append({"role": "user", "content": """Build an HTML formatted report that outlines the emerging cyber 
        threats that a multi-national defense and aerospace company should be aware of. The report should be no more 
        than two pages and contain and overview section and top five issues. Ensure that you provide citations for 
        any assertions you make in the document."""})
        messages.append({"role": "user", "content": """The following lines contain information scraped from the web in 
        the past day. It is formatted with two fields: url and content. Url contains the source url for the information 
        and content contains the actual information from the website. Your report should be pulling information from
        these sources exlusively."""})
        messages.append({"role": "user", "content": web_content_string})

        return messages

    def get_art_summary(self, article):
        '''
        Inputs article and returns tuble with url and summary.
        :param article:
        :return:
        '''

        client = openai.OpenAI()

        request = self.create_art_query(article['content'])

        # Checks the size of the request
        num_tokens = self.calc_tokens(request)
        print(f'Number of tokens: {num_tokens}')

        completion = client.chat.completions.create(
            model=self.model,
            temperature=self.temp,
            messages=request
        )

        article['summary'] = completion.choices[0].message.content
        return article

    def get_report(self, web_content):
        '''
        With information already loaded into the messages list we can now run the query to ChatGPT
        :return:
        '''

        client = openai.OpenAI()

        request = self.create_query(web_content)
        num_tokens = self.calc_tokens(request)
        print(f'Number of tokens: {num_tokens}')

        completion = client.chat.completions.create(
            model=self.model,
            temperature=self.temp,
            messages=request
        )

        return completion.choices[0].message.content

    def calc_tokens(self, request):
        enc = tiktoken.encoding_for_model(self.model)
        num_tokens = len(enc.encode(str(request)))

        return num_tokens