import json
import csv
from misc.MTFAliasLists.mtf_alias_utils import mtf_weapon_alias, mtf_equipment_alias

with open('../static/all.json', 'r') as f:
    data = json.load(f)
ok_weapon_list = set()
bad_weapon_list = set()
ok_equipment_list = set()
bad_equipment_list = set()
for ids, mechData in data.items():
    for location, list in mechData['equipment'].items():
        for item in list:
            if item:
                ok_equipment, bad_equipment = mtf_equipment_alias(item)
                ok_weapon, bad_weapon = mtf_weapon_alias(item)

                if ok_equipment:
                    ok_equipment_list.add(ok_equipment)
                elif bad_weapon:
                    bad_equipment_list.add(bad_equipment)
                elif ok_weapon:
                    ok_weapon_list.add(ok_weapon)
                elif bad_weapon:
                    bad_weapon_list.add(bad_weapon)

print(len(ok_weapon_list))
print(ok_weapon_list)
print(len(bad_weapon_list))
print(bad_weapon_list)

with open('../static/badweapons.csv', 'w') as csvfile:
    for i in bad_weapon_list:
        csvfile.write(f'{i},\n')
