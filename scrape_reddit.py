import praw
from scrape_headlines import get_tickers
from datetime import datetime
with open("info.txt") as f:
    lines = f.readlines()
    CLIENT_ID = lines[0][:-1]
    CLIENT_SECRET = lines[1][:-1]
    USER_AGENT = lines[2]
reddit = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT
)

def get_titles(subreddit, num_posts):
    titles = []
    tickers = get_tickers("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    for post in reddit.subreddit(subreddit).hot(limit = num_posts):
        for ticker in list(tickers.keys()):
            if (tickers[ticker] in post.title or tickers[ticker].lower() in post.title) and post.title not in titles:
                titles.append(post.title)
    return titles

def get_titles_and_comments(subreddit, num_posts, max_comments_per_post):
    titles = []
    comments = []
    tickers = get_tickers("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    for post in reddit.subreddit(subreddit).hot(limit = num_posts):
        for ticker in list(tickers.keys()):
            if tickers[ticker] in post.title or tickers[ticker].lower() in post.title and post.title not in [i[1] for i in titles]:
                #titles.append(post.title)
                titles.append((ticker, post.title, str(datetime.fromtimestamp(post.created_utc)), post.url))
                post.comments.replace_more(limit = 0)
                for i in range(len(post.comments)):
                    if i > max_comments_per_post:
                        break
                    #comments.append((ticker, post.comments[i].body, post.comments[i].created_utc))
                    comments.append((ticker, post.comments[i].body, str(datetime.fromtimestamp(post.comments[i].created_utc)), post.url)) # keep track of the ticker corresponding to the comment, because 
                                                                     # the comment won't necessarily mention it, unlike the title
                                                                     # also, rn didn't consider comment threads (replies to comments) but 
                                                                     # could possibly do that too
                                                                     # also, didn't clean up the comments like remove new lines and stuff like
                                                                     # that, will do that in the actual sentiment analysis part 
    return titles, comments

if __name__ == "__main__":
    #titles = get_titles("stocks", 50)
    titles, comments = get_titles_and_comments("stocks", 50, 10)
    print (titles)
    print (comments)