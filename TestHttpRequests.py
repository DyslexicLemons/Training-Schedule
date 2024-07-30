import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
import os
import OAuth





def test_http_request(BASE_URL, params, save=False):
    """
    Description:
    prints status code of HTTP request
    """
    response = requests.get(BASE_URL,headers=OAuth.get_auth_headers(),params=params)
    response.raise_for_status()
    print(response.status_code)
    if save:
        save_json(response, BASE_URL, params)


def save_json(response, BASE_URL, params):
    """
    Saves Http request JSON file
    """

    json_data = response.json()     # Sets HTTP response to variable 'json_data'

    folder_path = 'PIEJSONS'        # Generate the filename based on current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{current_time}.json"
    file_path = os.path.join(folder_path, file_name)

    metadata = {
        "BASE URL": BASE_URL,
        "Parameters": params if params else {}
    }
    
    with open(file_path, 'w') as file:
        json.dump({"metadata": metadata, "data": json_data}, file, indent=4)
    
    print(f"JSON data has been written to {file_path}")

def strip_json(file_path):
    with open(file_path, 'r') as file:
        raw_json = json.load(file)
    preferred_name = raw_json["data"][2]["preferredName"]
    first_name = raw_json["data"][2]["preferredName"]
    last_name = raw_json["data"][2]["lastName"]
    username = raw_json["data"][2]["username"]

    
    print(preferred_name)
    print(first_name)
    print(last_name)
    print(username)

if __name__ == "__main__":
    # file_path = os.path.join("PIEJSONS", "20240706_190028.json")
    # with open(file_path, 'r') as file:
    #     data = json.load(file)
    # user_values = [item['user'] for item in data]
    # print(user_values)

    #Test1
    # BASE_URL = 'https://scfl.pie.iu.edu/Api/Users'
    # params = {
    #     "minimal": "true"
    # }

    # test_http_request(BASE_URL,params, True)
    # file_path = "PIEJSONS/20240711_191825.json"
    # strip_json(file_path)

    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        'minimal': 'true',
        'weekOf': '2024-07-21T04:00:00.000Z',
        'groupById': '1',
        'formatById': '1'
    }
    test_http_request(BASE_URL,params)
