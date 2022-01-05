import random
from model.project import Project


def test_delete_some_project(app, db):
    if len(db.get_projects_list()) == 0:
        app.project.create(Project(name="name"))
    old_projects_list = db.get_projects_list()
    random_project = random.choice(old_projects_list)
    app.project.del_some_project(random_project)
    new_projects_list = db.get_projects_list()
    old_projects_list.remove(random_project)
    assert sorted(new_projects_list, key=Project.id_or_max) == sorted(old_projects_list, key=Project.id_or_max)
