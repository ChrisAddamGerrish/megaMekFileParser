import json
import keyring
import pymongo as pymongo

usr = "chrisDFA"
psw = keyring.get_password("mongoDB", usr)

uri = f"mongodb+srv://chrisDFA:{psw}@cluster0.h24miqs.mongodb.net/?retryWrites=true&w=majority"
print(uri)

client = pymongo.MongoClient(uri)

print(client.list_database_names())

db = client.DFA
collections = db.battlemech


with open('/Users/chris/Desktop/mmparser/all.json', 'r') as f:
    json_file = json.load(f)

for k,v in json_file.items():
    print(k)
    rec = collections.insert_one(v)
    print(rec)