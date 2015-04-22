class CProfileApplication(object):

    def __init__(self, profilePackageID, profileName, modificationBundleName):
        self.profilePackageID = profilePackageID
        self.profileName = profileName
        self.modificationBundleName = modificationBundleName

    def GetProfilePackageID(self):
        return self.profilePackageID

    def GetProfileName(self):
        return self.profileName

    def GetModificationBundleName(self):
        return self.modificationBundleName