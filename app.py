from flask import Flask, render_template
from utils import get_building_id_from_name, get_sorted_k_buildings_name_and_percent
import requests

app = Flask(__name__)

api_key = 'keaEyBNo68YQRGwpo-KbeyMxbCXJsUAAHOjNOausShWL6X0aR7NHzJKVaG9AAE-w'
base_url = 'http://density.adicu.com'

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/information/<int:k>', methods=['GET'])
def k_least_crowded(k):
    """
    Returns the sorted (on percentage full) k-least crowded building groups to display to the user.
    If k is greater than the total number of buildings, returns all building groups, sorted based on percent full.
    """
    error = ''
    if k < 0:
        error = 'Number cannot be negative.'
    else:
        # Make API request
        r = requests.get('{}/latest?auth_token={}'.format(base_url, api_key))

        # Attempt to parse data from API response
        try:
            response_json = r.json()
            data = response_json.get('data', None)
        except Exception as e:
            error = 'API response could not be parsed. Returned status code: {}'.format(r.status_code)

        # Turn raw API response data into sorted strings in following format:
        # <building_name> is <percent_full>% full.
        if data:
            # Get sorted building names and percent full
            sorted_k_buildings_name_and_percent = get_sorted_k_buildings_name_and_percent(data, k)

            # Convert to string version
            building_info = list()
            for building_tuple in sorted_k_buildings_name_and_percent:
                building_info.append('{} is {}% full'.format(building_tuple[0], building_tuple[1]))

            return render_template('information.html', building_info=building_info)
    return render_template('information.html', error=error) 
    

@app.route('/information/<string:building_name>', methods=['GET'])
def building_crowdedness(building_name):
    """
    Returns all of the building groups, along with their percentage full, within the given building name.
    The building name is not case sensitive, and spaces are given as underscores ('_')
    """
    # Get the building id from the given name. The id is needed to make the api call
    error = ''
    building_id = get_building_id_from_name(building_name)

    if not building_id:
        # Given building_name is not a valid name
        error = 'The given building name is not valid.'
    else:
        # Make API call
        r = requests.get('{}/latest/building/{}?auth_token={}'.format(base_url, building_id, api_key))

        # Attempt to parse data from raw API response
        try:
            response_json = r.json()
            data = response_json.get('data', None)
        except Exception as e:
            error = 'API response could not be parsed. Returned status code: {}'.format(r.status_code)
        if data:
            buildings_and_percentage_full = list()
            # Generate list of strings for front end from data
            for building in data:
                group_name, percent_full = building['group_name'], building['percent_full']
                buildings_and_percentage_full.append("{} is {}% full".format(group_name, percent_full))
            return render_template('information.html', building_info=buildings_and_percentage_full)
    return render_template('information.html', error=error)


if __name__ == '__main__':
    app.run()
