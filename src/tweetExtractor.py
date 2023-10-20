def getEntries(data):
    instructions = data['data']['user']['result']['timeline_v2']['timeline']['instructions']
    for instruction in instructions:
        if 'entries' in instruction:
            return instruction['entries']
    return []

def extractUser(result):
    user = result['core']['user_results']['result']
    return {
        "user_id": user['rest_id'],
        "user_full_name": user['legacy']['name'],
        "user_account_name": user['legacy']['screen_name'],
    }
    
def extractMentionedUser(mention):
    return {
        "user_id": mention['id_str'],
        "user_full_name": mention['name'],
        "user_account_name": mention['screen_name'],
    }

def extractUserMentions(legacy):
    return [extractMentionedUser(mention) for mention in legacy['entities']['user_mentions']]

def extractTweet(result):
    legacy = result['legacy']
    if 'retweeted_status_result' in legacy:
        tweetData = extractTweetData(legacy['retweeted_status_result']['result'])
        tweetData['reposted'] = True
        tweetData['timeline_owner'] = extractUser(result)
        return tweetData
    else:
        return {
            "created_by": extractUser(result),
            "timeline_owner": extractUser(result),
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
    for entry in getEntries(data):
        if 'tweet' in entry['entryId']:
            tweetFullData = entry['content']['itemContent']['tweet_results']['result']
            tweets.append(extractTweetData(tweetFullData))
    return tweets