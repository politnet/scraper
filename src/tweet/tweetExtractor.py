import copy
import globals as gl
import json
from user.extractors import UserExtractor
from user.utils import PoliticianUtils
from tweet.utils import TweetUtils

class TweetExtractor:
    
    def __extract_entries(data):
        instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
        for instruction in instructions:
            if 'entries' in instruction:
                return instruction['entries']
        return []

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
                "user_mentions": UserExtractor.extract_mentioned_user(legacy),
                "id": legacy['id_str'],
                "created_at": legacy['created_at'],
                "full_text": legacy['full_text'],
                "reposted": False,
                "processed": False
            }
    
    def __extract_tweet(result):
        if result['__typename'] == "Tweet":
            return TweetExtractor.__extract_tweet_data(result)
        elif result['__typename'] == 'TweetWithVisibilityResults':
            return TweetExtractor.__extract_tweet_data(result['tweet'])
    
    def __get_tweets(data):
        tweets = []
        for entry in TweetExtractor.__extract_entries(data):
            if 'tweet' in entry['entryId']:
                try:
                    tweet_full_data = entry['content']['itemContent']['tweet_results']['result']
                    tweets.append(TweetExtractor.__extract_tweet_data(tweet_full_data))
                except KeyError:
                    print("Skipping entry due to the KeyError.")
                    continue
        return tweets

    def __get_scraped_tweets(scraper, politician):
        raw_tweets = scraper.tweets([politician['user_id']])
        tweets = []
        for raw_tweet in raw_tweets:
            tweets += TweetExtractor.__get_tweets(raw_tweet)
        return tweets
    
    def getPoliticiansTweets(scraper, politicians):
        try:
            for politician in PoliticianUtils.sort_by_last_modified(politicians):
                print(f"Getting tweets for {politician['user_account_name']}...")
                scraped_tweets = TweetExtractor.__get_scraped_tweets(scraper, politician)
                saved_tweets = TweetUtils.read_tweets(politician)
                combined_tweets = TweetUtils.combine_tweets(saved_tweets, scraped_tweets)
                TweetUtils.save_tweets(politician, combined_tweets)
                PoliticianUtils.set_politician_last_updated_to_now(politician)
                print(f"Saving {len(combined_tweets) - len(scraped_tweets)} new tweets for {politician['user_account_name']}")
            PoliticianUtils.save_politicans(politicians)
            return True
        except KeyError as e:
            print(f"KeyError: {e}")
            PoliticianUtils.save_politicans(politicians)
            return False
        except Exception:
            PoliticianUtils.save_politicans(politicians)
            return False

    filepath = f'{gl.TWEETS_DIRECTORY}/{politician["user_account_name"]}.json'
    with open(filepath, 'w+', encoding="utf8") as file:
        json.dump(tweets, file, indent=4, ensure_ascii=False)

    
