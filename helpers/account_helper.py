import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retryer(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена #{count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('Превышено количество попыток получения активационного токена')
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    auth_token = None

    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response, auth_token = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login': login, 'password': password}
        )
        token = {
            "X-Dm-Auth-Token": auth_token
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'User is not created! {response.json()}'
        return response

    def activate_user(self, login: str):
        # response = self.mailhog.mailhog_api.get_api_v2_messages()
        # assert response.status_code == 200, 'Email does not received!'

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Token for user {login} does not received!'

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'User does not activated!'
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True, expected_status_code: int = 200):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response, auth_token = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == expected_status_code, "The user cannot log in"
        if expected_status_code == 200:
            assert auth_token is not None, "x-dm-auth-token was not retrieved"
        return auth_token

    def change_email(self, login: str, password: str, email: str):
        json_data = {
            "login": login,
            "password": password,
            "email": email
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, 'Email does not change!'

    def logout_current_user(self, auth_token):
        response = self.dm_account_api.login_api.delete_v1_account_login(auth_token=auth_token)
        assert response.status_code == 204, 'User is not unauthorized!'

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, 'Email does not received!'
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
