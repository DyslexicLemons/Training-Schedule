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
    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjIzNzMyMzEsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjI0MTY0MzEsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJnVjYtd0NaUlQ2aTM3YzROSm9KUWFNOUp0M2MiLCJjbGllbnRfaWQiOiJwaWUifQ.M4dTQBPzaInJvTOz3sJq1SgHDkxBSdJm0grM6g563C8Wa8IyoQEQu0rfAA4VSEz6AQ2iJSbchuE0FAIPsyyfwerV0w7_GkH4oO5ZC0Btfg9HuoeNFNVBOvTCDO8ACTRtCPPTP4wr60tNhkZKi2BLsXyROff13XQP3nq5rvPuYMl8NW-P_bsOq7Em22baz6SlCIsily78Ol7G1YMV9O1LDl2MrbkaqSS1TDbeHSys7MUPbbsfO9IM8OwDVFvaXZXETEmZRIDGl53P_gqqtGcnY6LY8PB_PBAIRUUgV5Oq3qnifP5Q5rUR9hGl-GxVXoElfhPH9OA-8vHK0Ceds9QRgg",
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjE4MjgwNjcsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjE4NzEyNjcsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJUdjVMSzUwUmc3MlB4djA3M0NiNVg4NGlSMTQiLCJjbGllbnRfaWQiOiJwaWUifQ.anYu-GRpckvK4e2Y12cGhRSH73rPouTJgumz6LsMKjWFkSu31MuhuIHIGfC4DIHEu41srE3zVwF33RKyMnci8svel2TdK8B13hYnsq1cpZvLQMKaE74a96XGhuuAZOG-96KbrT4ACbYJr6fMDaMq8q20Y_GPdjNW0HJLwDPL6ZPAMAy_bFBUbXYiOQzmrVQSosJGOojGOfE86ZZK5bqLEuIVsFBSnVDkJ3heVjotaj-R6-d28suEH5iSOrwdiJVPbQw_4AsI4ja4iBQl8sKhRR2abgK2fvL1MBlPS8y4vvGWeSm3NncNa41c4A_RpCBGvwmdQWWmJPcl2qZO3NQldw",
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