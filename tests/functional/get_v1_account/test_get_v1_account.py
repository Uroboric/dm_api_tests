def test_get_v1_account(auth_account_helper):
    auth_account_helper.get_user_info(validate_response=True)


def test_get_v1_account_no_auth(account_helper):
    account_helper.get_user_info()
