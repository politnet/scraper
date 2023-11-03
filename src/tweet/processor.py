import globals as gl
from twitter.scraper import Scraper
from tweet.scraper import TweetScraper
from tweet.utils import TweetUtils
from user.utils import PoliticianUtils

class TweetProcessor:
    
    def __init__(self, scraper : Scraper):
        self.tweet_scraper = TweetScraper(scraper)
    
    def __split_tweets_by_politician(politicians, tweets):
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
        print(f"Saved {len(combined_tweets) - len(saved_tweets)} new tweets for {politician['user_account_name']}")
        
    def __get_politician_tweets(self, politicians : dict):
        scraped_tweets = self.tweet_scraper.scrape_tweets(politicians)
        if scraped_tweets is None:
            return False
        
        tweets_by_politician = TweetProcessor.__split_tweets_by_politician(politicians, scraped_tweets)
        for account_name, tweets in tweets_by_politician.items():
            politician = next((politician for politician in politicians if politician['user_account_name'] == account_name))
            TweetProcessor.__combine_and_save_tweets(politician, tweets)
        
        return True
  
    def get_all_politicians_tweets_in_batch(self, limit : int):
        print(f"Getting tweets for all politicians with the limit of {limit} tweets...")
        
        sorted_politicians = PoliticianUtils.sort_by_last_modified(PoliticianUtils.read_politicians())
        
        for i in range(0, len(sorted_politicians), gl.DEFAULT_POLITICIANS_BATCH):
            politician_batch = sorted_politicians[i:i+gl.DEFAULT_POLITICIANS_BATCH]
            scraped_tweets = self.tweet_scraper.scrape_tweets_with_limit(politician_batch, limit)
            if scraped_tweets is None:
                    return False
            
            tweets_by_politician = TweetProcessor.__split_tweets_by_politician(politician_batch, scraped_tweets)
            for account_name, tweets in tweets_by_politician.items():
                politician = next((politician for politician in politician_batch if politician['user_account_name'] == account_name))
                TweetProcessor.__combine_and_save_tweets(politician, tweets)
            
        return True
              
    def get_politician_tweets_by_account_name(self, account_name : str):
        politician = PoliticianUtils.read_politcian_by_account_name(account_name)
        return self.__get_politician_tweets([politician])
    
    def get_all_politicians_tweets(self):
        print(f"Getting tweets for all politicians...")
        
        for politician in PoliticianUtils.read_politicians():
            print(f"Getting tweets for {politician['user_account_name']}...")
            self.__get_politician_tweets([politician])