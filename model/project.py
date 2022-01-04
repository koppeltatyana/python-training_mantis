from sys import maxsize


class Project:

    def __init__(self, id=None, name=None, status=None, view_status=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.view_status = view_status
        self.description = description

    def __repr__(self):
        return "{0}: {1} {2}".format(self.id, self.name, self.status)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
