import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime
from scrape_headlines import get_tickers
from scrape_headlines import get_headlines_marketwatch
from scrape_reddit import get_titles_and_comments


tickers = get_tickers('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
marketwatch_data = []
for ticker in tqdm(list(tickers.keys())):
    marketwatch_data += get_headlines_marketwatch(ticker, tickers[ticker])
print (marketwatch_data)

reddit_data = []
reddit_titles, reddit_comments = get_titles_and_comments("stocks", 50, 10)
reddit_data = reddit_titles + reddit_comments
print (reddit_data)

dataset = marketwatch_data + reddit_data
column_names = ['Ticker', 'Text', 'Date']
df = pd.DataFrame(dataset, columns = column_names)
df.to_csv('dataset.csv')
# for now just going to use marketwatch and reddit
# fix yahoo finance later
# do i have to deal with the possibility of multiple stocks
# being in the same headline?