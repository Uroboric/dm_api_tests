from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # Initialization
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # # Регистрация пользователя
    login = 'feel_good127'
    email = f'{login}@mail.com'
    password = 'strongpassword'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"User can't created{response.json()}"

    # Получить письма из почтового сервера,
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    # pprint.pprint(response.json())
    assert response.status_code == 200, "Messages cannot be sent"

    # Получить активационный токен

    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Token for user {login}, cannot be received"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "User cannot be activated"

    # # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    print(f'Auth token : {auth_token}')
    assert response.status_code == 200, "The user cannot log in"
    assert auth_token, "x-dm-auth-token was not retrieved"

    # # Получить текущего пользователя
    # response = account_api.get_v1_account(auth_token=auth_token)
    # assert response.status_code == 200, "The user cannot log out"
    # print(response.status_code)
    # print(response.text)

    # Меняем емейл
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"User can't created{response.json()}"


    # Пытаемся войти, получаем 403
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "The user cannot log in"

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    # pprint.pprint(response.json())
    assert response.status_code == 200, "Messages cannot be sent"

    # Активируем этот токен
    # Получить активационный токен

    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Token for user {login}, cannot be received"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "User cannot be activated"


    # Логинимся
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    print(f'Auth token : {auth_token}')
    assert response.status_code == 200, "The user cannot log in"
    assert auth_token, "x-dm-auth-token was not retrieved"


    # Выход из системы как текущий пользователь
    response = login_api.delete_v1_account_login(auth_token=auth_token)
    assert response.status_code == 204, "The user cannot log out"
    print(response.status_code)
    print(response.text)

    # # Выход из системы с любого устройства
    # response = login_api.delete_v1_account_login_all(auth_token=auth_token)
    # assert response.status_code == 204, "The user cannot log out"
    # print(response.status_code)
    # print(response.text)

def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    return token
