from megamekfileparser.utils.MTFAliasLists import masterList


def standardize_mta_item_name(item: str) -> str:
    item = item.replace(' ','')
    if new_item := masterList.mta_master_list.get(item):
        return new_item

    return item
