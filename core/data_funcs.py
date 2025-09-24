import json
import os

def get_row_by_id(data, id, id_field_name):
    for item in data:
        if item[id_field_name] == id:
            return item
        
    return None

def get_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def get_survivor_data():
    path = "data/survivors.json"
    data = get_data(path)

    survivor_id = 1
    survivors = []

    for row in data:
        survivors.append({"survivor_id": survivor_id, "survivor_name": row["survivor_name"],
                          "survivor_description": row["survivor_description"],
                          "survivor_icon": row["survivor_icon"]})
        survivor_id += 1

    return survivors


def get_killer_data():
    path = "data/killers.json"
    data = get_data(path)

    killer_id = 1
    killers = []
    addon_id = 1

    for row in data:
        killer = {"killer_id": killer_id,
                  "killer_name": row["killer_name"],
                  "killer_description": row["killer_description"],
                  "killer_icon": row["killer_icon"]}

        killer_id += 1

        addons = []
        for addon in row["killer_addons"]:
            addons.append({"killer_addon_id": addon_id,
                           "killer_addon_name": addon["killer_addon_name"],
                           "killer_addon_rarity": addon["killer_addon_rarity"],
                           "killer_addon_icon": addon["killer_addon_icon"]})
            addon_id += 1

        killer["killer_addons"] = addons
        killers.append(killer)

    return killers

def get_perks_data(character_type):
    path = "data/perks.json"
    data = get_data(path)

    perk_id = 1
    perks = []

    for row in data[f'{character_type}_perks']:
        perks.append({f'{character_type}_perk_id': perk_id,
                      f'{character_type}_perk_name': row[f'{character_type}_perk_name'],
                      f'{character_type}_owner_name': row[f'{character_type}_owner_name'],
                      f'{character_type}_perk_icon': row[f'{character_type}_perk_icon']
                      })
        perk_id += 1

    return perks

def get_items_data():
    path = 'data/items.json'
    data = get_data(path)
    
    item_id = 1
    items = []
    addon_id = 1
    addons = []
    
    for row in data:
        family_name = row["survivor_item_family"]
        
        for item in row["survivor_items"]:
            items.append({"survivor_item_id": item_id,
                          "survivor_item_name": item["survivor_item_name"],
                          "survivor_item_rarity": item["survivor_item_rarity"],
                          "survivor_item_icon": item["survivor_item_icon"],
                          "survivor_item_family": family_name})
            item_id += 1
            
        for addon in row["survivor_addons"]:
            addons.append({"survivor_addon_id": addon_id,
                           "survivor_addon_name": addon["survivor_addon_name"],
                           "survivor_addon_rarity": addon["survivor_addon_rarity"],
                           "survivor_addon_icon": addon["survivor_addon_icon"],
                           "survivor_item_family": family_name})
            addon_id += 1
            
    return {"items": items, "addons": addons}


def get_offerings_data():
    path = 'data/offerings.json'
    data = get_data(path)
    killer_offering_id = 1
    killer_offerings = []
    survivor_offering_id = 1
    survivor_offerings = []
    
    for row in data:
        if row["character_type"] == "Killer" or row["character_type"] == "All":
            for offering in row["offerings"]:
                killer_offerings.append({"offering_id": killer_offering_id,
                                         "offering_name": offering["offering_name"],
                                         "offering_rarity": offering["offering_rarity"],
                                         "offering_icon": offering["offering_icon"]})
                killer_offering_id += 1
        if row["character_type"] == "Survivor" or row["character_type"] == "All":
            for offering in row["offerings"]:
                survivor_offerings.append({"offering_id": survivor_offering_id,
                                           "offering_name": offering["offering_name"],
                                           "offering_rarity": offering["offering_rarity"],
                                           "offering_icon": offering["offering_icon"]})
                survivor_offering_id += 1

    return {"killer_offerings": killer_offerings, "survivor_offerings": survivor_offerings}
