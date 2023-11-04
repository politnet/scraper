import globals

from argsParser import ArgsParser
from politician.utils import PoliticianUtils
from tweet.scraper import TweetScraper
from processor.scheduler import TweetScheduler
from twitter.scraper import Scraper

def get_account_scraper(args):
    return Scraper(email=args.email, username=args.username, password=args.password, out=globals.OUT_DIRECTORY)  

def add_twitter_account(scraper, account_name, political_party):
    PoliticianUtils(scraper).fetch_and_add_politican(account_name, political_party)

def scrape_tweets(scraper, account_name, limit, batch_size):
    limit = int(limit) if limit is not None else globals.DEFAULT_LIMIT
    batch_size = int(batch_size) if limit is not None else globals.DEFAULT_BATCH_SIZE
    if account_name is None:
        TweetScraper(scraper).scrape_all_politicians_tweets(limit, batch_size)
    else:
        TweetScraper(scraper).scrape_politician_tweets_by_account_name(account_name, limit)

def schedule_tweets_scraping(scraper, interval, limit, batch_size):
    limit = int(limit) if limit is not None else globals.DEFAULT_LIMIT
    batch_size = int(batch_size) if batch_size is not None else globals.DEFAULT_BATCH_SIZE
    TweetScheduler(scraper).schedule_scraping(interval, limit, batch_size)

parser = ArgsParser.get_parser()
args = parser.parse_args()
scraper  = get_account_scraper(args)
logger = globals.get_logger(__name__)

if args.command == globals.add_twitter_account_cmd:
    logger.info(f"Adding twitter account {args.account_name}...")
    add_twitter_account(scraper, args.account_name, args.political_party)
elif args.command == globals.scrape_tweets_cmd:
    logger.info(f"Scraping tweets of {args.account_name} with limit {args.limit} and batch size {args.batch_size}...")
    scrape_tweets(scraper, args.account_name, args.limit, args.batch_size)
elif args.command == globals.schedule_tweets_scraping_cmd:
    logger.info(f"Scheduling tweets scraping with interval of {args.interval} minutes, with limit {args.limit} and batch size {args.batch_size}....")
    schedule_tweets_scraping(scraper, args.interval, args.limit, args.batch_size)
else:
    parser.error("Invalid command.")