from requests import JSONDecodeError

from requests import session
import structlog
import uuid
import curlify

from restclient.configuration import Configuration
from restclient.utiltties import allure_attach


class RestClient:
    def __init__(
            self,
            configuration: Configuration
    ):
        self.host = configuration.host
        self.set_headers(configuration.headers)
        self.disable_log = configuration.disable_log
        self.session = session()
        self.log = structlog.getLogger(__name__).bind(service='api')

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def post(self, path, **kwargs):
        return self._send_request(method='POST', path=path, **kwargs)

    def get(self, path, **kwargs):
        return self._send_request(method='GET', path=path, **kwargs)

    def put(self, path, **kwargs):
        return self._send_request(method='PUT', path=path, **kwargs)

    def delete(self, path, **kwargs):
        return self._send_request(method='DELETE', path=path, **kwargs)

    # метод для логирования запросов
    # kwargs принимает функции(переменные значения именованных аргуменов)из реквест принимает json, data, verified и т.д
    # kwargs является словарем по сути и значения получаем соотв оразом из нево
    @allure_attach
    def _send_request(self, method, path, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        full_url = self.host + path

        if self.disable_log:
            rest_response = self.session.request(method=method, url=full_url, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )
        rest_response = self.session.request(method=method, url=full_url, **kwargs)
        curl = curlify.to_curl(rest_response.request)
        print(curl)
        log.msg(
            event='Response',
            status_code=rest_response.status_code,
            headers=rest_response.headers,
            json=self._get_json(rest_response),
        )
        rest_response.raise_for_status()
        return rest_response

    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}
