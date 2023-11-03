from twitter.scraper import Scraper
from tweet.extractor import TweetExtractor

class TweetScraper:
    
    def __init__(self, scraper: Scraper):
        self.scraper = scraper
    
    def extract_tweets(raw_tweets_data : dict):
        tweets = []
        for raw_tweet_data in raw_tweets_data:
            tweets += TweetExtractor.extract_tweets(raw_tweet_data)
        return tweets
    
    def scrape_tweets(self, politicians : list):
        politicians_ids = [politician['user_id'] for politician in politicians]
        try:
            raw_tweets_data = self.scraper.tweets(politicians_ids) 
            return TweetScraper.extract_tweets(raw_tweets_data)
        except AttributeError:
            print(f"Failed to scrape tweets for {politicians_ids}. Rate limit exceeded.")
            return None
        
    def scrape_tweets_with_limit(self, politicians : list, limit : int):
        politicians_ids = [politician['user_id'] for politician in politicians]
        try:
            raw_tweets_data = self.scraper.tweets(politicians_ids, limit=limit)
            return TweetScraper.extract_tweets(raw_tweets_data)
        except AttributeError:
            print(f"Failed to scrape tweets for {politicians_ids} with limit of {limit} tweets. Rate limit exceeded.")
            return None