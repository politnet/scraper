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

def add_twitter_account(scraper, account_name, political_party):
    PoliticianUtils(scraper).fetch_and_add_politican(account_name, political_party)

def build_description_queries(num_of_tweets):
    if num_of_tweets is None:
        num_of_tweets = globals.DEFAULT_DESCRIPTION_QUERY_NUM_OF_TWEETS
    # Temporary solution
    description_queries = DescriptionBuilder.build_politicians_description_query(num_of_tweets)
    print(description_queries)

def scrape_tweets(scraper, account_name, limit):
    if account_name is None:
        TweetExtractor(scraper).get_all_politicians_tweets(limit)
    else:
        TweetExtractor(scraper).get_politician_tweets(account_name, limit)

def schedule_tweets_scraping(scraper, interval, limit):
    interval = globals.DEFAULT_SCHEDULER_INTERVAL if interval is None else interval
    TweetScheduler(scraper).schedule_scraping(interval, limit)

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
    print(f"Adding twitter account {args.account_name}...")
    add_twitter_account(scraper, args.account_name, args.political_party)
elif args.command == globals.build_description_queries_cmd:
    print("Building description queries...")
    build_description_queries(args.num_of_tweets)
elif args.command == globals.scrape_tweets_cmd:
    print("Scraping tweets...")
    scrape_tweets(scraper, args.account_name, args.limit)
elif args.command == globals.schedule_tweets_scraping_cmd:
    print("Scheduling tweets scraping..")
    schedule_tweets_scraping(scraper, args.interval, args.limit)
else:
    parser.error("Invalid command.")