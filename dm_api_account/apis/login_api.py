from dm_api_account.models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, login_credentials: LoginCredentials):
        """
        Authenticate via credentials
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        # auth_token = response.headers.get('x-dm-auth-token')
        return response

    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :param kwargs:
        :return:
        """
        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :param kwargs:
        :return:
        """
        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response
