import globals
from argparse import ArgumentParser
from user.extractors import PoliticianExtractor
from twitter.scraper import Scraper
from twitter.util import init_session

def get_guest_scraper():
    return Scraper(session=init_session(), out=globals.OUT_DIRECTORY)

def get_account_scraper(args):
    return Scraper(email=args.email, username=args.username, password=args.password, out=globals.OUT_DIRECTORY)      
    
def perfrom_action(scraper, action):
    action_name, value = action
    
    if action_name == "add-politician":
        politician_extractor = PoliticianExtractor(scraper)
        politician_extractor.fetch_and_save_politican(value)
    else:
        raise ValueError(f"Invalid action: {action}. Valid actions: {globals.LIST_OF_ACTIONS}.")
    
parser = ArgumentParser()
parser.add_argument("--account-scraper", "-as", action="store_true", help="Enable account scraper mode")
parser.add_argument("--guest-scraper", "-gs", action="store_true", help="Enable guest scraper mode")
parser.add_argument("--email", "-e", help="Twitter email")
parser.add_argument("--username", "-u", help="Twitter username")
parser.add_argument("--password", "-p", help="Twitter password")
parser.add_argument("--action", "-a", nargs=2, help="Action to perform")

args = parser.parse_args()

if args.account_scraper:
    if not args.email or not args.username or not args.password or not args.action:
        parser.error("When using account scraper mode, you must provide --email, --username, --password and --action")
        
    print("Using account scraper mode")
    scraper = get_account_scraper(args)
    perfrom_action(scraper, args.action)
elif args.guest_scraper:
    if not args.action:
        parser.error("When using guest scraper mode, you must provide --action.")
    
    print("Using guest scraper mode")
    scraper = get_guest_scraper()
    perfrom_action(scraper, args.action)
else:
    parser.print_help()
    print("Error: Invalid scraper mode")
