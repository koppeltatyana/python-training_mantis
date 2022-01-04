import pytest
import json
import os.path
from fixture.application import Application
from fixture.db import DbFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        # сначала берем абсолютный путь от файла __file__ (это у нас файл conftest)
        # далее берем название дииректории, в котором нах-ся conftest
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as file:
            target = json.load(file)
    return target


@pytest.fixture
def app(request):  # функция, инициализирующая фикстуру
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['web']['baseUrl'])  # создание фикстуры
    fixture.session.ensure_login(username=web_config['webAdmin']['username'], password=web_config['webAdmin']['password'])
    return fixture


@pytest.fixture(scope='session')
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    db_fixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])

    def fin():
        db_fixture.destroy()
    request.addfinalizer(fin)
    return db_fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")  # храним все остальные параметры в файле
