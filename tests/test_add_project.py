from model.project import Project


def test_add_project(app, config, json_project):
    config = config
    new_project = json_project
    old_projects_list = app.soap.get_projects(config)
    app.project.create(new_project)
    new_projects_list = app.soap.get_projects(config)
    if new_project not in old_projects_list:
        old_projects_list += [new_project]
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
