def test_put_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_password = prepare_user.new_password

    account_helper.register_and_activate_user(login=login, email=email, password=password)

    account_helper.auth_client(login=login, password=password)

    account_helper.reset_and_change_password(login=login, email=email, old_password=password, new_password=new_password)

    account_helper.user_login(login=login,
                              password=password,
                              expected_status_code=400
                              )

    account_helper.user_login(login=login, password=new_password)
