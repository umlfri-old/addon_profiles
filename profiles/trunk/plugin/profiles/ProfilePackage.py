class CProfilePackage(object):
    def __init__(self, packageElement, stereotypes = None):
        self.packageElement = packageElement
        self.stereotypes = stereotypes or []
        self.childProfiles = []

    def GetUID(self):
        return self.packageElement.uid

    def GetPackageElement(self):
        return self.packageElement

    def GetName(self):
        return self.packageElement.name

    def GetStereotypes(self):
        return self.stereotypes

    def AddChildProfile(self, profilePackage):
        self.childProfiles.append(profilePackage)

    def GetChildProfiles(self):
        for profile in self.childProfiles:
            yield profile