from user.extractor import UserExtractor
from twitter.scraper import Scraper

class TweetExtractor:
    
    def __init__(self, scraper : Scraper):
        self.scraper = scraper
    
    def extract_instructions(data : dict):
        return data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    
    def extract_tweet_entries(data : dict):
        entries = []
        instructions = TweetExtractor.extract_instructions(data)
        for instruction in instructions:
            entries += instruction['entries'] if 'entries' in instruction else []
            entries += [instruction['entry']] if 'entry' in instruction else []
        return list(filter(lambda entry: entry['entryId'].startswith('tweet'), entries))

    def extract_tweet_data(result : dict):
        result = result if 'core' in result else result['tweet']
        user = result['core']['user_results']['result']
        legacy = result['legacy']
        if 'retweeted_status_result' in legacy:
            tweetData = TweetExtractor.extract_tweet_data(legacy['retweeted_status_result']['result'])
            tweetData['reposted'] = True
            tweetData['timeline_owner'] = UserExtractor.extract_user(user)
            return tweetData
        else:
            return {
                "created_by": UserExtractor.extract_user(user),
                "timeline_owner": UserExtractor.extract_user(user),
                "user_mentions": UserExtractor.extract_mentioned_users(legacy),
                "id": legacy['id_str'],
                "created_at": legacy['created_at'],
                "full_text": legacy['full_text'],
                "reposted": False,
                "processed": False
            }
    
    def extract_tweets_from_data(data : dict):
        tweets = []
        for entry in TweetExtractor.extract_tweet_entries(data):
            if 'tweet' in entry['entryId']:
                try:
                    tweet_full_data = entry['content']['itemContent']['tweet_results']['result']
                    tweets.append(TweetExtractor.extract_tweet_data(tweet_full_data))
                except KeyError as e:
                    print("Skipping entry due to the KeyError. Error: ", e)
                    continue
        return tweets
    
    def extract_tweets(raw_tweets_data : dict):
        tweets = []
        for raw_tweet_data in raw_tweets_data:
            tweets += TweetExtractor.extract_tweets_from_data(raw_tweet_data)
        return tweets
