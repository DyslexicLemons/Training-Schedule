import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime
import socket
from dotenv import load_dotenv
import os

now_iso = datetime.now().isoformat()            # Current date/time (ISO format)
jwt_token = os.getenv('JWT_TOKEN')
load_dotenv()

def get_token(test=False):
    """
    Obtains JWToken for PIE API

    Parameters:
    test (bool): determines test or production function

    Returns:
    Token (string): JWT token to access PIE API
    """
    if test:
        return get_test_token()
    else:
        return get_real_token()


def get_test_token():
    """
    [REQUIRES MANUAL EDIT]
    Returns token obtained manually through inspect 
    
    """
#     test_auth_headers = {
#     "Authorization" : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjQ1Mjk2MDIsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjQ1NzI4MDIsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJHb1I5d2szbS04ZmsxZVozRVQwYkRKTGJKWlUiLCJjbGllbnRfaWQiOiJwaWUifQ.mWqIvcDhf9dGnPqVF5w2-YbS5LEzZhhnWc6Xem1gaCFid4Hyg64mG4Ay4LbgE-vBrOzMovFOgnVDugq9ZeprImR2CIHCu5vQO1LedVyYnrkE8QkO27CpjqeL2z_VHiKbvTW0-I5N0tdpkJuadP5HG2ncV_FZTNiwY5O5mO1Wd36dIxUZkIWBK7DxLcdIKWVQWSDrHOZ7plEKFOdokox__EBAlxBE2ZSHV1d3AVg-lheU4qXnDwIuFlGLRp56_3W07zJ3J6EMy_37Tqoja8YdkWcESpU-IdmllePUKZ7A5_Rf3BdqsZMGmIjZDu2BWJLCWWo3bpW7geqrkWZ7q0znfA'
# }
    token = os.getenv('JWT_TOKEN')
    print(token)
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