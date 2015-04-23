from ProfileManager import CProfileManager
from ProfileApplicationDiscovery import CProfileApplicationDiscovery

class CApplyProfilesTransaction(object):

    __profileManager = CProfileManager()
    __profileApplicationDiscovery = CProfileApplicationDiscovery()

    def __init__(self, projectRoot):
        self.__availableProfiles = self.__profileManager.GetAvailableProfiles(projectRoot)

        self.__profileApplications = self.__profileApplicationDiscovery.DiscoverProfileApplications(projectRoot)
        self.__currentProfiles = self.__GetAppliedProfiles(self.__profileApplications, self.__availableProfiles)

    def __GetAppliedProfiles(self, profileApplications, availableProfiles):
        return {package: self.__profileManager.GetAppliedProfiles(applications, availableProfiles)
                for package, applications in profileApplications.iteritems()}

    def GetAvailableProfiles(self):
        for profile in self.__availableProfiles.itervalues():
            yield profile

    def GetCurrentProfiles(self):
        return dict(self.__currentProfiles)

    def SetAppliedProfiles(self, profiles):
        self.__newProfiles = profiles

    def ApplyProfiles(self):
        pass