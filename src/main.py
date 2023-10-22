import sys
from twitter.util import init_session
from twitter.scraper import Scraper
from tweetExtractor import getPoliticiansTweets
from userExtractor import updateAndGetPoliticians

scraper = None

if len(sys.argv) < 2:
    print("Please provide a command scraper type - `python main.py guest` or `python main.py account`")
    exit()

if sys.argv[1] == "guest":
    scraper = Scraper(session=init_session(), save=False)
else:
    if len(sys.argv) < 5:
        print("Incorrect invocation. Usage: python main.py account [twitter_email] [twitter_username] [twitter_password]")
        exit()
    scraper = Scraper(sys.argv[2], sys.argv[3], sys.argv[4], save=False)

politicians = updateAndGetPoliticians(scraper)
succeded = getPoliticiansTweets(scraper, politicians)
infoMessage = "Scraping finished successfully" if succeded else "Failed to scrape all politicians due to the rate limit being reached."
print(infoMessage)



