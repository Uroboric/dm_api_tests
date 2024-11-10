from json import loads
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_put_v1_account_email():
    # Initialization
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # Регистрация пользователя
    fake = Faker()
    login = "tst_acc" + str(fake.random_int(min=1, max=9999))
    email = f'{login}@mail.com'
    password = 'strongpassword'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.post_v1_account(json_data=json_data)
    print(f'post_v1_account | status code: {response.status_code}')
    print(f'post_v1_account | response text{response.text}')
    assert response.status_code == 201, f'User is not created! {response.json()}'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print(f'get_api_v2_messages | status code: {response.status_code}')
    print(f'get_api_v2_messages | response text{response.text}')
    assert response.status_code == 200, 'Email does not received!'

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    print(f'Activation token  : {token}')
    assert token is not None, f'Token for user {login} does not received!'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(f'put_v1_account_token | status code: {response.status_code}')
    print(f'put_v1_account_token | response text{response.text}')
    assert response.status_code == 200, 'User does not activated!'

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(f'post_v1_account_login | status code: {response.status_code}')
    print(f'post_v1_account_login | response text{response.text}')
    print(f'Auth token : {auth_token}')
    assert response.status_code == 200, "The user cannot log in"
    assert auth_token is not None, "x-dm-auth-token was not retrieved"

    # Меняем емейл
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    print(f'put_v1_account_email | status code: {response.status_code}')
    print(f'put_v1_account_email | response text{response.text}')
    assert response.status_code == 200, f"User can't created{response.json()}"

    # Пытаемся войти, получаем 403
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(f'post_v1_account_login | status code: {response.status_code}')
    print(f'post_v1_account_login | response text{response.text}')
    assert response.status_code == 403, "The user cannot log in"

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages()
    print(f'get_api_v2_messages | status code: {response.status_code}')
    print(f'get_api_v2_messages | response text{response.text}')
    assert response.status_code == 200, "Messages cannot be sent"

    # Активируем этот токен
    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Token for user {login}, cannot be received"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print(f'put_v1_account_token | status code: {response.status_code}')
    print(f'put_v1_account_token | response text{response.text}')
    assert response.status_code == 200, "User cannot be activated"

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response, auth_token = login_api.post_v1_account_login(json_data=json_data)
    print(f'post_v1_account_login | status code: {response.status_code}')
    print(f'post_v1_account_login | response text{response.text}')
    print(f'Auth token : {auth_token}')
    assert response.status_code == 200, "The user cannot log in"
    assert auth_token, "x-dm-auth-token was not retrieved"


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(f'user login: {user_login}')
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(f'token: {token}')
    return token
