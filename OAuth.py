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

    "Desktop" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjE4NjcwNTksInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjE5MTAyNTksImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJJLXluV2piaU9aTDNVWk8xWngxV3NhdGhPUEkiLCJjbGllbnRfaWQiOiJwaWUifQ.F4XgNiPSNY6baRY-i3F6rNjptsTZLxJkiGBZWGlNBpgpx3W_myy401uZrS3GfbjKLzrNIrszrNuBHpdXzQStmmIIaIzcvenD7VTWcm22-kCVGHK95vQXKRMdOgZwBpZNGRF-ZfyUrNCl8-AMSf5F_qm_0YyV1sHC110cVZP6CJ5Fwys1neboWXqnUqFYmMYxq-5E8A68TGJc7DyBr_L3bQ3J-pALhWllkNdCo3NPVTveWhhOJGoIeugmAIC7cJlfwWIOCiOhhI6jjKUOz53JnOi5PR7hROpqrd9VwAbZxii-iSo5s9PAhw2FiinN5MaqW-H9fVDjDU9wczsm12bmSg",
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

def request_real_JWT(self):
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