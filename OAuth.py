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
    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjMxNjYyNTAsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjMyMDk0NTAsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJwZktnbEJKUFdvbDN3Z3lkSUlYVmhfN25RUm8iLCJjbGllbnRfaWQiOiJwaWUifQ.mwNn2kguQNX2kEc8WhBLKmognOze11wKEP2No061lbn0Cyx43lzSy0ZwOObCHp3zO-KRwAcTijdbSB23RE49U6h6C-GY2tZYYWc5APf4nGmbQ8Mas2mO0RWHMD-KGhL9SfOdmRYgU9bfZrVem3TQawdWtzHgBs1oEpvEMhLSSR5r78q8vqrfJjq7mpoCzZYaEcH82m_YuPvtbFaDYe4WwBTX44brelErM063GAolWW-QDNYluyy2lU75RLBp4_7ePyOJluMgCycjpoofvRgibMhKo0baNOoQJ9s2ymnSVpJ0TN9Qfvi6gkmZx9Aeqm9_iEEBi-cJMtMx_UNpt8uIRA",
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