import allure

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step("Зарегистрировать нового пользователя")
    def post_v1_account(self, registration: Registration):
        """
        Register new user
        :param
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    @allure.step("Получить данные пользователя")
    def get_v1_account(self, validate_response=True, **kwargs):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Активировать пользователя")
    def put_v1_account_token(self, token, validate_response=True):
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сменить почту зарегистрированного пользователя")
    def put_v1_account_email(
            self,
            change_email=ChangeEmail,
            validate_response=True
    ):
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сменить пароль зарегистрированного пользователя")
    def put_v1_account_password(self, change_password=ChangePassword, validate_response=True):
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/password',
            headers=headers,
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Сбросить пароль зарегистрированного пользователя")
    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=True):
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
