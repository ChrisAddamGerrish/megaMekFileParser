from collections import OrderedDict
from typing import Optional
import pathlib
import copy
from MegaMechFileParser.utils.armor_config import armor_config_lookup
from MegaMechFileParser.utils.equipment_locations import equip_config_lookup
from MegaMechFileParser.utils.weapon_locations import weapon_location_lookup


class MechParser:
    def __init__(self, mtffilepath):

        self.filepath: pathlib.Path = mtffilepath
        self.armor = {}
        self.weapons = {}
        self.equipment = {}
        self.fluff = {}
        self.fluff_keys = ['history', 'deployment', 'capabilities', 'overview', 'capabilities', 'manufacturer',
                           'systemmanufacturer', 'primaryfactory', 'systemmode']
        self.config = self.get_config()
        self.systemmanufacturer = {}

        self.mech = OrderedDict()

        if locs := equip_config_lookup.get(self.config):
            self.mech_locs = [loc for _, loc in locs.items()]

    @staticmethod
    def get_item(line: str, direction: Optional[str] = 'r') -> Optional[str]:
        match direction:
            case 'r':
                out = line.split(":")[1].rstrip("\n")
                return out
            case 'l':
                out = line.split(":")[0].rstrip("\n")
                return out
            case 'n':
                out = line.rstrip("\n")
                return out

    def parse_locations(self, equipment_location, file):
        equipment = []
        line = file.readline()
        while line != "\n":
            if len(line) < 1:
                break
            ln = line.lower().rstrip("\n")
            if ln == '-empty-':
                ln = None
            equipment.append(ln)
            line = file.readline()
            continue
        self.equipment.update({equipment_location.strip().lower(): equipment})

    def get_config(self):

        try:
            with open(file=self.filepath, encoding='utf8', errors='ignore', mode='r') as f:
                while line := f.readline():
                    if 'config:' in line.lower():
                        config = line.split(":")[1].rstrip("\n").lower()
        except Exception as e:
            config = f'error!\n {e}'

        return config

    def parse(self):
        with open(file=self.filepath, encoding='utf8', errors='ignore', mode='r') as f:
            self.mech.update({'file': self.filepath.name})
            line = f.readline()
            self.mech.update({'version': self.get_item(line, 'r')})
            line = f.__next__()
            self.mech.update({'chassis': self.get_item(line, 'n').strip().lower()})
            line = f.__next__()
            self.mech.update({'model': self.get_item(line, 'n').strip().lower()})

            while line := f.readline():

                try:
                    ln = line.lower().replace("\n", "")

                    if ln == '':
                        continue

                    row_check = None
                    for row in self.fluff_keys:
                        c = ln.split(":")[0]
                        if row in c:
                            row_check = True
                            break

                    if not row_check:

                        if "armor" in ln:

                            if ln.startswith('armor'):
                                self.armor.update({"type": self.get_item(ln, 'r')})
                            else:
                                armor_location, armor_value = (self.get_item(ln, 'l'), self.get_item(ln, 'r'))
                                armor_location_check = armor_location.split(' ')
                                armor_key = armor_config_lookup[self.config](self.config, armor_location_check[0])
                                if armor_key:
                                    self.armor.update({armor_key: armor_value})

                        elif "weapons:" in ln:
                            scans: int = int(self.get_item(ln, 'r'))

                            weapons_locations = copy.deepcopy(weapon_location_lookup[self.config])

                            for i in range(scans):
                                line = f.readline()
                                weapon_key_text = line.split(",")[1].rstrip("\n")
                                weapon_location = weapon_key_text.strip().lower()
                                weapon = line.split(",")[0].rstrip("\n").lower()
                                if '(r)' in weapon:
                                    weapon = weapon.replace('(r)', "").strip()
                                try:
                                    tmp_wpn_split = weapon.split(" ")
                                    wpn_count = tmp_wpn_split[0]
                                    wpn = " ".join(tmp_wpn_split[1:])
                                    for n in range(int(wpn_count)):
                                        weapons_locations[weapon_location].append(wpn)
                                except ValueError:
                                    weapons_locations[weapon_location].append(weapon)

                            for weapon_location, weapon in weapons_locations.items():
                                if len(weapon) == 0:
                                    if '(r)' in weapon_location or 'none' in weapon_location:
                                        continue
                                    else:
                                        self.weapons.update({weapon_location: None})
                                else:
                                    self.weapons.update({weapon_location: weapon})

                        elif ln.replace(":", "") in self.mech_locs:
                            self.parse_locations(ln, file=f)

                        else:
                            items = [i for i in line.split(":") if i != ""]
                            if len(items) > 1:
                                self.mech.update({items[0].lower(): items[1].lower().rstrip("\n")})
                    else:
                        if not line.split(":")[0] == 'systemmanufacturer':
                            items = [i for i in line.split(":") if i != ""]
                            if len(items) > 1:
                                self.fluff.update({items[0].lower(): items[1].rstrip("\n")})
                        else:
                            items = [i for i in line.split(":") if i != ""]
                            self.systemmanufacturer.update({items[1].lower(): items[2].rstrip("\n")})

                except IndexError:
                    print('bad')

        self.fluff.update({'systemmanufacturer': self.systemmanufacturer})
        self.mech.update({"armor": self.armor})
        self.mech.update({"weapons": self.weapons})
        self.mech.update({"equipment": self.equipment})
        self.mech.update({'fluff': self.fluff})
