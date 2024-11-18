from json import loads
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account():
    # Initialization
    account_api = AccountApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # # Регистрация пользователя
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
    assert response.status_code == 201, f"User can't created{response.json()}"

    # Получить письма из почтового сервера,
    response = mailhog_api.get_api_v2_messages()
    print(f'get_api_v2_messages | status code: {response.status_code}')
    print(f'get_api_v2_messages | response text{response.text}')
    # pprint.pprint(response.json())
    assert response.status_code == 200, "Messages cannot be sent"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    print(f'Activation token : {token}')
    assert token is not None, f"Token for user {login}, cannot be received"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(f'user login: {user_login}')
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(f'token: {token}')
    return token
