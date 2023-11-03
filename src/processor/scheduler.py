import schedule
import time
from tweet.processor import TweetProcessor

class TweetScheduler:
    
    def __init__(self, scraper):
        self.scraper = scraper
        
    def schedule_scraping(self, every_minutes):
        print(f"Scheduling scraping every {every_minutes} minutes.")
        
        schedule.every(int(every_minutes)).minutes.do(
            lambda: TweetProcessor(self.scraper).get_all_politicians_tweets()
        )
        
        # Start job immaditealy and then every [every_minutes] minutes
        TweetProcessor(self.scraper).get_all_politicians_tweets()

        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def schedule_scraping(self, every_minutes, limit):
        print(f"Scheduling scraping every {every_minutes} minutes with limit of {limit} tweets.")
        
        schedule.every(int(every_minutes)).minutes.do(
            lambda: TweetProcessor(self.scraper).get_all_politicians_tweets_in_batch(limit)
        )
        
        # Start job immaditealy and then every [every_minutes] minutes
        TweetProcessor(self.scraper).get_all_politicians_tweets_in_batch(limit)

        while True:
            schedule.run_pending()
            time.sleep(1)