import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
import os
import OAuth
import SQLhelper

# TODO Retrieve JSON file from PIE and saves it to the TrainingSchedule folder
def get_pie_json(save=False, test=False):
    """
    Gets Json file from PIE API
    """
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        "minimal": "true",
        "weekOf": "2024-07-21T04:00:00.000Z",
        "groupById": "1",
        "formatById": "1"
    }

    http_response = requests.get(BASE_URL,headers=OAuth.get_auth_headers(test),params=params)
    http_response.raise_for_status()
    print(http_response.status_code)
    if save:
        save_json(http_response, BASE_URL, params)
    
    return http_response.json()

def save_json(response, BASE_URL, params):
    """
    Saves formatted version of the JSON file to files
    """

    json_data = response.json()     # Sets HTTP GET request response 'json_data'
    folder_path = 'PIEJSONS'        

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

# TODO Update PSQL database based on JSON file from pie API
def update_employees(json):

    for shift in json:
         if shift["user"] not in employees["user"]:

# TODO Update Consultants Training Schedules in PSQL based on JSON file from pie API
def update_schedules(): 
    pass

if __name__ == "__main__":

    # 
    save = True
    test_JWT = True
    employee_json = get_pie_json(save, test_JWT)
    update_employees(employee_json)
    # employees = {}
    # for item in employee_json:


    