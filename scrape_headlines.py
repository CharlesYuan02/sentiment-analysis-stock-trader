'''
in this file, we will scrape https://en.wikipedia.org/wiki/List_of_S%26P_500_companies to get the tickers for S and P 500 stocks
following this: https://medium.com/analytics-vidhya/scraping-s-p-500-index-and-extracting-stock-market-data-from-yahoo-finance-api-72218eeed1be


https://www.octoparse.com/blog/how-to-scrape-yahoo-finance#:~:text=Scrape%20Yahoo%20Finance%20Data%20Using%20Python,-To%20web%20scrape&text=Step%201%3A%20Install%20the%20dependencies%20on%20the%20device%20you%20are%20using.&text=Step%203%3A%20Get%20the%20webpage%20URL%20and%20check%20for%20errors.&text=Step%204%3A%20Create%20a%20function,as%20a%20Beautiful%20Soup%20object.&text=Step%205%3A%20Extract%20and%20store%20the%20information.
'''
import bs4 as bs
import pickle
import requests
from bs4 import BeautifulSoup


def get_tickers(url):
    html = requests.get(url)
    soup = bs.BeautifulSoup(html.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        tickers.append(ticker)
    return tickers

def get_headlines(ticker):
    url = "https://finance.yahoo.com/quote/" + ticker + "/news?p=" + ticker
    print (url)
    response = requests.get(url)
    print (response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3', {'class': 'Mb(5px)'})
    print (len(headlines))
    '''
    page_content = response.text
    #print (page_content)
    doc = BeautifulSoup(page_content, 'html.parser')
    print (doc)
    a_tags = doc.find_all('a', {'class': "js-content-viewer"})
    print (len(a_tags))
    #print (a_tags)
    '''


tickers = get_tickers('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
#print (tickers)
get_headlines(tickers[0])

#url = "https://finance.yahoo.com/topic/stock-market-news"
url = "https://finance.yahoo.com/quote/MMM/news?p=MMM"
response = requests.get(url)
soup = BeautifulSoup(response.text,"lxml")
links = [l.find('a')['href'] for l in soup.find_all('li') if l.find('a')]
print (links)



