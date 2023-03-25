# sentiment-analysis-stock-trader

## Prerequisites
All code was written in Python 3.7.9. Please see <a href="https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/requirements.txt">requirements.txt</a> for dependencies.
```
beautifulsoup4==4.12.0
pandas==1.2.3
praw==7.7.0
requests==2.28.1
snscrape==0.3.4
tqdm==4.56.2
numpy==1.24.2
scikit-learn==1.2.2
torch==2.0.0+cu117
torchaudio==2.0.1+cu117
torchvision==0.15.1+cu117
transformers==4.27.3
```

## Description of Files
### <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/create_dataset.py">create_dataset.py</a>
This file calls functions defined in the other files to create a dataset (this is not the final dataset that we will be using for sentiment analysis, just a preliminary proof of concept).

### <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/dataset.csv">dataset.csv</a>
This is the example dataset created using create_dataset.py.

### <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/finbert.py">finbert.py</a>
This file uses the pretrained FinBERT model on the example dataseet.

### <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/scrape_headlines.py">scrape_headlines.py</a>
This file contains functions to scrape S and P 500 stock tickers and names from Wikipedia, scrape news headlines for any S and P 500 stock from Yahoo Finance, and scrape news headlines for any S and P 500 stock from MarketWatch.

### <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/scrape_reddit.py">scrape_reddit.py</a>
This file contains functions to scrape titles and top comments of top posts from a specified subreddit on Reddit. Note that it requires you to have a file called info.txt saved in the same directory, with the first line of this file being your Reddit API client ID, the second line being your Reddit API client secret, and the third and final line of this file being your Reddit API user agent. 

## License
This project is licensed under the MIT License - see the <a href = "https://github.com/Chubbyman2/sentiment-analysis-stock-trader/blob/main/LICENSE">LICENSE</a> file for details. 
