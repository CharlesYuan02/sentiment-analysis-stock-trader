'''
import requests
from bs4 import BeautifulSoup
url = 'https://finance.yahoo.com/quote/MMM/news?p=MMM'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
urls = []
for link in soup.find_all('a'):
    print (link.get('href'))
'''
import bs4 as BeautifulSoup
from bs4 import SoupStrainer
import re
import urllib.request
import pandas as pd
import requests
headers = {'User-agent': 'Mozilla/5.0'}
#url = ("https://finance.yahoo.com/quote/{}/profile?p={}".format('MMM','MMM'))
url = ("https://finance.yahoo.com/quote/{}/news?p={}".format('MMM','MMM'))
print (url)
webpage = requests.get(url, headers=headers)
soup = BeautifulSoup.BeautifulSoup(webpage.content)
for link in soup.find_all('a', href=True):
    print (link)