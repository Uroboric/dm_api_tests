from datetime import datetime

import allure
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


@allure.parent_suite('Functional tests')
@allure.suite('Tests for method POST v1/account/login')
@allure.sub_suite('Positive tests')
class TestsPostV1AccountLogin:
    @allure.title('Check registration new user')
    def test_post_v1_account_login(self, account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_and_activate_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        assert_that(response, all_of(
            has_property('resource', has_property('login', starts_with('homer_account'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                        {
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )
