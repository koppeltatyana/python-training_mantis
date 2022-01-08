from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper


class Application:

    def __init__(self, browser, config):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser {0}".format(browser))
        self.config = config
        self.base_url = config["web"]["baseUrl"]
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.mail = MailHelper(self)
        self.signup = SignupHelper(self)
        self.soap = SoapHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd  # получаем ссылку на драйвер из текущего объекта
        wd.get(self.base_url)


    # def return_to_home_page(self):
    #     wd = self.wd
    #     if not (wd.current_url.endswith("/mantisbt-1.2.20/") and len(wd.find_elements_by_xpath("//input[@value='Send e-Mail']")) > 0):
    #         wd.find_element_by_link_text("home").click()

    def destroy(self):
        self.wd.quit()
