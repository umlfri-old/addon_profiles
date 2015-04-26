class COrphanedProfilePackage(object):

    def __init__(self, profileApplication):
        self.profileApplication = profileApplication

    def GetUID(self):
        return self.profileApplication.GetProfilePackageID()

    def IsOrphaned(self):
        return True

    def GetName(self):
        return self.profileApplication.GetProfileName()

    def GetProfileApplication(self):
        return self.profileApplication