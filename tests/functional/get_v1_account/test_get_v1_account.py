
import allure
import pytest
from datetime import datetime
from hamcrest import (assert_that, has_property, starts_with, all_of, not_none, is_, instance_of, has_properties,
                      equal_to, has_items)


from checkers.http_checkers import check_status_code_http


    @allure.title('Check get current user without authentication')
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(expected_status_code=401, expected_message='User must be authenticated'):
            account_helper.get_user_info()

