from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=json_data
        )
        auth_token = response.headers.get('x-dm-auth-token')
        return response, auth_token

    def delete_v1_account_login(self, auth_token):
        """
        Logout as current user
        :param auth_token: The x-dm-auth-token required for logout
        :return: Response object
        """
        headers = {
            'accept': '*/*',
            'X-Dm-Auth-Token': auth_token
        }
        response = self.delete(
            path='/v1/account/login',
            headers=headers
        )
        return response

    def delete_v1_account_login_all(self, auth_token):
        """
        Logout from every device
        :param auth_token: The x-dm-auth-token required for logout
        :return: Response object
        """
        headers = {
            'accept': '*/*',
            'X-Dm-Auth-Token': auth_token
        }
        response = self.delete(
            path='/v1/account/login/all',
            headers=headers
        )
        return response
