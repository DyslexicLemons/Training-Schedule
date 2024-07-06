import requests

def get_jwt(username, password):
    url = 'https://idp.login.iu.edu/idp/profile/cas/login?execution=e1s2'
    payload = {'username': 'jowamajo', 'password': 'Taryn Lily Bowie,'}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json().get('token')
    else:
        raise Exception('Failed to retrieve JWT')

jwt_token = get_jwt('your_username', 'your_password')


