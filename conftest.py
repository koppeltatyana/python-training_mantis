import ftputil
import importlib
import jsonpickle
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


@pytest.fixture(scope='session')  # эта фикстура будет исп-ся другими фикстурами
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):  # функция, инициализирующая фикстуру
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config['web']['baseUrl'])  # создание фикстуры
    fixture.session.ensure_login(username=config['webAdmin']['username'], password=config['webAdmin']['password'])
    return fixture


@pytest.fixture(scope='session')
def db(request, config):
    db_fixture = DbFixture(host=config["db"]["host"], name=config["db"]["name"], user=config["db"]["user"], password=config["db"]["password"])

    def fin():
        db_fixture.destroy()
    request.addfinalizer(fin)
    return db_fixture


@pytest.fixture(scope='session', autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])

    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    #  создаем новое соединение с сервером
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    #  создаем новое соединение с сервером
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


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


def pytest_generate_tests(metafunc):  # функция для генерации тестов
    for fixture in metafunc.fixturenames:  # пробегаем по всем параметрам
        if fixture.startswith("data_"):
            test_data = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])
        elif fixture.startswith("json_"):
            test_data = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])


def load_from_module(module):  # берет из модуля данные
    return importlib.import_module("data.{0}".format(module)).test_data


def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/{0}.json".format(file))) as f:
        return jsonpickle.decode(f.read())
