import allure

from checkers.http_checkers import check_status_code_http


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method PUT v1/account/email')
@allure.sub_suite('Positive tests')
class TestPutV1AccountEmail:
    @allure.title('Check change registered user email')
    def test_put_v1_account_email(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_and_activate_user(login=login, password=password, email=email)
        account_helper.auth_client(login=login, password=password)
        # Меняем емейл
        account_helper.change_email(login=login, password=password, email=email)

        # Пытаемся войти, получаем 403
        with check_status_code_http(
                expected_status_code=403,
                expected_message='User is inactive. Address the technical support for more details'
        ):
            account_helper.user_login(
                login=login,
                password=password,
            )

        # Активация пользователя
        account_helper.find_activation_mail_and_activate_user(login=login)

        # Авторизоваться
        account_helper.user_login(login=login, password=password)
