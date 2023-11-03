from json import JSONDecodeError
from twitter.scraper import Scraper
from tweet.extractor import TweetExtractor

class TweetScraper:
    
    def __init__(self, scraper: Scraper):
        self.scraper = scraper
    
    def scrape_tweets(self, politician):
        try:
            raw_tweets_data = self.scraper.tweets([politician['user_id']])
            tweets = []
            for raw_tweet_data in raw_tweets_data:
                tweets += TweetExtractor.extract_tweets(raw_tweet_data)
            return tweets
        except JSONDecodeError:
            print(f"Failed to scrape tweets for {politician['user_account_name']}. Rate limit exceeded.")
            return None