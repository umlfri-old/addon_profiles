class CTag(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def GetName(self):
        return self.name

    def GetType(self):
        return self.type