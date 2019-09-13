from flask import Flask, render_template
from utils import get_building_id_from_name
import requests

app = Flask(__name__)

api_key = 'keaEyBNo68YQRGwpo-KbeyMxbCXJsUAAHOjNOausShWL6X0aR7NHzJKVaG9AAE-w'
base_url = 'http://density.adicu.com'

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/information/<int:k>', methods=['GET'])
def k_least_crowded(k):
    pass
    
@app.route('/information/<string:building_name>', methods=['GET'])
def building_crowdedness(building_name):
    building_id = get_building_id_from_name(building_name)
    if building_id:
        r = requests.get('{}/latest/building/{}?auth_token={}'.format(base_url, building_id, api_key))
        try:
            response_json = r.json()
            buildings_and_percentage_full = list()
            for building in response_json['data']:
                group_name, percent_full = building['group_name'], building['percent_full']
                buildings_and_percentage_full.append("{} is {}% full".format(group_name, percent_full))
            return render_template('information.html', building_info=buildings_and_percentage_full)
        except Exception as e:
            print("Error while parsing response: {}".format(e))
    return render_template('information.html', error='Error occurred while getting building data')


if __name__ == '__main__':
    app.run()
