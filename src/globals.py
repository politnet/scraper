import math
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

# Default values for the application
DEFAULT_DESCRIPTION_QUERY_NUM_OF_TWEETS = 25
DEFAULT_LIMIT = math.inf
DEFAULT_BATCH_SIZE = 1

# Command line arguments
add_twitter_account_cmd = "add-twitter-account"
build_description_queries_cmd = "build-description-queries"
scrape_tweets_cmd = "scrape-tweets"
schedule_tweets_scraping_cmd = "schedule-tweets-scraping"

# File paths
OUT_DIRECTORY = "out"
DATA_DIRECTORY = "data"
LOGS_DIRECTORY = "logs"
TWEETS_DIRECTORY = f"{DATA_DIRECTORY}/tweets"
POLITICIANS_FILE = f"{DATA_DIRECTORY}/politicians.json"

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    current_date = datetime.date.today().strftime("%Y-%m-%d")
    log_file = f"{LOGS_DIRECTORY}/{current_date}.log"
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


