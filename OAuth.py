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
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjIzNDY5MzUsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjIzOTAxMzUsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJhdXJEb292Yjd2ZXZvUnEtUGFEWFdRcnN4ZFkiLCJjbGllbnRfaWQiOiJwaWUifQ.YWsIm3TQEx1vay9IpDzhQgP-DkT1fr4mZuiwGvu2FPO77POXoEqa8-KZW-ml9JFpulfeQH5KC1uEt9v0OE61Dhoim5EBYNjdqYyIEyeksLnV2DKccRq2X_HIkPFzWFjRU0AMa-XTTVwqQlNq8iQMuGNP5CYUPHd4ml6m6WyebKxQ1dIotjcAA1Y0o1fHthixsY6fZA_xn6FE1ckwiR7aeKbgySpukAvH-IL48Ndyc6NkOJGvU9kz94j66zTmBGZSrsy2UYG2RE0VeusXU312Wlf39W8IuWJyuvj6YlNIpj43CXnEaLpxyLhwuJ188FSrEpx6uUZNJFysfWFx972kcQ",
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