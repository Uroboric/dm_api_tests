import time
from json import loads

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
# from retrying import retry


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

    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        auth_token = response.headers['X-Dm-Auth-Token']
        token = {
            "X-Dm-Auth-Token": auth_token
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)
        assert response.headers["X-Dm-Auth-Token"], "Token for user doesn't received"

    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            email=email,
            password=password,
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        # assert response.status_code == 201, f'User is not created! {response.json()}'
        return response

    def activate_user(self, token: str):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, 'User does not activated!'
        return response

    def register_and_activate_user(self, login: str, email: str, password: str):
        self.register_new_user(login=login, email=email, password=password)
        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        response_time = end_time - start_time
        assert response_time < 3, f"Activation waiting time is:{response_time} sec. out of limit"
        self.activate_user(token=token)

    def find_activation_mail_and_activate_user(self, login: str):
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f'Token for user {login} does not received!'
        self.activate_user(token=token)

    def user_login(self,
                   login: str,
                   password: str,
                   remember_me: bool = True,
                   validate_response=False,
                   validate_headers=False
                   ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me,
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        if validate_headers:
            assert response.headers['X-Dm-Auth-Token'], 'User does not get token'
            # assert response.status_code == expected_status_code, "The user cannot log in"
        return response

    def change_email(self, login: str, password: str, email: str):
        change_email = ChangeEmail(
            login=login,
            email=email,
            password=password
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        # assert response.status_code == 200, 'Email does not change!'
        return response

    def logout_current_user(self, **kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, 'User is not unauthorized!'

    def logout_user_from_all_devices(self, ** kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
        assert response.status_code == 204, 'User is not unauthorized!'

    # @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login: str, token_type: str = 'activate'):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login and token_type == 'activate' and user_data.get('ConfirmationLinkUrl'):
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            elif user_login == login and token_type == 'reset' and user_data.get('ConfirmationLinkUri'):
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
        return token

    def reset_password(self, login: str, email: str, validate_response=True):
        reset_password = ResetPassword(login=login, email=email)
        response = self.dm_account_api.account_api.post_v1_account_password(
            reset_password=reset_password,
            validate_response=validate_response
        )
        return response

    def get_user_info(self, validate_response=False):
        response = self.dm_account_api.account_api.get_v1_account(validate_response=validate_response)
        return response

    def change_password(
            self,
            login: str,
            token: str,
            old_password: str,
            new_password: str
    ):
        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        return response

    def reset_and_change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str,
    ):
        self.reset_password(
            login=login,
            email=email
        )
        token = self.get_activation_token_by_login(
            login=login,
            token_type='reset'
        )
        self.change_password(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )
