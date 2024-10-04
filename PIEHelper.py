import requests                                 # Http request library for python
import logging
import time
import json
import threading
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import socket
import os
import Authorization
import SQLHelper
import pandas as pd
from pytz import timezone
import orjson

# Set up logging
logging.basicConfig(level=logging.INFO)
eastern_tz = timezone('America/New_York')

SQL = SQLHelper.SQLHelper()

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

    logging.info("Submitting HTTP Request...")
    http_response = requests.get(BASE_URL,headers=headers,params=params)
    http_response.raise_for_status()
    logging.info(f"HTTP Request submitted with return code: {http_response.status_code}")

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

def get_shift_data_from_files(start_date, end_date):
    with ThreadPoolExecutor(max_workers=10) as executor:
        temp_date = start_date
        futures = []
        while temp_date < end_date:
            formatted_date = temp_date.strftime('%m-%d-%y')
            logging.info(f"Adding shifts for week of {formatted_date}")
            futures.append(executor.submit(process_weekly_shifts, formatted_date))
            temp_date += timedelta(days=7)

        # Wait for all futures to complete
        for future in futures:
            future.result()  # This will raise any exceptions that occurred in the thread


def process_weekly_shifts(formatted_date):
    json_data = read_file(formatted_date)
    total_accepted_shifts = 0

    if json_data:
        total_accepted_shifts = process_shifts(json_data, SQL)
    else:
        logging.warning(f"No data for {formatted_date}")

    logging.info(f"Shifts added for week of {formatted_date} with {total_accepted_shifts} accepted shifts.\n")


def process_shifts(json_data, SQL):
    shifts_to_insert = []
    total_failed_shifts = 0  # Counter for failed shifts

    for shift in json_data:
        try:
            shift_data = extract_shift_data(shift)
            shifts_to_insert.append(shift_data)
        except (KeyError, TypeError) as e:
            total_failed_shifts += 1  # Increment the counter on failure
            continue

    if shifts_to_insert:
        SQL.add_tasks(shifts_to_insert)

    # Log the total number of failed shifts for this data package
    if total_failed_shifts > 0:
        logging.warning(f"Total failed shifts for the current data package: {total_failed_shifts}")


    return len(shifts_to_insert)

def extract_shift_data(shift):
    shift_group = shift["shiftGroup"]
    user = shift["user"]
    task = shift_group["shiftType"]["name"]
    
    if task == "Training In Office":
        task = "Training"

    # Directly returning a tuple of values
    return (
        user["username"],
        user["firstName"],
        user["lastName"],
        task,
        shift["duration"]["difference"],
        datetime.fromisoformat(shift["startTime"]).astimezone(eastern_tz).date()
    )

def get_shift_data(start_date, end_date):
    temp_date = start_date
    SQL = SQLHelper.SQLHelper()

    total_accepted_shifts = 0

    while temp_date < end_date:
        formatted_date = temp_date.strftime('%Y-%m-%d')
        
        json_data = get_pie_data(save=True, test=True, date=formatted_date)  # Renamed 'json' to 'json_data'
        logging.info(f"Adding shifts for week of  {formatted_date}")
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

        logging.info("Shifts added for week of {formatted_date}")
        logging.info("Accepted shifts = {total_accepted_shifts}")
        logging.info("Rejected shifts = {total_rejected_shifts}")
        total_rejected_shifts = 0
        total_accepted_shifts = 0

        temp_date += timedelta(days=7)

def get_shift_date(start_datetime,end_datetime):

    # Extract the date from the start time
    start_date = start_datetime.date()

    # Check if end time is within one hour of midnight and if the date differs
    if end_datetime.date() != start_date and end_datetime.time() <= datetime.strptime('01:00:00', '%H:%M:%S').time():
        # If it crosses midnight within an hour, use the start date
        return start_date
    else:
        # Otherwise, use the date from the end time
        return end_datetime.date()

def read_file(date):
    folder_path = 'PIEJSONS'
    filename = date + '_10-03-24.json'
    file_path = os.path.join(folder_path, filename)
    
    if not os.path.isfile(file_path):
        logging.info(f"File {file_path} does not exist.")
        return None
    
    # Using orjson to read the JSON file
    with open(file_path, 'rb') as file:  # Note the 'rb' mode for binary reading
        try:
            content = orjson.loads(file.read())
            return content.get('data', [])
        except Exception as e:
            logging.info(f"Error reading JSON: {e}")
            return None


if __name__ == "__main__":
    start_time = time.time()  # Start time tracking
    save = True
    test = True
    start_date = datetime(2022, 1, 6)
    end_date = datetime(2024, 9, 1)
    get_shift_data_from_files(start_date, end_date)
    end_time = time.time()  # End time tracking

    elapsed_time = end_time - start_time
    logging.info(f"Total runtime: {elapsed_time:.2f} seconds")


    # # Call the get_shift_data function with the specified dates and inserted into "tasks" database
    # get_shift_data(start_date, end_date)





    