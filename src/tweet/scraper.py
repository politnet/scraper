import math

from globals import get_logger
from twitter.scraper import Scraper
from tweet.utils import TweetUtils
from user.utils import PoliticianUtils
from tweet.extractor import TweetExtractor

class TweetScraper:
    logger = get_logger(__name__)
    
    def __init__(self, scraper : Scraper):
        self.scraper = scraper      
        
    def __scrape_tweets(self, politicians : dict, limit): 
        politicians_account_names = [politician['user_account_name'] for politician in politicians]
        TweetScraper.logger.info(f"Scraping tweets for {politicians_account_names} with limit of {limit} tweets...")
        
        try:
            politicians_ids = [politician['user_id'] for politician in politicians]
            raw_tweets_data = self.scraper.tweets(politicians_ids, limit=limit) 
            return TweetExtractor.extract_tweets(raw_tweets_data)
        except AttributeError:
            TweetScraper.logger.debug(f"Failed to scrape tweets for {politicians_account_names}. Rate limit exceeded.")
            return None
        
    def __split_tweets_by_politician(politicians : list, tweets : list):
        tweets_by_politician = {}
        for politician in politicians:
            tweets_by_politician[politician['user_account_name']] = [tweet for tweet in tweets if tweet['timeline_owner']['user_id'] == politician['user_id']]
            
        return tweets_by_politician
    
    def __combine_and_save_tweets(politician : dict, scraped_tweets : list):
        saved_tweets = TweetUtils.read_tweets(politician)
        combined_tweets = TweetUtils.combine_tweets(saved_tweets, scraped_tweets)
        TweetUtils.save_tweets(politician, combined_tweets)
        PoliticianUtils.set_politician_last_updated_to_now(politician)
        PoliticianUtils.save_politician(politician)  
        TweetScraper.logger.info(f"Saved {len(combined_tweets) - len(saved_tweets)} new tweets for {politician['user_account_name']}")
        
    def __scrape_politicians_tweets(self, politicians : dict, limit : int):
        scraped_tweets = self.__scrape_tweets(politicians, limit)
        if scraped_tweets is None:
            return False
        
        tweets_by_politician = TweetScraper.__split_tweets_by_politician(politicians, scraped_tweets)
        for account_name, tweets in tweets_by_politician.items():
            politician = next((politician for politician in politicians if politician['user_account_name'] == account_name))
            TweetScraper.__combine_and_save_tweets(politician, tweets)
        
        return True
  
    def scrape_all_politicians_tweets(self, limit : int, batch_size : int = 1): 
        sorted_politicians = PoliticianUtils.sort_by_last_modified(PoliticianUtils.read_politicians())
        
        for i in range(0, len(sorted_politicians), batch_size):
            politician_batch = sorted_politicians[i:i + batch_size]
            if not self.__scrape_politicians_tweets(politician_batch, limit):
                return False
            
        return True
              
    def scrape_politician_tweets_by_account_name(self, account_name : str, limit : int):
        politician = PoliticianUtils.read_politcian_by_account_name(account_name)
        return self.__scrape_politicians_tweets([politician], limit)