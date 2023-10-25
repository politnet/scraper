from user.extractor import UserExtractor
from user.utils import PoliticianUtils
from tweet.utils import TweetUtils

class TweetExtractor:
    
    def __init__(self, scraper):
        self.scraper = scraper
        
    def extract_entries(data):
        entries = []
        instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if 'entries' in instruction:
                entries += instruction['entries']
            elif 'entry' in instruction:
                entries += [instruction['entry']]
        return entries

    def extract_tweet_data(result):
        user = result['core']['user_results']['result']
        legacy = result['legacy']
        if 'retweeted_status_result' in legacy:
            tweetData = TweetExtractor.extract_tweet(legacy['retweeted_status_result']['result'])
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
    
    def extract_tweet(result):
        if result['__typename'] == "Tweet":
            return TweetExtractor.extract_tweet_data(result)
        elif result['__typename'] == 'TweetWithVisibilityResults':
            return TweetExtractor.extract_tweet_data(result['tweet'])
    
    def extract_tweets(data):
        tweets = []
        for entry in TweetExtractor.extract_entries(data):
            if 'tweet' in entry['entryId']:
                try:
                    tweet_full_data = entry['content']['itemContent']['tweet_results']['result']
                    tweets.append(TweetExtractor.extract_tweet_data(tweet_full_data))
                except KeyError as e:
                    print("Skipping entry due to the KeyError. Error: ", e)
                    continue
        return tweets

    def __scrape_tweets(self, politician):
        raw_tweets_data = None
        tweets = []
        
        try:
            raw_tweets_data = self.scraper.tweets([politician['user_id']])
        except:
            print(f"Failed to scrape tweets for {politician['user_account_name']}. Rate limit exceeded.")
            return None
        
        for raw_tweet_data in raw_tweets_data:
            tweets += TweetExtractor.extract_tweets(raw_tweet_data)
        return tweets
    
    def __get_politicians_tweets(self, politicians):
        for politician in PoliticianUtils.sort_by_last_modified(politicians):
            print(f"Getting tweets for {politician['user_account_name']}...")
            scraped_tweets = self.__scrape_tweets(politician)
            if scraped_tweets is None:
                return False
            
            saved_tweets = TweetUtils.read_tweets(politician)
            combined_tweets = TweetUtils.combine_tweets(saved_tweets, scraped_tweets)
            TweetUtils.save_tweets(politician, combined_tweets)
            PoliticianUtils.set_politician_last_updated_to_now(politician)
            print(f"Saving {len(combined_tweets) - len(saved_tweets)} new tweets for {politician['user_account_name']}")
            PoliticianUtils.save_politicans(politicians)
            
        return True
        
    def get_politicians_tweets(self):
        politicians = PoliticianUtils.read_politicians()
        succeeded = self.__get_politicians_tweets(politicians)
        print("Result of scraping tweets: ", "Succeeded" if succeeded else "Failed")

    
