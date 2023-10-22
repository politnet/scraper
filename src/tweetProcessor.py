import globals as gl
import json

DESCRIPTION_QUERY_TEMPALTE = """
This is a current description of the politician: 

"{description}"

These are new, enumerated tweets of the politician:

{tweetsList}

Combine the current description with the tweets above and write a new description for the politician.
"""

def getUnprocessedTweets(politician, numberOfTweets = 20):
    filename = f'{gl.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
    
    with open(filename, encoding="utf8") as file:
        tweets = json.load(file)
        return [tweet for tweet in tweets if not tweet["processed"]][:numberOfTweets]
    
def getDescriptionQuery(politician, unprocessedTweets):
    description = "" if politician["description"] is None else politician["description"]
    tweetsList = "\n".join([f'{i+1}. "{tweet["full_text"]}"\n' for i, tweet in enumerate(unprocessedTweets)])
    descriptionQuery = DESCRIPTION_QUERY_TEMPALTE.format(
        description=description, 
        tweetsList=tweetsList
    )
    return descriptionQuery

def getPoliticiansDescriptionQuery(politicians):
    result = []
    for politician in politicians:
        unprocessedTweets = getUnprocessedTweets(politician)
        descriptionQuery = getDescriptionQuery(politician, unprocessedTweets)
        result.append({
            "user_account_name": politician["user_account_name"],
            "description_query": descriptionQuery,
            "used_tweets": unprocessedTweets
        })
    return result

def setTweetsToProcessed(descriptionQuery):
    for query in descriptionQuery:
        filepath = f'{gl.TWEETS_DIRECTORY}/{query["user_account_name"]}.json'
        unprocessedTweetsIds = [tweet["id"] for tweet in query['used_tweets']]
        
        tweets = []
        with open(filepath, encoding="utf8") as file:
            tweets = json.load(file)
            for tweet in tweets:
                if tweet["id"] in unprocessedTweetsIds:
                    tweet["processed"] = True
                    
        with open(filepath, 'w+', encoding="utf8") as file:
            json.dump(tweets, file, indent=4, ensure_ascii=False)