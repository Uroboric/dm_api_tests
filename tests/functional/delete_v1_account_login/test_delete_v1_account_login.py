import allure


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method DELETE v1/account/login')
@allure.sub_suite('Positive tests')
class TestDeleteV1AccountLogin:
    @allure.title('Check logout as current user')
    def test_delete_v1_account_login(self, account_helper, prepare_user, auth_account_helper):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_and_activate_user(login=login, email=email, password=password)

        account_helper.auth_client(login=login, password=password)
        account_helper.logout_current_user()
