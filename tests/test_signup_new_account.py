def test_signup_new_account(app):
    # проверка, что пользователь зарегистрирован на почтовом сервере
    username = "user123"
    password = "test"
    app.james.ensure_user_exists(username, password)
