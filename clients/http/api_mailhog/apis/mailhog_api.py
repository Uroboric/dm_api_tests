import allure

from packages.restclient.client import RestClient


class MailhogApi(RestClient):
    @allure.step('Get users emails')
    def get_api_v2_messages(self, limit=2):
        """
        Get user emails
        :return:
        """
        params = {
            'limit': limit,
        }
        response = self.get(
            path='/api/v2/messages',
            params=params,
            verify=False
        )
        return response
