from argparse import ArgumentParser
import globals

class ArgsParser:
    
    def build_add_twitter_account_subparser(subparsers):
        parser = subparsers.add_parser(globals.add_twitter_account_cmd, help="Add a Twitter account to politicians")
        parser.add_argument("account_name", help="Name of the account to add")
        parser.add_argument("political_party", help="Political party of the politican")
        
    def build_description_queries_subparser(subparsers):
        parser = subparsers.add_parser(globals.build_description_queries_cmd, help="Build description queries of saved politicians")
        parser.add_argument("--num-of-tweets", help="Description queries to build")
        
    def build_scrape_tweets_subparser(subparsers):
        parser = subparsers.add_parser(globals.scrape_tweets_cmd, help="Scrape tweets of all saved politicians")
        parser.add_argument("--account-name", help="Name of the single account to scrape")
        
    def build_schedule_tweets_scraping_subparser(subparsers):
        parser = subparsers.add_parser(globals.schedule_tweets_scraping_cmd, help="Schedule tweets scraping of saved politicians")
        parser.add_argument("--interval", help="Interval between scraping in minutes")
        parser.add_argument("--limit", help="Limit of number of scraped tweets")

    def get_parser():
        parser = ArgumentParser(description="Twitter Account Management")
        parser.add_argument("-e", "--email", required=True, help="Email address")
        parser.add_argument("-u", "--username", required=True, help="Username")
        parser.add_argument("-p", "--password", required=True, help="Password")
        
        subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
        ArgsParser.build_add_twitter_account_subparser(subparsers)
        ArgsParser.build_description_queries_subparser(subparsers)
        ArgsParser.build_scrape_tweets_subparser(subparsers)
        ArgsParser.build_schedule_tweets_scraping_subparser(subparsers)
        
        return parser