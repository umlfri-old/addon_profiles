class COrphanedProfilePackage(object):

    def __init__(self, profileApplication):
        self.profileApplication = profileApplication

    def IsOrphaned(self):
        return True

    def GetName(self):
        return self.profileApplication.GetProfileName()

    def GetProfileApplication(self):
        return self.profileApplication