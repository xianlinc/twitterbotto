import pymongo

client = pymongo.MongoClient('mongodb+srv://bot:bot@twitterbot.rsemx.mongodb.net/test')

db = client['twitter']

accounts = db['accounts']
followers = db['followers']
following = db['following']

results = accounts.find({})
for result in results:
    print(result)


