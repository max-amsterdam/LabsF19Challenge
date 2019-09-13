import json

def get_building_id_from_name(building_name):
    building_info_txt = open('building_info.txt')
    building_info_json = json.load(building_info_txt)

    building_name_f = building_name.lower().replace('_', ' ')
    parent_name_to_id = dict()
    for building in building_info_json['data']:
        parent_name = building['parent_name']
        if parent_name.lower() == building_name_f:
            return building['parent_id']
    return None



