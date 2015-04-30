class CProfilePackage(object):
    def __init__(self, packageElement, stereotypes = None):
        self.packageElement = packageElement
        self.stereotypes = stereotypes or []

    def IsOrphaned(self):
        return False

    def GetUID(self):
        return self.packageElement.__id__

    def GetPackageElement(self):
        return self.packageElement

    def GetName(self):
        return self.packageElement.name

    def GetStereotypes(self):
        return self.stereotypes