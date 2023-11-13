from argparse import ArgumentParser
import globals

class ArgsParser:
    
    def build_add_twitter_account_subparser(subparsers):
        parser = subparsers.add_parser(globals.add_twitter_account_cmd, help="Add a Twitter account to politicians")
        parser.add_argument("account_name", help="Name of the account to add")
        parser.add_argument("political_party", help="Political party of the politican")
        
    def build_scrape_tweets_subparser(subparsers):
        parser = subparsers.add_parser(globals.scrape_tweets_cmd, help="Scrape tweets of all saved politicians")
        parser.add_argument("--account-name", help="Name of the single account to scrape")
        parser.add_argument("--limit", help="Limit of number of scraped tweets")
        parser.add_argument("--batch-size", help="Number of scraper politicians per request")
        
    def build_schedule_tweets_scraping_subparser(subparsers):
        parser = subparsers.add_parser(globals.schedule_tweets_scraping_cmd, help="Schedule tweets scraping of saved politicians")
        parser.add_argument("interval", help="Interval between scraping in minutes")
        parser.add_argument("--limit", help="Limit of number of scraped tweets")
        parser.add_argument("--batch-size", help="Number of scraper politicians per request")

    def get_parser():
        parser = ArgumentParser(description="Twitter Account Management")  
        subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
        ArgsParser.build_add_twitter_account_subparser(subparsers)
        ArgsParser.build_scrape_tweets_subparser(subparsers)
        ArgsParser.build_schedule_tweets_scraping_subparser(subparsers)
        
        return parser