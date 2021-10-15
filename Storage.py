import pymongo

from pymongo import database

from twitterapi import TwitterController

# initialise MongoDB
client = pymongo.MongoClient(
    'mongodb+srv://bot:bot@twitterbot.rsemx.mongodb.net/test')

db = client['twitter']

accounts = db['accounts']
followers = db['followers']
following = db['following']

            

        
# get following list from twitter API
def get_following_from_twitter(handle):
    account = TwitterController(handle)
    following_list = []
    for user in account.get_following_list():
        following_list.append(user.screen_name)
    return following_list

# get following list from database
def get_following_from_db(handle):
    account = get_account_from_db(handle)
    # retrieve following list of account from db, assigns None to var if not present
    following_from_db = account.get('following')
    return following_from_db
    
# get account from database
def get_account_from_db(handle):
    # get following list of the account from database, None if not present
    account = None
    for temp in accounts.find({'handle' : handle}):
        account = temp

    # if account does not exist, create new account
    if account is None:
        account = {
            'handle' : handle,
            'following' : {}
        }
        add_one_account(account)
        print(f"Account does not exist in the database, creating Account for @{handle}")
    
    return account

# add one account into db.accounts
def add_one_account(account):
    accounts.insert_one(account)

# update the following list of the user
def update_following(handle, following_from_twitter):
    account = get_account_from_db(handle)
    accounts.update_one({'handle' : handle}, {
        '$set' :
            {'following' : following_from_twitter}
    })
    print(f"Successfully updated {handle}")
    
# returns a list of twitter minus db
def get_difference_in_following(following_from_db, following_from_twitter):
    difference = set(following_from_twitter).difference(following_from_db)
    return list(difference)
    
# update the database with the following list of the user
def check_for_new_following(handle):
    # new followers container
    new_following = []
    # get following list of the account from twitter
    following_from_twitter = get_following_from_twitter(handle)

    # get following list of the account from db
    following_from_db = get_following_from_db(handle)

    # compare db following to twitter following
    if frozenset(following_from_db) == frozenset(following_from_twitter):
        print('No new following found!')
        return new_following
    else:
        # get new following 
        new_following = get_difference_in_following(
            following_from_db, following_from_twitter
        )

        # update database with updated following from twitter
        update_following(handle, following_from_twitter)

        # system reply
        print(f"Here are the new following for @{handle}:")
        print(new_following)

        return new_following