import sys
from twitter.util import init_session
from twitter.scraper import Scraper
from tweetExtractor import getPoliticiansTweets
from userExtractor import updateAndGetPoliticians

if len(sys.argv) < 4:
    print("Incorrect invocation. Usage: python main.py [twitter_email] [twitter_username] [twitter_password]")
    exit(0)

scraper = Scraper(session=init_session(), save=False)
politicians = updateAndGetPoliticians(scraper)
succeded = getPoliticiansTweets(scraper, politicians)
infoMessage = "Scraping finished successfully" if succeded else "Failed to scrape all politicians due to the rate limit being reached."
print(infoMessage)



