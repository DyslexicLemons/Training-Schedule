import requests                                 # Http request library for python

import json

import psycopg2                                 # PostgreSQL library for Python

from datetime import datetime

import socket

headers = {
    "Authorization" : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAxOTM1NDQsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAyMzY3NDQsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiIwVHB1d0drUzZ5bXVfQnczVXVxQ2luVjNsODQiLCJjbGllbnRfaWQiOiJwaWUifQ.gjpSljHAAcMVQBigRI57tYrFPhzNGaZkKpTP43lehkBw4fqa4ENqzyxG54v464mLnpArRruzi4jqCDQIJhATV_9Kp97cTQMEjmW35oe_7YOhe_xpfcFgQ6gyRT0YVkC8jWFiHdVlH2sghu3BjXwcbk4skoB-GHZR6lhDLcQY9OiTwJuDyym1XDhgjELujn6ViENhOGh8q4I-a8j-tm5LQGIVbU-P0f4uhLxX9ke7cIUchnsFxY0_VwQk0j2-Iv5BuSPHc66f66_L202DirMrkWdRZWIDLQ5P34cay7bvk3q1BcwZOcOajodJJBzlyDfYA0sB3oSQNDHjQQa0OIJ0wQ'
}

now_iso = datetime.now().isoformat()
now_iso = datetime.now().isoformat()            # Current date/time in iso format
# auth = ('jowamajo', 'Taryn Lily Bowie.')      # Use to retrieve JWT
jwt_tokens = {
    
    "IU-1BSVFY3" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAxODEwMTEsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAyMjQyMTEsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiI1clFQR2xoZWJhN1U1Uk9TREVuWVJPUWt0MWciLCJjbGllbnRfaWQiOiJwaWUifQ.DiVzsv3KsirLKCzIaF9AxQQ8NAfsVYPoVYf2RgBrfMqp-80HnvAItMmUO2hwxFoNNVD5wJwrokl-ZJ6hJtSOLhpK4qtifcsf_zjV6aHBJ0fYxRUyvo2rTQWXFxnxYEccVkptn9IiaNmNtoHcGk7Pk_s_1Oj9QhYfP5xCzNyrAeyM4wQJz1ggGFKs-9gSYNENngHMKbZSgoQrRBUV_IaC9whAHciWBfyM9FOonYhVQtL59Tr8O3aMAfpQzclzx-UvuO1HXljpLPuHf5hQiB1gvW0EpCWJ9DbZjauSKRapCzjInyUE4ChfAthjXghzqV9Gh20r3rg1-XNZecjJ-Yq01Q"
}
hostname = socket.gethostname()

headers = {

    "Authorization" : jwt_tokens[hostname]

}


"""
Request all consultants schedules
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

print(response)

content = response.content
decoded_json = json.loads(content.decode('utf-8'))
parsed_json = json.dumps(decoded_json, indent = 4)
print(parsed_json)
# """

# Request one consultant schedule
# """
# BASE_URL = 'https://scfl.pie.iu.edu/Api/Availabilities'
# params = {
#     "scheduleId" : "826",
#     "userId" : "18867"
# }

# response = requests.get(BASE_URL, headers=headers, params=params)   
# content = response.content
# print(response)

# decoded_content = json.loads(content.decode('utf-8'))
# parsed_content = json.dumps(decoded_content, indent = 4)
# print(parsed_content)