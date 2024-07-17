import requests
import json
from bs4 import BeautifulSoup
import TestHttpRequests

def get_auth_token():
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
    token = get_auth_token()
    print(token)
    TestHttpRequests.headers = {
        "Authorization" : token
    }

    URL = 'https://pie-stage.eas.iu.edu/Api/Users/18867'
    params = {

    }
    TestHttpRequests.test_http_request(URL,params)
