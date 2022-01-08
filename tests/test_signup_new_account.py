import random
import string


def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    # проверка, что пользователь зарегистрирован на почтовом сервере
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)  # регистрация пользователя в багтрекере
    assert app.soap.can_login(username, password)  # проверка возможности логина через удаленный программый интерфейс (через апишку)
