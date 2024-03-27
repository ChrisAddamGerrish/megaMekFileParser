import json
import pymongo as pymongo
import yaml
import time

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)

uri = config['uri']

client = pymongo.MongoClient(uri)

db = client.DFA
collections = db.battlemech

collections.delete_many({})

with open('../static/all.json', 'r') as f:
    json_file = json.load(f)

toLoad = [v for _, v in json_file.items()]

strt = time.time()
rec = collections.insert_many(toLoad)
end = time.time()

print(end - strt)
