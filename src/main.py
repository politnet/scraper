import sys
from twitter.scraper import Scraper
from tweetExtractor import getPoliticiansTweets
from userExtractor import updateAndGetPoliticians

if len(sys.argv) < 4:
    print("Incorrect invocation. Usage: python main.py [twitter_email] [twitter_username] [twitter_password]")
    exit(0)
    
TWITTER_EMAIL = sys.argv[1]
TWITTER_USERNAME = sys.argv[2]
TWITTER_PASSWORD = sys.argv[3]
DATA_DIRECTORY = "data"
POLITICIANS_FILE = F"{DATA_DIRECTORY}/politicians.json"

scraper = Scraper(TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD)
politicians = updateAndGetPoliticians(scraper, POLITICIANS_FILE)
succeded = getPoliticiansTweets(scraper, DATA_DIRECTORY, politicians)
infoMessage = "Scraping finished successfully" if succeded else "Failed to scrape all politicians due to the rate limit being reached."
print(infoMessage)



