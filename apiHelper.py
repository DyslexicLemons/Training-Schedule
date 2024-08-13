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
    current_date = datetime.now().strftime('%Y-%m-%d')
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        "minimal": "true",
        "weekOf": current_date+"T04:00:00.000Z",
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
    SQL_database = SQLhelper.SQLhelper()
    usernames = SQL_database.get_usernames()
    print("current employees in Database: ")
    print(usernames)
    training_status = ""
    for shift in json: # each item in the JSON is describing a different shift
        PIErole = shift["shiftGroup"]["role"]["name"]
        if shift["user"] is not None and shift["user"]["username"] not in usernames:
            if PIErole == "PA (Supervisor)" or PIErole == "Comp Coord (Supervisor)":
                role = "Supervisor"
            else:
                role = "Consultant"
                if PIErole == "Trainee":
                    training_status = "Trainee"
            new_employee = (shift["user"]["id"], shift["user"]["username"], shift["user"]["firstName"], shift["user"]["lastName"], role, training_status) 
            # SQL_database.add_employee(shift["user"]["id"], shift["user"]["username"], shift["user"]["firstName"], shift["user"]["lastName"])

            for value in new_employee:
                print(value)
            print('\n')
            usernames = usernames + [shift["user"]["username"]] # (shift["user"]["username"],)

# TODO Update Consultants Training Schedules in PSQL based on JSON file from pie API
def update_schedules(): 
    pass

if __name__ == "__main__":

    # 
    save = True
    test_JWT = True
    employee_json = get_pie_json(save, test_JWT)
    update_employees(employee_json)


    