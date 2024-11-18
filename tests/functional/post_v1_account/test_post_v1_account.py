from json import loads
from faker import Faker

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)


def test_post_v1_account():
    # Initialization
    # 1.Создали конфигурацию
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    # 2. with configuration parametrize our Facades(they join our mini apis)
    dm_api = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    # 3. With our Facades(our 2 services - dm create and mailhog MEGA Facade)
    account_helper = AccountHelper(dm_account_api=dm_api, mailhog=mailhog)

    # Регистрация пользователя
    fake = Faker()
    login = "tst_account_" + str(fake.random_int(min=1, max=9999))
    email = f'{login}@mail.com'
    password = 'strongpassword'
    account_helper.register_new_user(login=login, password=password, email=email)
