class UserExtractor:
    
    def extract_user(raw_user):
        return {
            "user_id": raw_user['rest_id'],
            "user_full_name": raw_user['legacy']['name'],
            "user_account_name": raw_user['legacy']['screen_name'],
        }