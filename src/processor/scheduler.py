import schedule
import time
from tweet.extractor import TweetExtractor

class TweetScheduler:
    
    def __init__(self, scraper):
        self.scraper = scraper
        
    def schedule_scraping(self, every_minutes, limit):
        print(f"Scheduling scraping every {every_minutes} minutes.")
        schedule.every(int(every_minutes)).minutes.do(
            lambda: TweetExtractor(self.scraper).get_all_politicians_tweets(limit)
        )
        
        # Start job immaditealy and then every [every_minutes] minutes
        TweetExtractor(self.scraper).get_all_politicians_tweets(limit)

        while True:
            schedule.run_pending()
            time.sleep(1)