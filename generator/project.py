import getopt
import random
import string
import sys
from model.project import Project
import os.path
import jsonpickle


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 5
    return prefix + "".join(random.choice(symbols) for i in range(random.randrange(maxlen)))


def random_status():
    state = ["development", "release", "stable", "obsolete"]
    return random.choice(state)


def random_view_status():
    view_state = ["public", "private"]
    return random.choice(view_state)


#  чтение опций командной строки (из оф страницы)
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/project.json"

test_data = [
    Project(name=random_string('n', 10), status=random_status(), view_status=random_view_status(), description=random_string('desc', 50))
    for i in range(n)
]

# сначала берем абсолютный путь от файла __file__
# далее берем название дииректории, в котором нах-ся файл
# к директории приклеиваем значение из ".." + f
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)
with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)  # чтобы данные в json-файлых были красивенькие
    out.write(jsonpickle.encode(test_data))  # ета штука нужна чтобы к сгенерированным данным еще и дописывать имя класса
