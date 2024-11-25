from dm_api_account.models.registration import Registration
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

    def get_v1_account(self, **kwargs):
        """
        Get current user
        :param kwargs:
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
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

    def put_v1_account_token(self, token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(self, json_data):
        """
        Change registered user email
        :param json_data:
        :return:
        """

        response = self.put(
            path='/v1/account/email',
            json=json_data
        )
        return response

    def put_v1_account_password(self, json_data):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=json_data,
        )

    def post_v1_account_password(self, json_data):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=json_data
        )
        return response
