import json
import pymongo as pymongo
import yaml

with open('../../config.yaml', 'r') as file:
    config = yaml.safe_load(file)

uri = config['uri']

client = pymongo.MongoClient(uri)

db = client.DFA
collections = db.battlemech

collections.delete_many({})

with open('../static/all2.json', 'r') as f:
    json_file = json.load(f)


rec = {collections.insert_one(v) for k,v in json_file.items()}

print(rec)