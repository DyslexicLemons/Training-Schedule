import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
from dotenv import load_dotenv
import os

now_iso = datetime.now().isoformat()            # Current date/time (ISO format)
jwt_token = os.getenv('JWT_TOKEN')
load_dotenv('creds.env')

def get_token(test=False):
    """
    Obtains JWToken for PIE API

    Parameters:
    test (bool): determines test or production function

    Returns:
    Token (string): JWT token to access PIE API
    """
    print("Obtaining token....")


    token = get_test_token() if test else get_real_token()
    test_string = "(Test)" if test else ""
    
    if token:
        print(f"Token obtained! {test_string} \n")
    else:
        print("Failed to obtain token \n")

    return token


def get_test_token():
    """
    [REQUIRES MANUAL EDIT]
    Returns token obtained manually through inspect 
    
    """

    token = os.getenv('JWT_TOKEN')

    test_auth_headers = {
        "Authorization" : token
    }
    return test_auth_headers


def get_real_token():
    """
    requests JWT using Client Credentials and proper OAuth methodology
    """
    token_url = "https://apps-test.iu.edu/uaa-stg/oauth/token"
    client_id = "pietrain",
    client_secret = "LzopHrQs6ypY8LhewFv4d3MnQbnrdWoDA8aMv2Yw"
    grant_type = "client_credentials"
    
    data = {
        'client_id' : client_id,
        'client_secret' : client_secret,
        'grant_type' : grant_type
    }

    response = requests.post(token_url,data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = "Bearer " + token_data.get('access_token')
        print('Status code: ',response.status_code,'\nAccess Token: ', access_token)
        return access_token

    else:
        print('failed to get token', response.status_code)
        print(response.json())


if __name__ == "__main__":
    token = get_token(test=True)