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
    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjM1MTEzODUsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjM1NTQ1ODUsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJCX19tZGlpTFBfRThFdGRPclk4NWZ0TllycGMiLCJjbGllbnRfaWQiOiJwaWUifQ.WBOXHGfQlaSLxLkd2oaLMQV7Qd8sxy2oEW9iM4cttOTrIT54qiiKc2M9oLg2hxl143qKhnxWfEKwB18ma7PRsqJHqhxasVKcpBGJ58X0RHM7mWzSpiDFcSHKvVrYNxcM5kP71FdOAKOhZ4D24dwrTl5IRP6MltUAg4vbWFdj593_crlTdN9ZiM-I1KHzGXWe-KpGP2a_oofVyelHlnVDXM-kUgXlQpkMtXg8ODxazxukQN_s6KhRkOuDnJ2Uqze_dk6k7xxlbYpEbPq-FAZF1rz4ywOONM0YLMG-6LlUTaKPSZ2BGsvOQfsun4e73AzBNZAaw5U55x6qQNyFlTjURA",
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjM1MTU4NjMsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjM1NTkwNjMsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJ2eWlkX1ByMk1mNi1IT2dJLUlYZGROaWhxZG8iLCJjbGllbnRfaWQiOiJwaWUifQ.a7mPbTVSRfvw75d3n1PmCSMV6s0EY_9miabFs93vJXtRMYC1Xw-0nyLdrCU4fzqMwTP6FGsIACi1Hutso_NEjRqOd3cMUOfaSY962Bl1SC4p3d0Ga4QgWrkfa9-pRBP2zyRz3BaOZ_Y2ovEZSQwBX0G0qvqcgtRhXW9jSI0LFz4i3LEEvTuAV81SNpQfMzSTJjd-vDJOc3PmWZRumTGcdvNNE-pJCowQur_NHp2amiu4WbIC7C-ii4d9uHAEziNB5Ubb2eL0nTRHrzqI2jIjaPwEfV-x-1WpS_OdkqP4AvAYZeeTNgCyM6PGBTDm315K-0Iz0fLsed0ao2GGcZgU3Q",
    "Pavlov-Inspiron-7559" : "TBD"
}

test_headers = {
    "Authorization" : jwt_tokens[hostname]
}

def get_auth_headers(test=False):
    """
    Returns oAuth JWT within headers
    """
    if test:
        return test_headers
    else:
        headers = {
            "Authorization" : request_real_JWT()
        }

def request_real_JWT():
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