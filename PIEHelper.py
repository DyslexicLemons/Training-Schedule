import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
import os
import Authorization
import SQLHelper


def get_pie_data(save=False, test=False):
    """
    Obtains employee schedule data from scfl.pie.iu.edu website.

    Parameters:
    save (bool): Saves HTTP response.
    test (bool): When true, uses JWToken obtained manually from browser. 
                 When false, uses client secret provided by IU.

    Returns:
    json: Employee schedule data (shifts, roles, and tasks)
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        "minimal": "true",
        "weekOf": current_date+"T04:00:00.000Z",
        "groupById": "1",
        "formatById": "1"
    }
    headers = Authorization.get_token(test)

    print("Submitting HTTP Request...")
    http_response = requests.get(BASE_URL,headers=headers,params=params)
    http_response.raise_for_status()
    print("HTTP Request submitted with return code: " + str(http_response.status_code))

    if save:
        save_file(http_response.json(), BASE_URL, params)
    
    return http_response.json()

def save_file(json_data, BASE_URL, params):
    """
    Saves JSON file to files

    Paramaters:
    json_data:           HTTP response (as a JSON).
    BASE_URL (string):   Request URL.
    params (dict):       Request paramaters.

    Returns (NA): Prints value contigent upon saving the new file
    
    """
    print("\n\nSaving file...")
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S") 
    file_name = f"{current_time}.json"
    folder_path = 'PIEJSONS'        
    file_path = os.path.join(folder_path, file_name) # File Path = /PIEJSONS/{filename}

    metadata = { # Adds params for HTTP request to JSON
        "BASE URL": BASE_URL,
        "Parameters": params if params else {}
    }
    
    with open(file_path, 'w') as file:
        json.dump({"metadata": metadata, "data": json_data}, file, indent=4)
    
    print(f"JSON data has been written to {file_path}")

def work_on_date(username, date, PIEdata):
    for data in PIEdata:
        if data['user']['username'] is username:
            start_time_str = data["startTime"]
            work_date = datetime.strptime(start_time_str[:10], "%m-%d-%y").date()
            if date is work_date:
                return True
    return False
                

if __name__ == "__main__":
    save = True
    test = True
    SQLWizard = SQLHelper.SQLHelper()
    employee_json = get_pie_data(save, test=True)
    SQLWizard.update_employees(employee_json)


    