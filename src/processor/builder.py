from user.utils import PoliticianUtils
from tweet.utils import TweetUtils

class DescriptionBuilder:
    
    DESCRIPTION_QUERY_TEMPALTE = """
        This is a current description of the politician: 

        "{description}"

        These are new, enumerated tweets of the politician:

        {tweets_str}

        Combine the current description with the tweets above and write a new description for the politician.
    """
    
    def build_description_query(politician, unprocessed_tweets):
        description = "" if politician["description"] is None else politician["description"]
        tweets_str = "\n".join([f'{i+1}. "{tweet["full_text"]}"\n' for i, tweet in enumerate(unprocessed_tweets)])
        return DescriptionBuilder.DESCRIPTION_QUERY_TEMPALTE.format(
            description=description, 
            tweets_str=tweets_str
        )

    def build_politicians_description_query(num_of_tweets):
        num_of_tweets = int(num_of_tweets)
        politicians = PoliticianUtils.read_politicians()
        result = []
        for politician in politicians:
            unprocessed_tweets = TweetUtils.read_unprocessed_tweets(politician, num_of_tweets)
            if len(unprocessed_tweets) <= 0:
                result.append({
                    "built": False,
                    "user_account_name": politician["user_account_name"],
                    "message": f"Politician {politician['user_account_name']} has no unprocessed tweets."
                })
                continue
            
            description_query = DescriptionBuilder.build_description_query(politician, unprocessed_tweets)
            result.append({
                "built": True,
                "user_account_name": politician["user_account_name"],
                "description_query": description_query,
                "used_tweets": unprocessed_tweets
            })
        return result