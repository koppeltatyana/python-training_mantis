from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        config = self.app.config
        client = Client(config["web"]["soapUrl"])
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects(self):
        config = self.app.config
        client = Client(config["web"]["soapUrl"])
        projects_list = []
        all_projects = client.service.mc_projects_get_user_accessible(config["webAdmin"]["username"], config["webAdmin"]["password"])
        for project in all_projects:
            projects_list += [Project(id=project.id, name=project.name, description=project.description, status=str(project.status.name))]
        return list(projects_list)
