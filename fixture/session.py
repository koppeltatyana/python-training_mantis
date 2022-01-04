class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd  # получаем ссылку на драйвер из текущего объекта
        self.app.open_home_page()
        wd.implicitly_wait(2)
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector('input[type="submit"]').click()

    def logout(self):
        wd = self.app.wd  # получаем ссылку на драйвер из текущего объекта
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as_username(username):
                return
            else:
                self.logout()
        self.login(username, password)

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0  # считаем, что залогинены, если на стр есть кнопка Logout

    def is_logged_in_as_username(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    #  находим под каким именем залогинены
    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text
