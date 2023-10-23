class UserExtractor:
    
    def extract_user(raw_user):
        return {
            "user_id": raw_user['rest_id'],
            "user_full_name": raw_user['legacy']['name'],
            "user_account_name": raw_user['legacy']['screen_name'],
        }
    
    def extract_mentioned_user(mention):
        return {
            "user_id": mention['id_str'],
            "user_full_name": mention['name'],
            "user_account_name": mention['screen_name'],
        }