import requests                                 # Http request library for python
import json
import psycopg2                                 # PostgreSQL library for Python
from datetime import datetime


headers = {
    "Authorization" : 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3MjAxMDMwNjcsInVzZXJfbmFtZSI6Impvd2FtYWpvIiwic2NvcGUiOlsicmVhZCJdLCJleHAiOjE3MjAxNDYyNjcsImF1dGhvcml0aWVzIjpbIlJPTEVfU1RVREVOVCIsIlJPTEVfQUNNX1VTRVIiLCJST0xFX01GQV9VU0VSIiwiUk9MRV9TVEFGRiJdLCJqdGkiOiJISU9OSGFtcS15WkxYd2pwTy1FQ091U3l2STAiLCJjbGllbnRfaWQiOiJwaWUifQ.DS8pmotT0TUB5EwZR-6L_jUAAR-FBZwtIqcUFhz588ofCvb7qT5u5qSTKWfh3Fwsa1dGwLX_5041sHYx7wD6lnSNPF8pjLUQMfJ33axBB-TM5A2JaQ7_xwJ9iJLjp1rWlgFsAJ5019mi13LcHhI2zU33BOo3VYSJQEALHQ3PyQ91sMxah5VR4dZd7PJrVdq4Z2od7t3uammyIJa1vCDgBkEUCufCISlTP4M0pCXJ0ok1qcN0gUn52fFUUglja-eO7I1y1zOxHODrki6sDWfs_U4xWNwfwt-ZGRESR1jXW3W7p4XQCyye3DFtzNu9oM7gTlSunhsmJCaGFcef00EIhw'
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