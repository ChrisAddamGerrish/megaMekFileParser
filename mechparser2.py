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
        self.fluff_keys = ['history:', 'deployment:', 'capabilities:', 'overview:','capabilities:']

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

    def parse_locations(self, loc, file):
        eq = []
        line = file.readline()
        while line != "\n":
            if len(line) <1:
                break
            ln = line.lower().replace("\n", "")
            eq.append(ln)
            line = file.readline()
            continue
        self.equipment.update({loc: eq})

    def parse(self):
        with open(self.filepath, 'r') as f:
            self.mech.update({'file' : self.filepath.name})
            line = f.readline()
            self.mech.update({'version': self.get_item(line, 'r')})
            line = f.__next__()
            self.mech.update({'chassis': self.get_item(line, 'n')})
            line = f.__next__()
            self.mech.update({'model': self.get_item(line, 'n')})

            while line := f.readline():
                try:
                    ln = line.lower().replace("\n", "")

                    if 'deployment:' not in ln and 'capabilities:' not in ln and 'overview:' not in ln and 'history' not in ln:
                    #if ln not in self.fluff_keys:
                        if "armor" in ln:

                            if ln.startswith('armor'):
                                self.armor.update({"armor type": self.get_item(ln, 'r')})
                            else:
                                self.armor.update({self.get_item(ln, 'l'): self.get_item(ln, 'r')})

                        elif "weapons:" in ln:
                            scans: int = int(self.get_item(ln, 'r'))
                            for i in range(scans):
                                line = f.readline()
                                key_text = line.split(",")[1].replace("\n", "")
                                k = f'{key_text} {str(i + 1)}'
                                v = line.split(",")[0].replace("\n", "")
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
                            self.fluff.update({items[0].lower(): items[1].lower().replace("\n", "")})
                except IndexError:
                    pass

        self.mech.update({"armor": self.armor})
        self.mech.update({"weapons": self.weapons})
        self.mech.update({"equipment": self.equipment})
        self.mech.update({'fluff': self.fluff})
