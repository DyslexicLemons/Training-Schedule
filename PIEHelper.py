import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime, timedelta
import socket
import os
import Authorization
import SQLHelper
import pandas as pd


def get_pie_data(save=False, test=False, date=datetime.now().strftime('%Y-%m-%d') ):
    """
    Obtains employee schedule data from scfl.pie.iu.edu website.

    Parameters:
    save (bool): Saves HTTP response.
    test (bool): When true, uses JWToken obtained manually from browser. 
                 When false, uses client secret provided by IU.

    Returns:
    json: Employee schedule data (shifts, roles, and tasks)
    """
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        "minimal": "true",
        "weekOf": date+"T04:00:00.000Z",
        "groupById": "1",
        "formatById": "1"
    }
    headers = Authorization.get_token(test)
    folder = "PIEJSONS"

    print("Submitting HTTP Request...")
    http_response = requests.get(BASE_URL,headers=headers,params=params)
    http_response.raise_for_status()
    print("HTTP Request submitted with return code: " + str(http_response.status_code))

    if save:
        save_file(http_response.json(), BASE_URL, params, folder)
    
    return http_response.json()

def get_role_data(save=False, test=False):
    """
    Obtains employee role data from scfl.pie.iu.edu website.

    Parameters:
    save (bool): Saves HTTP response.
    test (bool): When true, uses JWToken obtained manually from browser. 
                 When false, uses client secret provided by IU.

    Returns:
    json: Employee schedule data (shifts, roles, and tasks)
    """
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Users'
    params = {
        "minimal": "true",
        "ignoreActive": "true"
    }
    headers = Authorization.get_token(test)
    folder = "RoleJSONS"

    print("Submitting HTTP Request...")
    http_response = requests.get(BASE_URL,headers=headers,params=params)
    http_response.raise_for_status()
    print("HTTP Request submitted with return code: " + str(http_response.status_code))

    if save:
        save_file(http_response.json(), BASE_URL, params, folder)
    
    return http_response.json()

def save_file(json_data, BASE_URL, params, folder):
    """
    Saves JSON file to files

    Paramaters:
    json_data:           HTTP response (as a JSON).
    BASE_URL (string):   Request URL.
    params (dict):       Request paramaters.

    Returns (NA): Prints value contigent upon saving the new file
    
    """
    print("\n\nSaving file...")
    # Extract the weekOf date
    week_of_str = params["weekOf"]
    week_of_date = datetime.fromisoformat(week_of_str[:-1])  # remove 'Z' and convert
    week_of_formatted = week_of_date.strftime("%m-%d-%y")

    file_name = f"{week_of_formatted}.json"
    folder_path = folder        
    file_path = os.path.join(folder_path, file_name) # File Path = /{folder_path}/{filename}

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

def get_shift_data(start_date, end_date):
    temp_date = start_date
    SQL = SQLHelper.SQLHelper()
    total_rejected_shifts = 0
    total_accepted_shifts = 0

    while temp_date < end_date:
        formatted_date = temp_date.strftime('%Y-%m-%d')
        
        json_data = get_pie_data(save=True, test=True, date=formatted_date)  # Renamed 'json' to 'json_data'
        print("Adding shifts for week of " + formatted_date)
        for shift in json_data:  # each item in the JSON describes a shift
            # Check if required information is available
            try:
                task = shift["shiftGroup"]["shiftType"]["name"]
                if task == "Training In Office":
                    task = "Training"
                username = shift["user"]["username"]
                firstname = shift["user"]["firstName"]
                lastname = shift["user"]["lastName"]
                duration = shift["duration"]["difference"]
                # Convert the string to a datetime object
                datetime_obj = datetime.fromisoformat(shift["startTime"])

                # Extract just the date (without time)
                date = datetime_obj.date()


                SQL.add_task(username, firstname, lastname, task, duration, date)
                total_accepted_shifts+=1

            except (KeyError, TypeError) as e:
                total_rejected_shifts+=1
                continue  # Skip this shift if any required information is missing

        print("Shifts added for week of " + formatted_date)
        print("Accepted shifts = " + str(total_accepted_shifts))
        print("Rejected shifts = " + str(total_rejected_shifts))
        total_rejected_shifts = 0
        total_accepted_shifts = 0

        temp_date += timedelta(days=7)



                

if __name__ == "__main__":
    save = True
    test = True
    SQLWizard = SQLHelper.SQLHelper()
    role_data = get_role_data(save,test)
    SQLWizard.insert_role_data(role_data)



    # # Call the get_shift_data function with the specified dates and inserted into "tasks" database
    # get_shift_data(start_date, end_date)





    