import schedule
import time
from tweet.scraper import TweetScraper

class TweetScheduler:
    
    def __init__(self, scraper):
        self.scraper = scraper
            
    def schedule_scraping(self, every_minutes, limit, batch_size):   
        schedule.every(int(every_minutes)).minutes.do(
            lambda: TweetScraper(self.scraper).scrape_all_politicians_tweets(limit, batch_size)
        )
        
        # Start job immaditealy and then every [every_minutes] minutes
        TweetScraper(self.scraper).scrape_all_politicians_tweets(limit, batch_size)

        while True:
            schedule.run_pending()
            time.sleep(1)