'''


Keyword Sentiment Analysis



'''

import pandas as pd
import config
from newsapi import NewsApiClient
from newspaper import Article
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

'''
    Function: 
        download_fulltext
    
    Arguments:
        url (string)    
    
    Description:
        Returns the text of an article using the newspaper3k API.
'''

def download_fulltext(url):
    print('Downloading article from '+url)
    try:
        article = Article(url)
        article.download()
        article.parse()
        fulltext = article.text
    except:
        fulltext = 'Full Text Download Failed'
    return fulltext




'''
    Function: 
        get_bias
    
    Arguments:
        source_id (string)
    
    Description:
        Returns the category or bias of the news source
'''

def get_bias(source_id):
    bias = {
        'skew-left':['cbs-news','cnn','msnbc','nbc-news','newsweek','new-york-magazine','the-new-york-times','the-washington-post','vice-news'],
        'skew-right':['breitbart-news','fox-news','national-review'],
        'neutral':['associated-press','axios','politico','reuters','the-economist','the-hill','time','usa-today'],
        'tech':['ars-technica','engadget','recode','techcrunch','techradar','the-verge','wired'],
        'business':['bloomberg','business-insider','cnbc','financial-times','fortune','the-wall-street-journal'],
        'gaming':['ign','polygon'],
        'world':['al-jazeera-english','bbc-news','the-telegraph'],
        'aggregates':['google-news','reddit-r-all']       
    }
    
    for category, source_array in bias.items():
        for source in source_array:
            if (source_id == source):
                print(source_id + ' bias identified as ' + category)
                return category
        
    return "N/A"



def get_google_sentiment_score(contents):
    client = language.LanguageServiceClient.from_service_account_json(
        config.GOOGLE_SENTIMENT_ANALYSIS_CREDENTIAL_PATH)
    document = types\
               .Document(content=contents,
                         type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score           
    return sentiment_score


def get_sentiment(df):
    sentiment = {'index':[], 'sentiment':[]} 
    for index, entry in df.iterrows():
         s = get_google_sentiment_score(entry.fulltext)
         print(index, s)
         sentiment['index'].append(index)
         sentiment['sentiment'].append(s)

    sentdf = pd.DataFrame(sentiment)
    newdf = df.copy()
    newdf['sentiment'] = sentdf['sentiment']
    
    return newdf






'''
    Function: 
        get_news
    
    Arguments:
        search_term (string)
        considered_sources (list of strings)     
    
    Description:
        Collects all articles (from the NewsAPI (https://newsapi.org) regarding the
        search term from the list of considered news sources.
        The data for each article contains: news source (id/name), author, title,
        url, publish datetime, and description.
        The NewsAPI does not provide the full text of the article (the 'content' 
        only contains the first ~200 characters), so to gather the full text of 
        the article, the url is passed to download_fulltext(url (string)), which
        returns the entire text from the article url. Returns a Pandas Dataframe
        containing the details and content of articles relating to the search term.
         
'''

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
            d['publication_bias'].append(get_bias(sourcepkg['id']))
            d['title'].append(a['title'])
            d['url'].append(a['url'])
            d['description'].append(a['description'])
            d['publishedAt'].append(a['publishedAt'])
            d['content'].append(a['content'])
            d['fulltext'].append(download_fulltext(a['url']))
        
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
    
    df = get_news(searchterm, consideredsources)
    print(df)
    
    
    

if __name__ == "__main__":
    main()