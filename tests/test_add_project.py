from model.project import Project


def test_add_project(app, db, json_project):
    new_project = json_project
    old_projects_list = db.get_projects_list()
    app.project.create(new_project)
    new_projects_list = db.get_projects_list()
    if new_project not in old_projects_list:
        old_projects_list += [new_project]
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
