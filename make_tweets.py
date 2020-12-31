import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from random import random, randint


twitter_hashes = {
    'data-engineering': '#Data',
    'data-science': '#DataScience',
    'aws': '#AWS',
    'analytics': '#Analytics',
    'data': '#Data'
}

nice_words = ['Fantastic article', 'Great piece', 'Wonderful article', 'Insightful piece', 'Helpful content',
              'Useful article', 'Nice piece of work', 'Spectacular piece', 'Recommended article', 
              'Trending piece', 'Popular piece', 'Really good work',
              'Great content', 'Superb article', 'Brilliant piece', 'Amazing piece of work',
              'Awesome content', 'Enjoyable piece', 'Terrific piece', 'Smart article']


def get_articles(tag, num_articles=5):
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y/%m/%d')
    url = f'https://medium.com/tag/{tag}/archive/{yesterday}'
    r = requests.get(url)
    asoup = BeautifulSoup(r.text, 'html.parser')
    
    datas = []
    
    articles = asoup.find_all('div', class_='streamItem')
    
    if not articles:
        print(f'No articles found today for tag: {tag}')
        return
    
    for i,art in enumerate(articles[:num_articles]):
        
        print(f'Working on article {i+1}')
        
        dat = {}
        
        sleep(random())
        
        article_url = art.find('a', class_='').get('href').split('?')[0]
        # article_title = art.find('h3', {'name': 'previewTitle'}).text
        article_title = art.find('h3', class_='graf--title').text
        
        try:
            num_claps = int(art.find('button', class_='js-multirecommendCountButton').text)
        except:
            num_claps = 0
            
        author_block = art.find_all('a', class_='ds-link')
        print(f'author block length is: {len(author_block)}')
        
        author_name = author_block[0].text
        author_url = author_block[0].get('href').split('?')[0] + '/about'
        
        if len(author_block) == 2:
        
            publication = author_block[1].text
            
        elif len(author_block) == 1:
            
            publication = None
            
        else:
            print(f'Weird Number of blocks in author!!! (val: {len(author_block)})')
            # author_url = ''
            continue
            
            
        if author_url:
            sleep(random())

            ar = requests.get(author_url)
            ausoup = BeautifulSoup(ar.text, 'html.parser')

            twitter = ausoup.select("a[href*=twitter]")

            if twitter:
                handle = '@' + str(twitter[0].get('href')).split('/')[-1]
            else:
                handle = None
                
        dat['article_url'] = article_url
        dat['article_title'] = article_title
        dat['num_claps'] = num_claps
        dat['author_name'] = author_name
        dat['publication'] = publication
        dat['handle'] = handle
        
        datas.append(dat)
        
    return datas

def generate_tweets(articles, tag):

    

    for art in articles:

        nice_word = nice_words[randint(0, len(nice_words)-1)]

        if art['handle'] and art['publication']:
            print(f"\n{nice_word} by {art['handle']} {art['article_title']}  in {art['publication']} {twitter_hashes[tag]} {art['article_url']}")
        elif art['handle']:
            print(f"\n{nice_word} titled {art['article_title']} by {art['handle']} {twitter_hashes[tag]} {art['article_url']}")
        elif art['publication']:
            print(f"\n{nice_word} by {art['author_name']} in {art['publication']}: {art['article_title']} {twitter_hashes[tag]} {art['article_url']}")
        else:
            print(f"\n{nice_word} by {art['author_name']} titled: {art['article_title']}  {twitter_hashes[tag]} {art['article_url']}")


if __name__=='__main__':

    aparser = argparse.ArgumentParser()
    aparser.add_argument("-t", "--tag", required=False, default='all')
    
    args = aparser.parse_args()
    tag = args.tag

    if tag == 'all':

        tags = ['data-engineering', 'data-science', 'aws', 'analytics', 'data']

    else:
        tags = [tag]
    

    for tag in tags:

        print(f'\nFinding tweets for tag: {tag}\n')

        sleep(3)

        articles = get_articles(tag)

        generate_tweets(articles, tag)

