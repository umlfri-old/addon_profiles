class CStereotypeIcon(object):

    def __init__(self, id, name, filename):
        self.id = id
        self.name = name
        self.filename = filename

    def GetID(self):
        return self.id

    def GetName(self):
        return self.name

    def GetFilename(self):
        return self.filename