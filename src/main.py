import json
import os
import sys
from twitter.scraper import Scraper
from tweetExtractor import getTweets

if len(sys.argv) < 4:
    print("Incorrect invocation. Usage: python main.py [twitter_email] [twitter_username] [twitter_password]")
    exit(0)
    
TWITTER_EMAIL = sys.argv[1]
TWITTER_USERNAME = sys.argv[2]
TWITTER_PASSWORD = sys.argv[3]

def getTweetsFromWeb():
    scraper = Scraper(TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD, save=True)
    rawTweets = scraper.tweets(['3242182113'])
    return[getTweets(rawTweet) for rawTweet in rawTweets]
       
def getTweetsFromFile(baseDirectory): 
    tweets = []
    for file in os.listdir(baseDirectory):
        with open(f'{baseDirectory}/{file}', encoding="utf8") as json_file:
            data = json.load(json_file)
            tweets += getTweets(data)
    return tweets

tweets = getTweetsFromFile("data/3242182113") # getTweetsFromWeb()
with open('data/processed/3242182113.json', 'w+', encoding="utf8") as outfile:
    json.dump(tweets, outfile, indent=4, ensure_ascii=False)

