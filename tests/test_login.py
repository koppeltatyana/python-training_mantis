def test_login(app):
    app.session.login("administrator", "root")
    assert app.session.is_logged_in_as_username("administrator")
