from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        config = self.app.config
        client = Client(config["web"]["baseUrl"] + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    project_cache = None

    def get_projects(self):
        if self.project_cache is None:
            config = self.app.config
            client = Client(config["web"]["baseUrl"] + "api/soap/mantisconnect.php?wsdl")
            self.project_cache = []
            all_projects = client.service.mc_projects_get_user_accessible(config["webAdmin"]["username"], config["webAdmin"]["password"])
            for project in all_projects:
                self.project_cache += [Project(id=project.id, name=project.name, description=project.description, status=str(project.status.name))]
        return list(self.project_cache)
