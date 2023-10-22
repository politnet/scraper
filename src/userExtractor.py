import globals as gl
import json
import datetime

def extractUser(user):
    return {
        "user_id": user['rest_id'],
        "user_full_name": user['legacy']['name'],
        "user_account_name": user['legacy']['screen_name'],
    }
    
def extractMentionedUser(mention):
    return {
        "user_id": mention['id_str'],
        "user_full_name": mention['name'],
        "user_account_name": mention['screen_name'],
    }

def extractUserMentions(legacy):
    return [extractMentionedUser(mention) for mention in legacy['entities']['user_mentions']]

def readPoliticians():
    completeUsers = []
    incompleteUsers = []
    with open(gl.POLITICIANS_FILE, 'r', encoding="utf8") as file:
        for policitian in json.load(file)["politicians"]:
            if policitian["user_id"] is None:
                incompleteUsers.append(policitian)
            else:
                completeUsers.append(policitian)
    return completeUsers, incompleteUsers

def savePoliticians(politicians):
    with open(gl.POLITICIANS_FILE, 'w+', encoding="utf8") as file:
        json.dump({"politicians": politicians}, file, indent=4, ensure_ascii=False)
        
def getUsers(scraper, users):
    if len(users) == 0:
        return []
    
    screenNames = [user["user_account_name"] for user in users]
    rawUsers = scraper.users(screenNames)
    for i, rawUser in enumerate(rawUsers):
        user = extractUser(rawUser['data']['user']['result'])
        users[i]["user_id"] = user["user_id"]
        users[i]["user_full_name"] = user["user_full_name"]
        users[i]["last_modified"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return users

def updateAndGetPoliticians(scraper):
    completeUsers, incompleteUsers = readPoliticians()
    users = getUsers(scraper, incompleteUsers)
    allPoliticians = completeUsers + users
    savePoliticians(allPoliticians)
    return allPoliticians

def setPoliticianLastUpdatedToNow(politician):
    politician["last_modified"] = datetime.datetime.now(datetime.timezone.utc).isoformat()