import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
import os

# auth = ('jowamajo', 'Taryn Lily Bowie.')      # Login info
hostname = socket.gethostname()                 # PC hostname for JWT dictionary
now_iso = datetime.now().isoformat()            # Current date/time (ISO format)
jwt_tokens = {

    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAzMDI5OTQsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAzNDYxOTQsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJyX2REaDRteTdPR2NVV0F1aGZWdjdwNW1zYmciLCJjbGllbnRfaWQiOiJwaWUifQ.ofFsvLyrnDYpR2CPR7a1ts9TAjFqnNQl6syF7Mu6ACvLi6V718PGmoINGYgzSULYZ4K3lsMQ0xiGSoJeKibSG1EzXJA4TqhXJyCDBG9lP8Aofbk9j2nd95CUDnQinRwNE4YiqdfLtZlFQeG8y4yJumeWTzo9z8f2CTRT1tsccOnXsieACruaFWK-GssJXiFXAI6K3lQfr7X3lZpPSn56-jxHHsDj5vfjTTjpYLtR1XAmQ8OCUMOJ34nWKmAgMjeldxG3_7EiMUprk8Yfub0JKL3h4O7KdEJQOtl9M9Np6dqX_UhLXrR_KiM4wMZ1ZeONZ0_6otiRLNN1eqIhanXbtQ",
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAxODEwMTEsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAyMjQyMTEsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiI1clFQR2xoZWJhN1U1Uk9TREVuWVJPUWt0MWciLCJjbGllbnRfaWQiOiJwaWUifQ.DiVzsv3KsirLKCzIaF9AxQQ8NAfsVYPoVYf2RgBrfMqp-80HnvAItMmUO2hwxFoNNVD5wJwrokl-ZJ6hJtSOLhpK4qtifcsf_zjV6aHBJ0fYxRUyvo2rTQWXFxnxYEccVkptn9IiaNmNtoHcGk7Pk_s_1Oj9QhYfP5xCzNyrAeyM4wQJz1ggGFKs-9gSYNENngHMKbZSgoQrRBUV_IaC9whAHciWBfyM9FOonYhVQtL59Tr8O3aMAfpQzclzx-UvuO1HXljpLPuHf5hQiB1gvW0EpCWJ9DbZjauSKRapCzjInyUE4ChfAthjXghzqV9Gh20r3rg1-XNZecjJ-Yq01Q",
    "Pavlov-Inspiron-7559" : "tbd"

}
headers = {

    "Authorization" : jwt_tokens[hostname]

}

def get_all_users_json():
    """
    Description:
    Gets all Users data (including Schedule, first name, last name, username, etc.).
    Adds contents to PIEJSONS folder.
    """
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {

        "page" : "0",
        "pageLimit" : "0",
        "minimal" : "true",
        "weekOf" : now_iso,
        "groupById" : "1",
        "formatById" : "1"

    }
    response = requests.get(BASE_URL,headers=headers,params=params)
    content = response.content
    decoded_json = json.loads(content.decode('utf-8'))

    add_json_to_folder(content)
    return "decoded json added to folder"

def get_user(username):
    """
    Request consultant
    """
    BASE_URL = 'https://scfl.pie.iu.edu/Api/Availabilities'
    params = {
        "scheduleId" : "826",
        "userId" : "18867"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)   
    content = response.content
    print(response)

    decoded_content = json.loads(content.decode('utf-8'))
    parsed_content = json.dumps(decoded_content, indent = 4)
    print(parsed_content)

def add_json_to_folder(json_string):
    # Parse the JSON string
    data = json.loads(json_string)
    
    folder_path = 'PIEJSONS'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Generate the filename based on current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{current_time}.json"
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"JSON data has been written to {file_path}")

def add_users_database(json_string):
    tbd = json_string
    
if __name__ == "__main__":
    print("hello")
    get_all_users_json()
