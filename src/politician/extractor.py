class UserExtractor:
    
    def extract_user(raw_user):
        return {
            "user_id": raw_user['rest_id'],
            "user_full_name": raw_user['legacy']['name'],
            "user_account_name": raw_user['legacy']['screen_name'],
            "profile_image_url": raw_user['legacy']['profile_image_url_https'].replace("_normal.jpg", "_400x400.jpg")
        }
    
    def extract_mentioned_user(mention):
        return {
            "user_id": mention['id_str'],
            "user_full_name": mention['name'],
            "user_account_name": mention['screen_name'],
        }
        
    def extract_mentioned_users(legacy):
        return [UserExtractor.extract_mentioned_user(mention) for mention in legacy['entities']['user_mentions']]