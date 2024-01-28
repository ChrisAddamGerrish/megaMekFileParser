import csv

import pymongo
import yaml

with open('../../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
uri = config['uri']

client = pymongo.MongoClient(uri)

db = client.DFA
collections = db.battlemech

mechs = []
weapons = set()
for mech in collections.find({}):
    mechs.append(mech)

for i in mechs:
    for k, v in i['weapons'].items():
        if v:
            weapons.update(v)

with open(file='/Users/chris/Desktop/mmparser/static/wpnslist.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter='|', dialect='excel')
    writer.writerow(['weapons'])
    for i in weapons:
        writer.writerow([i])
