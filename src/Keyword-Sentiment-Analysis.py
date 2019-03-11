'''


Keyword Sentiment Analysis



'''

import pandas as pd
import config
from newsapi import NewsApiClient


def get_news(search_term, considered_sources):
    newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)
    d = {'id':[], 'name':[],'author':[],'publication_bias':[], 'title':[], 'url':[], 'description':[], 'publishedAt':[], 'content':[], 'fulltext':[]}
    
    for source in considered_sources:
        newspkg = newsapi.get_everything(q=search_term, sources = source)
        articlepkg = newspkg['articles']
        print("Gathering Articles from " + source)
        for a in articlepkg:
            sourcepkg = a['source']
            d['id'].append(sourcepkg['id'])
            d['name'].append(sourcepkg['name'])
            d['author'].append(a['author'])
            d['title'].append(a['title'])
            d['url'].append(a['url'])
            d['description'].append(a['description'])
            d['publishedAt'].append(a['publishedAt'])
            d['content'].append(a['content'])
        
    df = pd.DataFrame.from_dict(d)
    
    return df



def main():
    consideredsources = ['al-jazeera-english', 'ars-technica', 'associated-press', 
                         'axios', 'bbc-news', 'bloomberg', 'breitbart-news', 'business-insider' ,
                         'cbs-news', 'cnbc' ,'cnn', 'engadget','financial-times', 'fortune' ,
                         'fox-news', 'google-news' , 'ign', 'msnbc' , 'national-review' , 'nbc-news',
                         'newsweek', 'new-york-magazine', 'politico', 'polygon' ,'recode','reddit-r-all',
                         'reuters', 'techcrunch', 'techradar', 'the-economist', 'the-hill', 
                         'the-new-york-times', 'the-telegraph', 'the-verge', 'the-wall-street-journal',
                         'the-washington-post', 'time', 'usa-today', 'vice-news', 'wired']
    
    searchterm = 'Larry Ellison'
    
    df = get_news(searchterm,consideredsources)
    print(df)