from argparse import ArgumentParser
import globals

class ArgsParser:
    
    def __build_add_twitter_account_subparser(subparsers):
        parser = subparsers.add_parser(globals.add_twitter_account_cmd, help="Add a Twitter account to politicians")
        parser.add_argument("account_name", help="Name of the account to add")
        
    def __build_description_queries_subparser(subparsers):
        parser = subparsers.add_parser(globals.build_description_queries_cmd, help="Build description queries of saved politicians")
        parser.add_argument("--num-of-tweets", help="Description queries to build")
        
    def __build_scrape_tweets_subparser(subparsers):
        parser = subparsers.add_parser(globals.scrape_tweets_cmd, help="Scrape tweets of all saved politicians")
        parser.add_argument("--account-name", help="Name of the single account to scrape")
        
    def __build_schedule_tweets_scraping_subparser(subparsers):
        parser = subparsers.add_parser(globals.schedule_tweets_scraping_cmd, help="Schedule tweets scraping of saved politicians")
        parser.add_argument("--interval", help="Interval between scraping in minutes")
        
    def __build_command_subparsers(subparsers):
        ArgsParser.__build_add_twitter_account_subparser(subparsers)
        ArgsParser.__build_description_queries_subparser(subparsers)
        ArgsParser.__build_scrape_tweets_subparser(subparsers)
        ArgsParser.__build_schedule_tweets_scraping_subparser(subparsers)
        
    def __build_guest_session_subparser(subparsers):
        parser = subparsers.add_parser(globals.guest_session_cmd, help="Use guest session")
        
        subsubparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
        ArgsParser.__build_command_subparsers(subsubparsers)
        
    def __build_account_login_parser(subparsers):
        parser = subparsers.add_parser(globals.account_login_cmd, help="Use twitter account")
        parser.add_argument("-e", "--email", required=True, help="Email address")
        parser.add_argument("-u", "--username", required=True, help="Username")
        parser.add_argument("-p", "--password", required=True, help="Password")
        
        subsubparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
        ArgsParser.__build_command_subparsers(subsubparsers)

    def get_parser():
        parser = ArgumentParser(description="Twitter Account Management")
        subparsers = parser.add_subparsers(dest="login", required=True, help="Available commands")

        ArgsParser.__build_guest_session_subparser(subparsers)
        ArgsParser.__build_account_login_parser(subparsers)
        return parser