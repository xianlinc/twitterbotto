import pymongo
import re

from twitterapi import TwitterController

# initialise MongoDB
client = pymongo.MongoClient(
    'mongodb+srv://bot:bot@twitterbot.rsemx.mongodb.net/test')

db = client['twitter']

accounts = db['accounts']
followers = db['followers']
following = db['following']
new_following_db = db['new_following']

def escape_markdown(text):
    # Use {} and reverse markdown carefully.
    parse = re.sub(r"([_*\[\]()~`>\#\+\-=|\.!])", r"\\\1", text)
    reparse = re.sub(r"\\\\([_*\[\]()~`>\#\+\-=|\.!])", r"\1", parse)
    return reparse 

def link_markdown(handle):
    return f"[@{escape_markdown(handle)}](twitter.com/{handle}/)"

# if account exists, return true, else return false
def account_exists(handle):
    account = None
    for temp in accounts.find({'handle': handle}):
        account = temp

    # if account exists, return true, else return false
    return account is not None


# add an account + following list into the database from twitter
def add_account(handle):
    following_from_twitter = get_following_from_twitter(handle)
    account = {
        'handle': handle,
        'following': following_from_twitter
    }
    add_one_account(account)
    print(f"We are successfully stalking {link_markdown(handle)}")


# get a list of accounts in the accounts database
def get_account_list():
    account_list = []
    for account in accounts.find({}):
        handle = account.get('handle')
        account_list.append(handle)
    # print("Here is the list of accounts being stalked:")
    # print(account_list)
    return account_list


# get following list from twitter API
# returns a list of strings
def get_following_from_twitter(handle):
    account = TwitterController(handle)
    following_list = []
    for user in account.get_following_list():
        following_list.append(user.screen_name)
    return following_list


# get following list from database
# returns a list of strings
def get_following_from_db(handle):
    account = get_account_from_db(handle)
    # retrieve following list of account from db,
    #   assigns None to var if not present
    following_from_db = account.get('following')
    return following_from_db


# get account from database
def get_account_from_db(handle):
    # get following list of the account from database, None if not present
    account = None
    for temp in accounts.find({'handle': handle}):
        account = temp

    # if account does not exist, create new account
    if account is None:
        account = {
            'handle': handle,
            'following': {}
        }
        add_one_account(account)
        print("Account does not exist in the database," +
              f" creating Account for {link_markdown(handle)}")

    return account


# add one account into db.accounts
def add_one_account(account):
    accounts.insert_one(account)


# update the following list of the user
def update_following(handle, following_from_twitter, collection):
    get_account_from_db(handle)
    collection.update_one({'handle': handle}, {
        '$set':
            {'following': following_from_twitter}
    })
    # print(f"Successfully updated {handle}")


# returns a list of twitter minus db
def get_difference_in_following(following_from_db, following_from_twitter):
    difference = set(following_from_twitter).difference(following_from_db)
    return list(difference)


# update the database with the following list of the user
def check_for_new_following(handle):
    # new followers container
    new_following = []

    # if account doesnt exist, update database with account and exit function
    if (not account_exists(handle)):
        print(f"Account is not in the database\!" +
              f" Creating account for {link_markdown(handle)}")
        add_account(handle)
        return new_following

    # get following list of the account from twitter
    following_from_twitter = get_following_from_twitter(handle)

    # get following list of the account from db
    following_from_db = get_following_from_db(handle)

    # get the following that are in twitter but not db
    new_following = get_difference_in_following(
        following_from_db, following_from_twitter
    )
    
    # if no difference in following, no new followers, exit function
    if (new_following == []):
        # print(f'No new following found for {link_markdown(handle)}\!')
        return new_following

    # add to new followers database
    update_following(handle, new_following, new_following_db)

    # update database with updated following from twitter
    update_following(handle, following_from_twitter, accounts)

    # system reply
    print(f"Here are the new following for {link_markdown(handle)}:")
    str_builder = ""
    for str in new_following:
        str_builder += f"{link_markdown(str)}\n"
    print(str_builder.strip())


    return new_following


# check for new following for all stalked accounts in the database
def check_all():
    # get a list of handles of stalked accounts
    handle_list = get_account_list()

    # for each account, check for new following
    for handle in handle_list:
        check_for_new_following(handle)


# get mutual followers of two accounts
def mutual(handle_1, handle_2):
    # initalise TwitterControllers for both handles
    handle_1_controller = TwitterController(handle_1)
    handle_2_controller = TwitterController(handle_2)

    # get follower list for both handles
    handle_1_followers = handle_1_controller.get_followers()
    handle_2_followers = handle_2_controller.get_followers()

    # find mutual followers
    mutual_followers = set(handle_1_followers).intersection(set(handle_2_followers))

    result = []
    # put the handles of mutual followers in a list
    for user in mutual_followers:
        result.append(user.screen_name)
    print(result)

# gets a list of following of all following in db that contains substring "dao"
# returns a list of strings
def get_dao_list():
    db_contains("dao")

# gets following that contains input string TODO
def db_contains(str):
    print(f"Here are the handles containing {str} found in the database:")
    handle_list = get_account_list()
    found = False
    for handle in handle_list:
        str_list = []
        for user in get_following_from_db(handle):
            if str in user.lower():
                found = True
                user_markdown = link_markdown(user)
                str_list.append(user_markdown)
        
        if str_list != []:
            print(f"\nMatches found from {link_markdown(handle)}:")
            print(*str_list, sep='\n')
    if not found:
        print(f"No handles containing \"{str}\" can be found")
