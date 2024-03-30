import io
from collections import OrderedDict
from typing import Optional
import pathlib
import copy
from megamekfileparser.utils.armor_config import armor_config_lookup
from megamekfileparser.utils.equipment_locations import equip_config_lookup
from megamekfileparser.utils.weapon_locations import weapon_location_lookup


class MekParser:
    def __init__(self, mtffilepath: Optional[pathlib.Path] = None):

        self.filepath: pathlib.Path = mtffilepath
        self.armor = {}
        self.weapons = {}
        self.equipment = {}
        self.fluff = {}
        self.fluff_keys = ['history', 'deployment', 'capabilities', 'overview', 'capabilities', 'manufacturer',
                           'systemmanufacturer', 'primaryfactory', 'systemmode']
        self.config = self.__get_config()
        self.systemmanufacturer = {}

        self.mech = OrderedDict()
        self.mech_locs = None

    def __split_key_value_pair(self, line: str, direction: Optional[str] = 'r') -> Optional[str]:
        """
        Splits the current line into a key value pair. The direction argument is used to determine which side of the :
        is used to set the key.
        :param line: Text from the file to be parsed
        :param direction: r = right side of : to be set as key; l = left side of : to be used as key; \n to move on to
        next line
        :return: A list of text, where the first value is the key and subsequent items are the values.
        """
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

    def __get_generic_item(self, line: str) -> None:
        """
        Parses over the easy lines. Builds key value pairs based on the current line read into the function.
        :param line: Current line of the file.
        :return: None, class object is updated directly.
        """
        items = [i for i in line.split(":") if i != ""]
        if len(items) > 1:
            self.mech.update({items[0].lower(): items[1].lower().rstrip("\n")})

    def __get_config(self) -> str:
        """
        Finds the config line in the file being parsed to be used in the configue setup step.
        :return: a string to be used in the config lookup function.
        """
        try:
            with open(file=self.filepath, encoding='utf8', errors='ignore', mode='r') as f:
                while line := f.readline():
                    if 'config:' in line.lower():
                        config = line.split(":")[1].rstrip("\n").lower()
        except Exception as e:
            config = f'error!\n {e}'

        return config

    def __file_path_check(self) -> None:
        """
        Checks to make sure the file path object passed into the parser exists and is a file.
        :return: None
        """
        if self.filepath is None:
            raise Exception('No filepath provided!')
        elif not isinstance(self.filepath, pathlib.Path):
            raise TypeError(f'{self.filepath} is not a valid file path!')
        elif not pathlib.Path(self.filepath).is_file():
            raise TypeError(f'{self.filepath} does not exist')

    def __parse_armor(self, line: str) -> None:
        """
        Function to parse armor lines in the fie. This triggered  after the if statement detects the word "armor" in the
        text of the current line in the main parse function. Each row is then handled accordingly.
        :param line: current text of the current line in the file
        :return: None, class object is updated directly.
        """
        if line.startswith('armor'):
            self.armor.update({"type": self.__split_key_value_pair(line, 'r')})
        else:
            armor_location, armor_value = (self.__split_key_value_pair(line, 'l'), self.__split_key_value_pair(line, 'r'))
            armor_location_check = armor_location.split(' ')
            armor_key = armor_config_lookup[self.config](self.config, armor_location_check[0])
            if armor_key:
                self.armor.update({armor_key: armor_value})

    def __parse_weapons(self, file, line: str) -> None:
        """
        Weapon sequence contains the most checks. Control is handled over to the function from the main parser
        to make sure items are assigned to the correct location. Since the number of weapons are indicated on the first
        line of the file where weapons are declared, this step will iterate through the file for the total length
        indicated, and then will return control back to the main parse function to continue iteration.
        :param file: current file parsed
        :param line: current line of file parsed
        :return: None, class object is updated directly.
        """
        scans: int = int(self.__split_key_value_pair(line, 'r'))
        weapons_locations = copy.deepcopy(weapon_location_lookup[self.config])
        for i in range(scans):
            line = file.readline()
            weapon_key_text = line.split(",")[1].rstrip("\n")
            weapon_location = weapon_key_text.strip().lower()
            weapon = line.split(",")[0].rstrip("\n").lower()
            # if '(r)' in weapon:
            # weapon = weapon.replace('(r)', "").strip()
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

    def __parse_locations(self, equipment_location: str, file) -> None:
        """
        Build sub dictionary for an arbitrary locations. After a location is detected by the parser, the parser creates a
        dictionary with the locations names, and adds values to that dictionary for each subsequent line in the file.
        final results are added to the equipment dictionary in the end.
        :param equipment_location: Location string at top of sequence.
        :param file: file object to be iterated over. File will be read from current row in parser sequence.
        :return None: Items appended to self in the class.
        """
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

    def __handle_fluff_and_systemmanufacturer(self, line: str) -> None:
        """
        This function handles misc information that is not needed for gameplay, but helps with narrative when needed.
        :param line: Text of the current line of the file being parser
        :return: None, class object is updated directly.
        """
        if not line.split(":")[0] == 'systemmanufacturer':
            items = [i for i in line.split(":") if i != ""]
            if len(items) > 1:
                self.fluff.update({items[0].lower(): items[1].rstrip("\n")})
        else:
            items = [i for i in line.split(":") if i != ""]
            self.systemmanufacturer.update({items[1].lower(): items[2].rstrip("\n")})

    def parse(self):
        self.__file_path_check()

        with open(file=self.filepath, encoding='utf8', errors='ignore', mode='r') as f:

            if locs := equip_config_lookup.get(self.config):
                self.mech_locs = [loc for _, loc in locs.items()]
            else:
                raise ValueError('MegaMek Object Configuration not recognized!')

            # All megamek files should start of with these 4 items {file,version,chassis,model}
            self.mech.update({'file': self.filepath.name})
            line = f.readline()
            self.mech.update({'version': self.__split_key_value_pair(line, 'r')})
            line = f.__next__()
            self.mech.update({'chassis': self.__split_key_value_pair(line, 'n').strip().lower()})
            line = f.__next__()
            self.mech.update({'model': self.__split_key_value_pair(line, 'n').strip().lower()})

            while line := f.readline():

                try:
                    ln = line.lower().replace("\n", "")

                    if ln == '':
                        continue

                    # Check to see if current row in file is fluff / system manufacturer. If false, the parser will
                    # continue. These items should always show up at EOF, but necessary to check first based on current
                    # flow of the script. Possible refactor in the future?
                    row_check = None
                    for row in self.fluff_keys:
                        fluff_items = ln.split(":")[0]
                        if row in fluff_items:
                            row_check = True
                            break

                    if not row_check:

                        if "armor" in ln:
                            self.__parse_armor(line=ln)

                        elif "weapons:" in ln:
                            self.__parse_weapons(file=f, line=ln)

                        elif ln.replace(":", "") in self.mech_locs:
                            self.__parse_locations(equipment_location=ln, file=f)

                        else:
                            self.__get_generic_item(line)
                    else:
                        self.__handle_fluff_and_systemmanufacturer(line)

                except IndexError:
                    print(f'Could not successfully read line {line} of file {self.filepath}!')

        # Build final document with all parsed items.
        self.mech.update({"armor": self.armor})
        self.mech.update({"weapons": self.weapons})
        self.mech.update({"equipment": self.equipment})
        self.fluff.update({'systemmanufacturer': self.systemmanufacturer})
        self.mech.update({'fluff': self.fluff})


