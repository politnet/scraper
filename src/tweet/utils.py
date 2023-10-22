import globals
import json
import os

class TweetUtils:
    
    def save_tweets(politician, tweets):
        file_path = f'{globals.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
        if not os.path.isfile(file_path):
            return []
        
        with open(file_path, 'w+', encoding="utf8") as file:
            json.dump(tweets, file, indent=4, ensure_ascii=False)
            
    def read_tweets(politician):
        file_path = f'{globals.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
        if not os.path.isfile(file_path):
            return []

        with open(file_path, encoding="utf8") as file:
            return json.load(file)   
            
    def read_unprocessed_tweets(politician, num_of_tweets):
        tweets = TweetUtils.read_tweets(politician)
        return [tweet for tweet in tweets if not tweet["processed"]][:num_of_tweets]
        
    def set_tweets_to_processed(politician, unprocessed_tweets):
        for tweets in TweetUtils.read_tweets(politician):
            for tweet in tweets:
                if tweet["id"] in [unprocessed_tweet["id"] for unprocessed_tweet in unprocessed_tweets]:
                    tweet["processed"] = True
                    
        TweetUtils.save_tweets(politician, tweets)