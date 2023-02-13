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
            self.mech.update({'file' : self.filepath.name})
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


                            #left_arm = {'left arm' : []}
                            left_arm = []
                            right_arm = []
                            left_torso = []
                            right_torso = []
                            center_torso = []
                            head = []
                            left_leg = []
                            right_leg = []
                            weapon_location_lists = [left_arm,
                                                    right_arm,
                                                    left_torso,
                                                    right_torso,
                                                    center_torso,
                                                    head,
                                                    left_leg,
                                                    right_leg,]
                            for i in range(scans):
                                line = f.readline()
                                key_text = line.split(",")[1].replace("\n", "")
                                k = key_text.strip().lower()
                                v = line.split(",")[0].replace("\n", "").strip().lower()

                                match k:
                                    case 'left arm':
                                        left_arm.append(v)
                                    case 'right arm':
                                        right_arm.append(v)
                                    case 'left torso':
                                        left_torso.append(v)
                                    case 'right torso':
                                        right_torso.append(v)
                                    case 'center torso':
                                        center_torso.append(v)
                                    case 'head':
                                        head.append(v)
                                    case 'left leg':
                                        left_leg.append(v)
                                    case 'right leg':
                                        right_leg.append(v)

                            for idx, location in enumerate(self.mech_locs):
                                if weapon_location_lists[idx].__len__() == 0:
                                    self.weapons.update({location : None})
                                else:
                                    self.weapons.update({location : weapon_location_lists[idx] })

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
                    pass

        self.mech.update({"armor": self.armor})
        self.mech.update({"weapons": self.weapons})
        self.mech.update({"equipment": self.equipment})
        self.mech.update({'fluff': self.fluff})
