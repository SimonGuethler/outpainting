import configparser
import re
from datetime import datetime

import requests

from src.utils import is_in_file
from newsapi import NewsApiClient

# from pytrends.request import TrendReq


def create_prompt_from_news() -> str:
    # main api
    prompt = call_nyt_api()
    if prompt == '' or prompt == None:
        # backup api
        prompt = call_news_api()
        if prompt == '' or prompt == None:
            return '-'
    return prompt


def call_nyt_api() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('api', 'key_nyt')
    api_url = f'https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={api_key}'

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        for _, article in enumerate(data['results'], start=1):
            for key, value in article.items():
                if value and key == 'title':
                    prompt = clean_prompt(value)

                    # return the first new result
                    if not is_in_file('outpainting', 'prompts.txt', prompt):
                        return f'{prompt}'
    else:
        print(f'Request failed with status code: {response.status_code}')
    return ''


def call_news_api() -> str:
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_key = config.get('api', 'key')

        newsapi = NewsApiClient(api_key=api_key)

        top_headlines = newsapi.get_top_headlines(language='en')

        for article in top_headlines['articles']:
            title = article['title']
            title = title.rpartition(' - ')[0].strip()
            prompt = clean_prompt(title)

            # return the first new result
            if not is_in_file('outpainting', 'prompts.txt', prompt):
                return f'{prompt}'
    except:
        return ''


def clean_prompt(prompt) -> str:
    prompt_clean = re.sub(r'[^a-zA-Z0-9\s]', '', f'{prompt}')  # remove special characters
    prompt_clean = ' '.join(prompt_clean.split())  # remove duplicate white spaces
    # prompt_clean = re.sub(r'\s*,\s*', ', ', prompt_clean)  # create clean commas
    return prompt_clean


def create_prompt_from_history():
    current_month = datetime.now().strftime(f'%m')
    current_day = datetime.now().strftime(f'%d')
    api_url = f'https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/selected/{current_month}/{current_day}'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        text = data["selected"][0]["text"]
        print(text)
        return (text)
    else:
        print(f'Request failed with status code: {response.status_code}')


# def create_prompt_from_trends():
#     pytrends = TrendReq(hl='en-US', tz=360)
#     trending_searches_df = pytrends.trending_searches(pn='germany')
#     most_talked_about_topic = trending_searches_df.iloc[0, 0]
#     print(most_talked_about_topic)
#     return(most_talked_about_topic)
