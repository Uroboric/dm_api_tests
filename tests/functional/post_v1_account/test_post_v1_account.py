import allure
import pytest
from faker import Faker

from checkers.http_checkers import check_status_code_http


faker = Faker()
fake_login = faker.name()
fake_email = faker.email()
fake_password = faker.password(length=10)


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method POST v1/account')
@allure.sub_suite('Positive tests')
class TestPostV1Account:

    @allure.title('Check register new user')
    def test_post_v1_account(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_code_http():
            account_helper.register_new_user(
                login=login,
                email=email,
                password=password
            )


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method POST v1/account')
@allure.sub_suite('Negative tests')
class TestPostV1AccountNeg:
    faker = Faker()
    fake_login = faker.name()
    fake_email = faker.email()
    fake_password = faker.password(length=10)

    @allure.title('Check register new user with bad request')
    @pytest.mark.parametrize(
        'login, email, password, error_message, expected_status_code',
        [
            # Короткий пароль: менее 6 символов
            (fake_login, fake_email, '1', 'Validation failed', 400),
            # Невалидный емейл: например, без использования символа @
            (fake_login, 'gmail.com', fake_password, 'Validation failed', 400),
            # Невалидный логин: например, один символ.
            ('S', fake_email, fake_password, 'Validation failed', 400)
        ]
    )
    def test_post_v1_account_negative(
            self,
            account_helper,
            login,
            email,
            password,
            error_message,
            expected_status_code
    ):
        with check_status_code_http(
                expected_status_code=expected_status_code,
                expected_message=error_message
        ):
            account_helper.register_new_user(
                login=login,
                email=email,
                password=password
            )
