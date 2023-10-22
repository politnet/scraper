import copy
import globals as gl
import json
import os
from userExtractor import extractUser, extractUserMentions, setPoliticianLastUpdatedToNow, savePoliticians

def extractEntries(data):
    instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    for instruction in instructions:
        if 'entries' in instruction:
            return instruction['entries']
    return []

def extractTweet(result):
    user = result['core']['user_results']['result']
    legacy = result['legacy']
    if 'retweeted_status_result' in legacy:
        tweetData = extractTweetData(legacy['retweeted_status_result']['result'])
        tweetData['reposted'] = True
        tweetData['timeline_owner'] = extractUser(user)
        return tweetData
    else:
        return {
            "created_by": extractUser(user),
            "timeline_owner": extractUser(user),
            "user_mentions": extractUserMentions(legacy),
            "id": legacy['id_str'],
            "created_at": legacy['created_at'],
            "full_text": legacy['full_text'],
            "reposted": False
        }
    
def extractTweetData(result):
    if result['__typename'] == "Tweet":
        return extractTweet(result)
    elif result['__typename'] == 'TweetWithVisibilityResults':
        return extractTweet(result['tweet'])
    
def getTweets(data):
    tweets = []
    for entry in extractEntries(data):
        if 'tweet' in entry['entryId']:
            tweetFullData = entry['content']['itemContent']['tweet_results']['result']
            tweets.append(extractTweetData(tweetFullData))
    return tweets

def readPoliticianTweets(politician):
    filepath = f'{gl.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
    if os.path.isfile(filepath) == False:
        return []
    
    with open(filepath, encoding="utf8") as file:
        data = json.load(file)
        return data

def getScrapedTweets(scraper, politician):
    rawTweets = scraper.tweets([politician['user_id']])
    tweets = []
    for rawTweet in rawTweets:
        tweets += getTweets(rawTweet)
    return tweets

def combineTweets(tweets1, tweets2):
    tweets = copy.deepcopy(tweets1)
    for tweet in tweets2:
        if not any(existing_tweet['id'] == tweet['id'] for existing_tweet in tweets):
            tweets.append(tweet)
    return tweets

def saveTweets(politician, tweets):
    filepath = f'{gl.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
    with open(filepath, 'w+', encoding="utf8") as file:
        json.dump(tweets, file, indent=4, ensure_ascii=False)

def sortByLastModified(politicians):
    return sorted(politicians, key=lambda politician: politician['last_modified'])
       
def getPoliticiansTweets(scraper, politicians):
    try:
        for politician in sortByLastModified(politicians):
            print(f"Getting tweets for {politician['user_account_name']}...")
            scrapedTweets = getScrapedTweets(scraper, politician)
            savedTweets = readPoliticianTweets(politician)
            combinedTweets = combineTweets(savedTweets, scrapedTweets)
            saveTweets(politician, combinedTweets)
            setPoliticianLastUpdatedToNow(politician)
            print(f"Saving {len(combinedTweets) - len(scrapedTweets)} new tweets for {politician['user_account_name']}")
        savePoliticians(politicians)
        return True
    except Exception as e:
        savePoliticians(politicians)
        return False
    
