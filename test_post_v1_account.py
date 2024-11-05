import pprint
from json import loads

import requests


def test_post_v1_account():
    # # Регистрация пользователя
    login = 'theodor_crow9'
    email = f'{login}@mail.com'
    password = 'strongpassword'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"User can't created{response.json()}"

    # Получить письма из почтового сервера,
    params = {
        'limit': '10',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    # pprint.pprint(response.json())
    assert response.status_code == 200, "Messages cannot be sent"

    # Получить активационный токен
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
            break
    assert token is not None, f"Token for user {login}, cannot be received"

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "User cannot be activated"

    # # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "The user cannot log in"
