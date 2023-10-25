import globals
from argparse import ArgumentParser
from user.utils import PoliticianUtils
from tweet.extractor import TweetExtractor
from processor.builder import DescriptionBuilder
from processor.scheduler import TweetScheduler
from twitter.scraper import Scraper
from twitter.util import init_session

# def get_guest_scraper():
#     return Scraper(session=init_session(), out=globals.OUT_DIRECTORY)

# def get_account_scraper(args):
#     return Scraper(email=args.email, username=args.username, password=args.password, out=globals.OUT_DIRECTORY)      
    
# def perfrom_action(scraper, action):
#     action_name, value = action
    
#     if action_name == "add-politician":
#         print(f"Adding politician {value}...")
#         PoliticianUtils(scraper).fetch_and_save_politican(value)
#     elif action_name == "build-description-queries":
#         print("Building description queries...")
#         description_queries = DescriptionBuilder.build_politicians_description_query(value)
#         print(description_queries)
#     elif action_name == "scrape-tweets":
#         print("Scraping tweets...")
#         TweetExtractor(scraper).get_politicians_tweets()
#     elif action_name == "schedule-tweets-scraping":
#         print("Scheduling tweets scraping...")
#         TweetScheduler(scraper).schedule_scraping(value)
#     else:
#         raise ValueError(f"Invalid action: {action}. Valid actions: {globals.LIST_OF_ACTIONS}.")
    
# parser = ArgumentParser()
# parser.add_argument("--account-scraper", "-as", action="store_true", help="Enable account scraper mode")
# parser.add_argument("--guest-scraper", "-gs", action="store_true", help="Enable guest scraper mode")
# parser.add_argument("--email", "-e", help="Twitter email")
# parser.add_argument("--username", "-u", help="Twitter username")
# parser.add_argument("--password", "-p", help="Twitter password")
# parser.add_argument("--action", "-a", nargs=2, help="Action to perform")

# args = parser.parse_args()

# if args.account_scraper:
#     if not args.email or not args.username or not args.password or not args.action:
#         parser.error("When using account scraper mode, you must provide --email, --username, --password and --action")
        
#     print("Using account scraper mode")
#     scraper = get_account_scraper(args)
#     perfrom_action(scraper, args.action)
# elif args.guest_scraper:
#     if not args.action:
#         parser.error("When using guest scraper mode, you must provide --action.")
    
#     print("Using guest scraper mode")
#     scraper = get_guest_scraper()
#     perfrom_action(scraper, args.action)
# else:
#     parser.print_help()
#     print("Error: Invalid scraper mode")

# def set_login_method_subparser(parser):
#     subparsers = parser.add_subparsers()
    
#     subparsers.add_parser("guest-session")

#     account_parser = subparsers.add_parser("account-login")
#     account_parser.add_argument("--email", "-e", required=True, help="Twitter email")
#     account_parser.add_argument("--username", "-u", required=True, help="Twitter username")
#     account_parser.add_argument("--password", "-p", required=True, help="Twitter password")

# parser = ArgumentParser()
# subparsers = parser.add_subparsers()

# add_twitter_account_parser = subparsers.add_parser("add-twitter-account")
# set_login_method_subparser(add_twitter_account_parser)

# args = parser.parse_args()

# print(args)

# def set_login_method_subparser(parser):
#     subparsers = parser.add_subparsers()
    
#     subparsers.add_parser("guest-session")

#     account_parser = subparsers.add_parser("account-login")
#     account_parser.add_argument("--email", "-e", required=True, help="Twitter email")
#     account_parser.add_argument("--username", "-u", required=True, help="Twitter username")
#     account_parser.add_argument("--password", "-p", required=True, help="Twitter password")

def get_guest_scraper():
    return Scraper(session=init_session(), out=globals.OUT_DIRECTORY)

def get_account_scraper(args):
    return Scraper(email=args.email, username=args.username, password=args.password, out=globals.OUT_DIRECTORY)  

def set_add_twitter_account_subparser(subparsers):
    parser = subparsers.add_parser("add-twitter-account", help="Add a Twitter account to politicians")
    parser.add_argument("account_name", help="Name of the account to add")
    
def set_build_description_queries_subparser(parser):
    parser = subparsers.add_parser("build-description-queries", help="Build description queries of saved politicians")
    parser.add_argument("--num-of-tweets", help="Description queries to build")
    
def set_scrape_tweets_subparser(subparsers):
    subparsers.add_parser("scrape-tweets", help="Scrape tweets of saved politicians")

def set_schedule_tweets_scraping_subparser(subparsers):
    parser = subparsers.add_parser("schedule-tweets-scraping", help="Schedule tweets scraping of saved politicians")
    parser.add_argument("--interval", help="Interval between scraping in minutes")

parser = ArgumentParser(description="Twitter Account Management")
parser.add_argument("account_type", choices=["account-login", "guest-session"], help="Choose login method")

# Common arguments for both "account-login"
parser.add_argument("-e", "--email", help="Email address")
parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="Password")

# Subparsers for different commands
subparsers = parser.add_subparsers(dest="command", help="Available commands")

# Subparsers
set_add_twitter_account_subparser(subparsers)
set_build_description_queries_subparser(subparsers)
set_scrape_tweets_subparser(subparsers)
set_schedule_tweets_scraping_subparser(subparsers)

args = parser.parse_args()

# Login parsing
scraper = None
if args.account_type == "account-login":
    print("Login using twitter account.")
    if not (args.email and args.username and args.password):
        parser.error("For 'account-login', you must provide email, username, and password of your twitter account.")
    scraper = get_account_scraper(args)
elif args.account_type == "guest-session":
    print("Using guest session.")
    scraper = get_guest_scraper()
else:
    parser.error("Invalid login method.")
    
if args.command == "add-twitter-account":
    print("add-twitter-account")
    # set_add_twitter_account_subparser(add_twitter_account_parser)
    print(args.account_name)
elif args.command == "build-description-queries":
    print("build-description-queries")
    # set_add_twitter_account_subparser(build_description_query_parser)
    print(args.num_of_tweets)
elif args.command == "scrape-tweets":
    print("scrape-tweets")
    # set_scrape_tweets_subparser(scrape_tweets_parser)
elif args.command == "schedule-tweets-scraping":
    print("schedule-tweets-scraping")
    # set_schedule_tweets_scraping_subparser(schedule_tweets_scraping_parser)
    print(args.interval)
else:
    parser.error("Invalid command.")


