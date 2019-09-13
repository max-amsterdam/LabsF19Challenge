import json
from operator import itemgetter

def get_building_id_from_name(building_name):
    """
    Gets the building id from a given building name.
    Uses the 'building_info.txt' file to know which building_name correlates to which id.

    Note: building name is not case sensitive and all white spaces are given as underscores

    Returns None if the given building_name is not found
    """
    building_info_txt = open('building_info.txt')
    building_info_json = json.load(building_info_txt)

    building_name_f = building_name.lower().replace('_', ' ')
    parent_name_to_id = dict()
    for building in building_info_json['data']:
        parent_name = building['parent_name']
        if parent_name.lower() == building_name_f:
            return building['parent_id']
    return None

def get_sorted_k_buildings_name_and_percent(data, k):
    """
    Converts a list of json objects into a sorted list of at least size k 
    based on the percent full (ascending order). 

    The return type is a list of tuples, with each tuple corresponding to:
    (group_name, percent_full)
    """
    result_list = list()
    for building in data:
        group_name, percent_full = building['group_name'], building['percent_full']
        result_list.append((group_name, percent_full))
    result_list.sort(key=itemgetter(1))
    # Returns the first k elements of the list, unless k is greater than or equal to the 
    # number of total building groups. In that case, just returns the entire result_list
    return result_list[:k] if k < len(result_list) else result_list
            



