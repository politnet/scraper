# Default values for the application
DEFAULT_DESCRIPTION_QUERY_NUM_OF_TWEETS = 25
DEFAULT_SCHEDULER_INTERVAL = 30 # minutes

# Command line arguments
account_login_cmd = "account-login"
guest_session_cmd = "guest-session"
add_twitter_account_cmd = "add-twitter-account"
build_description_queries_cmd = "build-description-queries"
scrape_tweets_cmd = "scrape-tweets"
schedule_tweets_scraping_cmd = "schedule-tweets-scraping"

# File paths
OUT_DIRECTORY = "out"
DATA_DIRECTORY = "data"
TWEETS_DIRECTORY = f"{DATA_DIRECTORY}/tweets"
POLITICIANS_FILE = f"{DATA_DIRECTORY}/politicians.json"


