import configparser
import re
from datetime import datetime

import requests

from src.utils import write_to_file, is_in_file


# from pytrends.request import TrendReq

def create_prompt_from_news() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('api', 'key_nyt')
    api_url = f'https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={api_key}'

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        for index, article in enumerate(data['results'], start=1):
            prompt = ''
            prompt_clean = ''
            for key, value in article.items():
                if value is not None and value != '':
                    if key in (  # 'section', 'subsection',
                            'title'#, 'abstract', 'subheadline',
                            #'des_facet', 'geo_facet'
                            ):
                        subprompt = re.sub(r'[^\w\s]', '', f'{value}')  # remove special characters
                        prompt += f'{subprompt}, '
                        # remove duplicate whitespaces and clean commas
                        prompt_clean = re.sub(r'\s*,\s*', ', ', re.sub(r'\s+', ' ',
                                                                       prompt.strip()))
                        prompt_clean = re.sub(r',\s*$', '', prompt_clean)   # remove trailing commas
            if not is_in_file('outpainting', 'prompts.txt', prompt_clean):
                write_to_file('outpainting', 'prompts.txt', f'{prompt_clean}\n', append=True)
                return f'{prompt_clean}'  # return the first new result
    else:
        print(f'Request failed with status code: {response.status_code}')
    return ''


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
