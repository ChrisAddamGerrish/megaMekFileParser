import json
import csv
from misc.MTFAliasLists.mtf_alias_utils import mtf_weapon_alias
from misc.MTFAliasLists.equipment_alias import equipment_alias

with open('/Users/chris/Desktop/megamekparser/misc/static/all.json', 'r') as f:
    data = json.load(f)
ok_weapon_list = set()
bad_weapon_list = set()
for ids, mechData in data.items():
    for location, list in mechData['weapons'].items():
        if list:
            for i in list:
                i = i.replace("(r)", "")
                if equipment_alias.get(i):
                    continue

                good, bad = mtf_weapon_alias(i)
                if good:
                    ok_weapon_list.add(good)
                if bad:
                    bad_weapon_list.add(bad)

print(len(ok_weapon_list))
print(ok_weapon_list)
print(len(bad_weapon_list))
print(bad_weapon_list)

with open('/Users/chris/Desktop/megamekparser/misc/static/badweapons.csv', 'w') as csvfile:
    for i in bad_weapon_list:
        csvfile.write(f'{i},\n')
