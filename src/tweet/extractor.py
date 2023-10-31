import globals
from user.extractor import UserExtractor
from user.utils import PoliticianUtils
from tweet.utils import TweetUtils

class TweetExtractor:
    
    def __init__(self, scraper):
        self.scraper = scraper
    
    def __extract_instructions(data):
        return data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    
    def __extract_tweet(result):
        if result['__typename'] == "Tweet":
            return TweetExtractor.__extract_tweet_data(result)
        elif result['__typename'] == 'TweetWithVisibilityResults':
            return TweetExtractor.__extract_tweet_data(result['tweet'])
    
    def __extract_entries(data):
        entries = []
        instructions = TweetExtractor.__extract_instructions(data)
        for instruction in instructions:
            entries += instruction['entries'] if 'entries' in instruction else []
            entries += [instruction['entry']] if 'entry' in instruction else []
        return list(filter(lambda entry: entry['entryId'].startswith('tweet'), entries))

    def __extract_tweet_data(result):
        user = result['core']['user_results']['result']
        legacy = result['legacy']
        if 'retweeted_status_result' in legacy:
            tweetData = TweetExtractor.__extract_tweet(legacy['retweeted_status_result']['result'])
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
    
    def __extract_tweets(data):
        tweets = []
        for entry in TweetExtractor.__extract_entries(data):
            if 'tweet' in entry['entryId']:
                try:
                    tweet_full_data = entry['content']['itemContent']['tweet_results']['result']
                    tweet_full_data = tweet_full_data if 'core' in tweet_full_data else tweet_full_data['tweet']
                    tweets.append(TweetExtractor.__extract_tweet_data(tweet_full_data))
                except KeyError as e:
                    print("Skipping entry due to the KeyError. Error: ", e)
                    continue
        return tweets

    def __scrape_tweets(self, politician, limit):
        raw_tweets_data = None
        tweets = []
        
        try:
            if limit is None:
                raw_tweets_data = self.scraper.tweets([politician['user_id']]) 
            else: 
                raw_tweets_data = self.scraper.tweets([politician['user_id']], limit)
        except:
            print(f"Failed to scrape tweets for {politician['user_account_name']}. Rate limit exceeded.")
            return None
        
        for raw_tweet_data in raw_tweets_data:
            tweets += TweetExtractor.__extract_tweets(raw_tweet_data)
        return tweets
    
    def __get_politician_tweets(self, politician, limit):
        print(f"Getting tweets for {politician['user_account_name']}...")
        scraped_tweets = self.__scrape_tweets(politician, limit = limit)
        if scraped_tweets is None:
            return False
        
        saved_tweets = TweetUtils.read_tweets(politician)
        combined_tweets = TweetUtils.combine_tweets(saved_tweets, scraped_tweets)
        TweetUtils.save_tweets(politician, combined_tweets)
        PoliticianUtils.set_politician_last_updated_to_now(politician)
        print(f"Saving {len(combined_tweets) - len(saved_tweets)} new tweets for {politician['user_account_name']}")
        PoliticianUtils.save_politician(politician)
        
        return True
        
    def __get_all_politicians_tweets(self, politicians, limit):
        for politician in PoliticianUtils.sort_by_last_modified(politicians):
            scraped = self.__get_politician_tweets(politician, limit)
            if not scraped:
                return False
            
        return True
        
    def get_all_politicians_tweets(self, limit):
        print("Getting tweets for all saved politicians...")
        politicians = PoliticianUtils.read_politicians()
        succeeded = self.__get_all_politicians_tweets(politicians, limit)
        print("Result of scraping tweets: ", "Succeeded" if succeeded else "Failed")
        
    def get_politician_tweets(self, account_name, limit):
        print(f"Getting tweets for {account_name}...")
        politician = PoliticianUtils.read_politcian_by_account_name(account_name)
        if politician is None:
            print(f"Politician with account name {account_name} is not saved in {globals.POLITICIANS_FILE}.")
            return
        
        succeeded = self.__get_politician_tweets(politician, limit)
        print("Result of scraping tweets: ", "Succeeded" if succeeded else "Failed")

    
