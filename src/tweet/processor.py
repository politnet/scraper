from twitter.scraper import Scraper
from tweet.scraper import TweetScraper
from tweet.utils import TweetUtils
from user.utils import PoliticianUtils

class TweetProcessor:
    
    def __init__(self, scraper : Scraper):
        self.tweet_scraper = TweetScraper(scraper)
        
    def get_politician_tweets(self, politician : dict):
        print(f"Getting tweets for {politician['user_account_name']}...")
            
        scraped_tweets = self.tweet_scraper.scrape_tweets(politician)
        if scraped_tweets is None:
            return False
        
        saved_tweets = TweetUtils.read_tweets(politician)
        combined_tweets = TweetUtils.combine_tweets(saved_tweets, scraped_tweets)
        TweetUtils.save_tweets(politician, combined_tweets)
        PoliticianUtils.set_politician_last_updated_to_now(politician)
        PoliticianUtils.save_politician(politician)
        
        print(f"Saved {len(combined_tweets) - len(saved_tweets)} new tweets for {politician['user_account_name']}")
        return True
    
    def get_politician_tweets_by_account_name(self, account_name : str):
        politician = PoliticianUtils.read_politcian_by_account_name(account_name)
        return self.get_politician_tweets(politician)
    
    def get_politicians_tweets(self):
        print(f"Getting tweets for account_name...")
        
        for politician in PoliticianUtils.read_politicians():
            self.get_politician_tweets(politician)