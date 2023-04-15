import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import praw
from datetime import datetime
from scrape_headlines import get_tickers
from scrape_headlines import get_headlines_marketwatch
from scrape_reddit import get_titles_and_comments
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
labels = {0:'hold', 1:'buy',2:'sell'}

df = pd.read_csv('dataset.csv')
for x in df['Text']:   # need to add corresponding url to the dataset
    inputs = tokenizer(x, return_tensors="pt", padding=True)
    outputs = finbert(**inputs)[0]
    val = labels[np.argmax(outputs.detach().numpy())]
    print (x)
    print (val)
    print ("")
    import time
    time.sleep(2)