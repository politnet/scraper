import copy
import globals
import json
import os

class TweetUtils:
    
    def sort_tweets_by_date(tweets):
        return sorted(tweets, key=lambda tweet: tweet["created_at"])
    
    def save_tweets(politician, tweets):
        file_path = f'{globals.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
        with open(file_path, 'w+', encoding="utf8") as file:
            sorted_tweets = sort_tweets_by_date(tweets)
            json.dump(sorted_tweets, file, indent=4, ensure_ascii=False)
            
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
        
    def combine_tweets(tweets1, tweets2):
        tweets = copy.deepcopy(tweets1)
        for tweet in tweets2:
            if not any(existing_tweet['id'] == tweet['id'] for existing_tweet in tweets):
                tweets.append(tweet)
        return tweets