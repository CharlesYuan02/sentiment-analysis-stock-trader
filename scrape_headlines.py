'''
https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
https://medium.com/analytics-vidhya/scraping-s-p-500-index-and-extracting-stock-market-data-from-yahoo-finance-api-72218eeed1be
https://www.octoparse.com/blog/how-to-scrape-yahoo-finance#:~:text=Scrape%20Yahoo%20Finance%20Data%20Using%20Python,-To%20web%20scrape&text=Step%201%3A%20Install%20the%20dependencies%20on%20the%20device%20you%20are%20using.&text=Step%203%3A%20Get%20the%20webpage%20URL%20and%20check%20for%20errors.&text=Step%204%3A%20Create%20a%20function,as%20a%20Beautiful%20Soup%20object.&text=Step%205%3A%20Extract%20and%20store%20the%20information.
https://www.cloudquant.com/url2symbol/
'''
import bs4 as bs
import pickle
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_tickers(url):
    html = requests.get(url)
    soup = bs.BeautifulSoup(html.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = {}
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        name = row.findAll('td')[1].text
        tickers[ticker] = name
    return tickers # dictionary with keys tickers, and values the corresponding names

def get_headlines_yahoo(ticker, name):
    headers = {'User-agent': 'Mozilla/5.0'}
    url = ("https://finance.yahoo.com/quote/{}/news?p={}".format(ticker, ticker))     # this should be news not new??
    webpage = requests.get(url, headers = headers)
    soup = bs.BeautifulSoup(webpage.content)
    headlines = []
    for link in soup.find_all('a', href=True):
        if ticker.lower() in link['href'] or name.lower() in link['href']:
            for i in link.find_all('u'):
                headline = ''
                j = str(link).find(str(i)) + len(str(i))
                while str(link)[j] != '<':
                    headline += str(link)[j]
                    j += 1
                headlines.append(headline)
    return headlines

def get_headlines_marketwatch(ticker, name):
    url = 'https://www.marketwatch.com/investing/stock/' + ticker.lower()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []
    for headline in soup.find_all('h3', class_ = 'article__headline'):
        headline_clean = headline.text.strip()
        '''
        for category_name in ['Markets', 'Opinion', 'Technology', 'Companies', 'Transportation', 'Manufacturing', 'Aerospace and Defense']:
            if headline_clean[:len(category_name)] == category_name:
                headline_clean = headline_clean[len(category_name):]
        '''
        if '\n' in headline_clean and '    ' in headline_clean and headline_clean[0] != ' ':
            idx = 0
            while headline_clean[idx] != ' ':
                idx += 1
            headline_clean = headline_clean[idx:]        
            headline_clean = headline_clean.strip()
        if name in headline_clean or name.lower() in headline_clean:
            headlines.append(headline_clean)
    return headlines

if __name__ == "__main__":
    tickers = get_tickers('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    print (tickers)
    all_headlines = []
    for ticker in tqdm(list(tickers.keys())):
        all_headlines += get_headlines_marketwatch(ticker, tickers[ticker])
    print (all_headlines)
    file = open('output2.txt', 'w')
    file.writelines(all_headlines)
    file.close()
    '''
    for ticker in tqdm(list(tickers.keys())):
        all_headlines += get_headlines_yahoo(ticker, tickers[ticker])
    print (all_headlines)
    file = open('output.txt', 'w')
    file.writelines(all_headlines)
    file.close()
    '''

'''
next steps:
also scrape information like the date, and figure out how to get more of the headlines from the same page (like why does it only get the first one)
also look for other sources for news about s and p 500 stocks
also save what stock corresponds to the headline
'''