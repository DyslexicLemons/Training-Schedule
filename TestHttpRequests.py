import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
import os
import OAuth

# auth = ('jowamajo', 'Taryn Lily Bowie.')      # Login info
hostname = socket.gethostname()                 # PC hostname for JWT dictionary
now_iso = datetime.now().isoformat()            # Current date/time (ISO format)
jwt_tokens = {

    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAzMDI5OTQsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAzNDYxOTQsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJyX2REaDRteTdPR2NVV0F1aGZWdjdwNW1zYmciLCJjbGllbnRfaWQiOiJwaWUifQ.ofFsvLyrnDYpR2CPR7a1ts9TAjFqnNQl6syF7Mu6ACvLi6V718PGmoINGYgzSULYZ4K3lsMQ0xiGSoJeKibSG1EzXJA4TqhXJyCDBG9lP8Aofbk9j2nd95CUDnQinRwNE4YiqdfLtZlFQeG8y4yJumeWTzo9z8f2CTRT1tsccOnXsieACruaFWK-GssJXiFXAI6K3lQfr7X3lZpPSn56-jxHHsDj5vfjTTjpYLtR1XAmQ8OCUMOJ34nWKmAgMjeldxG3_7EiMUprk8Yfub0JKL3h4O7KdEJQOtl9M9Np6dqX_UhLXrR_KiM4wMZ1ZeONZ0_6otiRLNN1eqIhanXbtQ",
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjIzNDY5MzUsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjIzOTAxMzUsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJhdXJEb292Yjd2ZXZvUnEtUGFEWFdRcnN4ZFkiLCJjbGllbnRfaWQiOiJwaWUifQ.YWsIm3TQEx1vay9IpDzhQgP-DkT1fr4mZuiwGvu2FPO77POXoEqa8-KZW-ml9JFpulfeQH5KC1uEt9v0OE61Dhoim5EBYNjdqYyIEyeksLnV2DKccRq2X_HIkPFzWFjRU0AMa-XTTVwqQlNq8iQMuGNP5CYUPHd4ml6m6WyebKxQ1dIotjcAA1Y0o1fHthixsY6fZA_xn6FE1ckwiR7aeKbgySpukAvH-IL48Ndyc6NkOJGvU9kz94j66zTmBGZSrsy2UYG2RE0VeusXU312Wlf39W8IuWJyuvj6YlNIpj43CXnEaLpxyLhwuJ188FSrEpx6uUZNJFysfWFx972kcQ",
    "Pavlov-Inspiron-7559" : "TBD"
}
headers = {

    "Authorization" : jwt_tokens[hostname]

}

def get_token():
    return jwt_tokens[hostname]


def test_http_request(BASE_URL, params, save=False):
    """
    Description:
    prints status code of HTTP request
    """
    response = requests.get(BASE_URL,headers=OAuth.get_auth_headers,params=params)
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

    URL = 'https://scfl.pie.iu.edu/Api/Shifts'
    params = {
        "userId": '14495',
        "startTime": "2024-07-07T04:00:00.000Z",
        "endTime": "2024-07-21T04:00:00.000Z",
        "minimal": 'True'
    }
    test_http_request(URL,params)
