from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, registration: Registration):
        """
        Register new user
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)  # exclude_none - if some field is optional and not filled in, we will not pass it
        )
        return response

    def get_v1_account(self, validate_response=True, **kwargs):
        """
        Get current user
        :param kwargs:
        :param validate_response:
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    # def get_v1_account(self, auth_token):
    #     """
    #     Get current user
    #     :param auth_token: The x-dm-auth-token required
    #     :return: Response object
    #     """
    #     headers = {
    #         'accept': 'text/plain',
    #         'X-Dm-Auth-Token': auth_token
    #     }
    #     response = self.get(
    #         path='/v1/account',
    #         headers=headers
    #     )
    #     return response

    def put_v1_account_token(self, token, validate_response=True):
        """
        Activate registered user
        :param token:
        :param validate_response:
        :return:
        """
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

    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response=True
    ):
        """
        Change registered user email
        :param change_email: ChangeEmail:
        :param validate_response:
        :return:
        """

        response = self.put(
            path='/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=True
    ):
        """
        Change registered user password
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response=True
    ):
        """
        Reset registered user password
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
