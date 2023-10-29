import globals as gl
import json
import datetime
from user.extractor import UserExtractor

class PoliticianUtils:
        
    def __init__(self, scraper):
        self.scraper = scraper
        
    def __add_politician(politician):
        politicians = PoliticianUtils.read_politicians()
        politicians.append(politician)
        PoliticianUtils.__save_politicans(politicians)
        
    def __build_politician(user):
        return {
            "user_id": user["user_id"],
            "user_full_name": user["user_full_name"],
            "user_account_name": user["user_account_name"],
            "description": None,
            "last_modified": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
    def __fetch_politician(self, account_name):
        raw_user = self.scraper.users([account_name])[0]
        user = UserExtractor.extract_user(raw_user['data']['user']['result'])
        return PoliticianUtils.__build_politician(user)     
    
    def __check_if_politician_exists(account_name):
        politicians = PoliticianUtils.read_politicians()
        for politician in politicians:
            if politician["user_account_name"] == account_name:
                return True
        return False
    
    def set_politician_last_updated_to_now(politician):
        politician["last_modified"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    def save_politician(politician):
        politicians = PoliticianUtils.read_politicians()
        for i in range(len(politicians)):
            if politicians[i]["user_id"] == politician["user_id"]:
                politicians[i] = politician
                PoliticianUtils.save_politicans(politicians)
                return
        
    def save_politicans(politicians):
        with open(gl.POLITICIANS_FILE, 'w+', encoding="utf8") as file:
            json.dump({"politicians": politicians}, file, indent=4, ensure_ascii=False)
            
    def sort_by_last_modified(politicians):
        return sorted(politicians, key=lambda politician: politician['last_modified'])

    def read_politicians():
        with open(gl.POLITICIANS_FILE, 'r', encoding="utf8") as file:
            data = json.load(file)
            return data["politicians"]
        
    def fetch_and_add_politican(self, account_name):
        if PoliticianUtils.__check_if_politician_exists(account_name):
            print(f"Politician with account name {account_name} already exists.")
            return
        
        politician = self.__fetch_politician(account_name)
        PoliticianUtils.__add_politician(politician)
        
    def read_politcian_by_account_name(account_name):
        politicians = PoliticianUtils.read_politicians()
        for politician in politicians:
            if politician["user_account_name"] == account_name:
                return politician
        return None