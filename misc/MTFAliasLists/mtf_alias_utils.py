from misc.MTFAliasLists.weapon_alias import weapon_alias
from misc.MTFAliasLists.equipment_alias import equipment_alias

def mtf_weapon_alias(item):

    lookup = item.replace(" ", "")

    if weapon_alias.get(lookup):
        ok_item = lookup
        bad_item = None
    else:
        bad_item = lookup
        ok_item = None

    return ok_item, bad_item


