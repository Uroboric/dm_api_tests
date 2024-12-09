def test_put_v1_account_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.auth_client(login=login, password=password)
    # Меняем емейл
    account_helper.change_email(login=login, password=password, email=email)

    # Пытаемся войти, получаем 403
    account_helper.user_login(login=login, password=password, expected_status_code=403)

    # Активация пользователя
    account_helper.find_activation_mail_and_activate_user(login=login)

    # Авторизоваться
    account_helper.user_login(login=login, password=password)
