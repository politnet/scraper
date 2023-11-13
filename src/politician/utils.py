import globals
import json
import datetime
from politician.extractor import UserExtractor
from twitter.scraper import Scraper
from pymongo.database import Database 

class PoliticianUtils:
    logger = globals.get_logger(__name__)
    
    def __init__(self, scraper : Scraper, db : Database):
        self.scraper = scraper
        self.db = db
        
    def __build_politician(user : dict):
        return {
            "user_id": user["user_id"],
            "user_full_name": user["user_full_name"],
            "user_account_name": user["user_account_name"],
            "description": None,
            "last_modified": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
    def __fetch_politician(self, account_name : str):
        raw_user = self.scraper.users([account_name])[0]
        user = UserExtractor.extract_user(raw_user['data']['user']['result'])
        return PoliticianUtils.__build_politician(user)     
    
    def __check_if_politician_exists(account_name : str):
        politicians = PoliticianUtils.read_politicians()
        for politician in politicians:
            if politician["user_account_name"] == account_name:
                return True
        return False
    
    def set_politician_last_updated_to_now(politician : dict):
        politician["last_modified"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    def update_politician(self, politician : dict):
        collection = self.db[globals.POLITICIANS_COLLECTION]
        filter = {'user_id': politician['user_id']}
        update = {'$set': politician}
        collection.update_one(filter, update)
            
    def sort_by_last_modified(politicians : list):
        return sorted(politicians, key=lambda politician: politician['last_modified'])

    def read_politicians():
        with open(globals.POLITICIANS_FILE, 'r', encoding="utf8") as file:
            data = json.load(file)
            return data["politicians"]
        
    def fetch_and_add_politican(self, account_name, politacal_party):
        if PoliticianUtils.__check_if_politician_exists(account_name):
            PoliticianUtils.logger.warning(f"Politician with account name {account_name} already exists.")
            return
        
        politician = self.__fetch_politician(account_name)
        politician['political_party'] = politacal_party
        collection = self.db[globals.POLITICIANS_COLLECTION]
        collection.insert_one(politician)
        
    def read_politcian_by_account_name(account_name):
        politicians = PoliticianUtils.read_politicians()
        for politician in politicians:
            if politician["user_account_name"] == account_name:
                return politician
        return None