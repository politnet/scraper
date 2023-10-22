from user.utils import PoliticianUtils
from tweet.utils import TweetUtils

class DescriptionProcessor:
    
    DESCRIPTION_QUERY_TEMPALTE = """
        This is a current description of the politician: 

        "{description}"

        These are new, enumerated tweets of the politician:

        {tweets_str}

        Combine the current description with the tweets above and write a new description for the politician.
    """
    
    def generate_description_query(politician, unprocessed_tweets):
        description = "" if politician["description"] is None else politician["description"]
        tweets_str = "\n".join([f'{i+1}. "{tweet["full_text"]}"\n' for i, tweet in enumerate(unprocessed_tweets)])
        return DescriptionProcessor.DESCRIPTION_QUERY_TEMPALTE.format(
            description=description, 
            tweets_str=tweets_str
        )

    def generate_politicians_description_query(num_of_tweets):
        num_of_tweets = int(num_of_tweets)
        politicians = PoliticianUtils.read_politicians()
        result = []
        for politician in politicians:
            unprocessed_tweets = TweetUtils.read_unprocessed_tweets(politician, num_of_tweets)
            description_query = DescriptionProcessor.generate_description_query(politician, unprocessed_tweets)
            result.append({
                "user_account_name": politician["user_account_name"],
                "description_query": description_query,
                "used_tweets": unprocessed_tweets
            })
        return result