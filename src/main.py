import globals
from argsParser import ArgsParser
from user.utils import PoliticianUtils
from tweet.extractor import TweetExtractor
from processor.builder import DescriptionBuilder
from processor.scheduler import TweetScheduler
from twitter.scraper import Scraper
from twitter.util import init_session

def get_guest_scraper():
    return Scraper(session=init_session(), out=globals.OUT_DIRECTORY)

def get_account_scraper(args):
    return Scraper(email=args.email, username=args.username, password=args.password, out=globals.OUT_DIRECTORY)  

def add_twitter_account(scraper, account_name):
    pass

def build_description_queries(scraper, num_of_tweets):
    if num_of_tweets is None:
        num_of_tweets = globals.DEFAULT_DESCRIPTION_QUERY_NUM_OF_TWEETS
    pass

def scrape_tweets(scraper):
    pass

def schedule_tweets_scraping(scraper, interval):
    if interval is None:
        interval = globals.DEFAULT_SCHEDULER_INTERVAL
    pass

parser = ArgsParser.get_parser()
args = parser.parse_args()

# Login parsing
scraper = None
if args.login == globals.account_login_cmd:
    print("Using twitter account.")
    scraper = get_account_scraper(args)
elif args.login == globals.guest_session_cmd:
    print("Using guest session.")
    scraper = get_guest_scraper()
else:
    parser.error("Invalid login method.")
    
if args.command == globals.add_twitter_account_cmd:
    print("Adding twitter account...")
    add_twitter_account(scraper, args.account_name)
elif args.command == globals.build_description_queries_cmd:
    print("Building description queries...")
    build_description_queries(scraper, args.num_of_tweets)
elif args.command == globals.scrape_tweets_cmd:
    print("Scraping tweets...")
    scrape_tweets(scraper)
elif args.command == globals.schedule_tweets_scraping_cmd:
    print("Scheduling tweets scraping..")
    schedule_tweets_scraping(scraper, args.interval)
else:
    parser.error("Invalid command.")


