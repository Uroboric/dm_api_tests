import requests


class AccountApi:
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return response

    def get_v1_account(self, auth_token):
        """
        Get current user
        :param auth_token: The x-dm-auth-token required
        :return: Response object
        """
        headers = {
            'accept': 'text/plain',
            'X-Dm-Auth-Token': auth_token
        }
        response = requests.get(
            url=f'{self.host}/v1/account',
            headers=headers
        )
        return response

    def put_v1_account_token(self, token):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(self, json_data):
        """
        Change registered user email
        :param json_data:
        :return:
        """

        response = requests.put(
            url=f'{self.host}/v1/account/email',
            json=json_data
        )
        return response
