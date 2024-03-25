from MegaMechFileParser.utils.base.equipment_locations import equip_config_lookup


def biped_armor_converter(config, armor_location_check):
    armor_key = equip_config_lookup[config][armor_location_check]
    return armor_key


def tripod_armor_converter(config, armor_location_check):
    armor_key = equip_config_lookup[config][armor_location_check]
    return armor_key


def quad_armor_converter(config, armor_location_check):
    armor_key = equip_config_lookup[config][armor_location_check]
    return armor_key


armor_config_lookup = {'biped': biped_armor_converter,
                       'biped omnimech': biped_armor_converter,
                       'lam': biped_armor_converter,
                       'tripod': tripod_armor_converter,
                       'tripod omnimech': tripod_armor_converter,
                       'tripod battlemech': tripod_armor_converter,
                       'quad omnimech': quad_armor_converter,
                       'quad': quad_armor_converter,
                       'quadvee': quad_armor_converter,
                       'quadvee omnimech': quad_armor_converter,
                       }
