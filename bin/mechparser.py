import pathlib
from typing import Optional
from collections import OrderedDict



class MechParser():
    def __init__(self, mtffilepath):
        self.filepath: pathlib.Path = mtffilepath

        self.mech = OrderedDict()
        self.armor = {}
        self.weapons = {}
        self.equipment = {}
        self.fluff = {}
        self.mech_locs = ["left arm", "right arm", "left torso", "right torso", "center torso", "head", "left leg",
                          "right leg"]
        self.fluff_keys = ['history:', 'deployment:', 'capabilities:', 'overview:', 'capabilities:']

    def get_item(self, line: str, direction: Optional[str] = 'r') -> Optional[str]:
        match direction:
            case 'r':
                out = line.split(":")[1].replace("\n", "")
                return out
            case 'l':
                out = line.split(":")[0].replace("\n", "")
                return out
            case 'n':
                out = line.replace("\n", "")
                return out

    def parse_locations(self, equipment_location, file):
        equipment = []
        line = file.readline()
        while line != "\n":
            if len(line) <1:
                break
            ln = line.lower().replace("\n", "")
            if ln == '-empty-':
                ln = None
            equipment.append(ln)
            line = file.readline()
            continue
        self.equipment.update({equipment_location.strip().lower(): equipment})

    def parse(self):
        with open(self.filepath, 'r') as f:
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

                    if 'deployment:' not in ln and 'capabilities:' not in ln and 'overview:' not in ln and 'history' not in ln:
                    #if ln not in self.fluff_keys:
                        if "armor" in ln:

                            if ln.startswith('armor'):
                                self.armor.update({"type": self.get_item(ln, 'r')})
                            else:
                                armor_location, armor_value = (self.get_item(ln, 'l'), self.get_item(ln, 'r'))
                                armor_location_check = armor_location.split(' ')
                                armor_key = None
                                match armor_location_check[0]:
                                    case 'la':
                                        armor_key = 'left arm'
                                    case 'ra':
                                        armor_key = 'right arm'
                                    case 'lt':
                                        armor_key = 'left torso'
                                    case 'rt':
                                        armor_key = 'right torso'
                                    case 'ct':
                                        armor_key = 'center torso'
                                    case 'hd':
                                        armor_key = 'head'
                                    case 'll':
                                        armor_key = 'left left'
                                    case 'rl':
                                        armor_key = 'right leg'
                                    case 'rtl':
                                        armor_key = 'rear left torso'
                                    case 'rtr':
                                        armor_key = 'rear right torso'
                                    case 'rtc':
                                        armor_key = 'rear center torso'

                                self.armor.update({armor_key: armor_value})

                        elif "weapons:" in ln:
                            scans: int = int(self.get_item(ln, 'r'))

                            weapons_locations = {
                                                'left arm': [],
                                                'left arm (r)': [],
                                                'right arm': [],
                                                'right arm (r)': [],
                                                'left torso': [],
                                                'left torso (r)': [],
                                                'right torso': [],
                                                'right torso (r)': [],
                                                'center torso': [],
                                                'center torso (r)': [],
                                                'head': [],
                                                'head (r)': [],
                                                'left leg': [],
                                                'left leg (r)': [],
                                                'right leg': [],
                                                'right leg (r)': [],
                                                'none': [],
                                                }

                            for i in range(scans):
                                line = f.readline()
                                key_text = line.split(",")[1].replace("\n", "")
                                k = key_text.strip().lower()

                                if 'front' in k:
                                    k = k.replace('front','').strip()
                                elif'rear' in k:
                                    k = f"{k.replace('rear','').strip()} (r)"

                                v = line.split(",")[0].replace("\n", "").strip().lower()

                                if ('(r)') in v:
                                    v = v.replace('(r)',"").strip()
                                try:
                                    tmp_wpn_split = v.split(" ")
                                    wpn_count = tmp_wpn_split[0]
                                    wpn = " ".join(tmp_wpn_split[1:])
                                    for n in range(int(wpn_count)):
                                        weapons_locations[k].append(wpn)
                                except Exception as e:
                                    weapons_locations[k].append(v)

                            for k, v in weapons_locations.items():
                                if len(v) == 0:
                                    if '(r)' in k or 'none' in k:
                                        continue
                                    else:
                                        self.weapons.update({k: None})
                                else:
                                    self.weapons.update({k: v})


                        elif ln.replace(":", "") in self.mech_locs:
                            self.parse_locations(ln, file=f)

                        else:
                            items = [i for i in line.split(":") if i != ""]
                            if len(items) > 1:
                                self.mech.update({items[0].lower(): items[1].lower().replace("\n", "")})
                    else:
                        items = [i for i in line.split(":") if i != ""]
                        if len(items) > 1:
                            self.fluff.update({items[0].lower(): items[1].replace("\n", "")})
                except IndexError:
                    print('bad')

        self.mech.update({"armor": self.armor})
        self.mech.update({"weapons": self.weapons})
        self.mech.update({"equipment": self.equipment})
        self.mech.update({'fluff': self.fluff})
