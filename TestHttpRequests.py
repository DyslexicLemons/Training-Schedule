import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime


headers = {
    "Authorization" : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAxOTM1NDQsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAyMzY3NDQsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiIwVHB1d0drUzZ5bXVfQnczVXVxQ2luVjNsODQiLCJjbGllbnRfaWQiOiJwaWUifQ.gjpSljHAAcMVQBigRI57tYrFPhzNGaZkKpTP43lehkBw4fqa4ENqzyxG54v464mLnpArRruzi4jqCDQIJhATV_9Kp97cTQMEjmW35oe_7YOhe_xpfcFgQ6gyRT0YVkC8jWFiHdVlH2sghu3BjXwcbk4skoB-GHZR6lhDLcQY9OiTwJuDyym1XDhgjELujn6ViENhOGh8q4I-a8j-tm5LQGIVbU-P0f4uhLxX9ke7cIUchnsFxY0_VwQk0j2-Iv5BuSPHc66f66_L202DirMrkWdRZWIDLQ5P34cay7bvk3q1BcwZOcOajodJJBzlyDfYA0sB3oSQNDHjQQa0OIJ0wQ'
}

now_iso = datetime.now().isoformat()
# auth = ('jowamajo', 'Taryn Lily Bowie.')      # Use to retrieve JWT

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
# print(parsed_json)
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