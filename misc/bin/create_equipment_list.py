import json
import csv

with open('../static/all.json', 'r') as f:
    data = json.load(f)
weapon_list = set()
for ids, mechData in data.items():
    for location, list in mechData['equipment'].items():
        if list:
            for i in list:
                if i:
                    weapon_list.add(i)

new = [i for i in weapon_list]
final = sorted(new)


with open('../static/equipment.csv', 'w') as csvfile:
    for i in final:
        csvfile.write(f'{i},\n')
