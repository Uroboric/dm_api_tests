from dm_api_account.models.user_envelope import UserRole
from datetime import datetime
from hamcrest import (assert_that, has_property, starts_with, all_of, not_none, is_, instance_of, has_properties,
                      equal_to, has_items, greater_than_or_equal_to, greater_than, any_of, close_to,
                      less_than_or_equal_to)


def test_get_v1_account(auth_account_helper):
    response = auth_account_helper.get_user_info(validate_response=True)
    assert_that(response.resource, all_of(
        has_property('login', starts_with('tst_account')),
        has_property('roles', not_none()),
        has_property('roles', is_(list)),
        has_property('roles', has_items(
                    UserRole.GUEST,
                    UserRole.PLAYER
                   )
        ),
        has_property('registration', instance_of(datetime)),
        has_property('rating', has_properties(
                    {
                        "enabled": equal_to(True),
                        "quality": equal_to(0),
                        "quantity": equal_to(0)
                    }
                )
            ),

        )
    )


def test_get_v1_account_no_auth(account_helper):
    account_helper.get_user_info()
