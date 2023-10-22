import sys
from twitter.util import init_session
from twitter.scraper import Scraper
from tweetExtractor import getPoliticiansTweets
from tweetProcessor import getPoliticiansDescriptionQuery, setTweetsToProcessed
from userExtractor import updateAndGetPoliticians, readPoliticians

# ---- Get scraper ----
scraper = None

if len(sys.argv) < 2:
    print("Please provide a command scraper type - `python main.py guest` or `python main.py account`")
    exit()

if sys.argv[1] == "guest":
    scraper = Scraper(session=init_session(), save=True)
else:
    if len(sys.argv) < 5:
        print("Incorrect invocation. Usage: python main.py account [twitter_email] [twitter_username] [twitter_password]")
        exit()
    scraper = Scraper(sys.argv[2], sys.argv[3], sys.argv[4], save=True)

# ---- Scrape tweets ----
politicians = updateAndGetPoliticians(scraper)
succeded = getPoliticiansTweets(scraper, politicians)
infoMessage = "Scraping finished successfully" if succeded else "Failed to scrape all politicians due to the rate limit being reached."
print(infoMessage)

# ---- Process tweets ----
# completeUser,incompleteUsers = readPoliticians() 
# decsriptionQueries = getPoliticiansDescriptionQuery(completeUser + incompleteUsers)
# setTweetsToProcessed(decsriptionQueries)

# ---- Test ----
# from tweetExtractor import getScrapedTweets
# tweets = getScrapedTweets(scraper, {"user_id": "1206893629337419781"})
# print(tweets)

# ---- Test ----
# from tweetExtractor import getTweets
# import json

# with open("data/1206893629337419781/1697985311493005100_UserTweets.json", encoding="utf8") as file:
#     data = json.load(file)
#     tweets = getTweets(data)
#     print(tweets)
    





