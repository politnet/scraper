from userExtractor import extractUser, extractUserMentions

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