from ProfileManager import CProfileManager
from ProfileApplicationDiscovery import CProfileApplicationDiscovery
from gui import CProfileListDialog


class CAppliedProfileEditor(object):

    __profileManager = CProfileManager()
    __profileApplicationDiscovery = CProfileApplicationDiscovery()

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        projectRoot = self.__interface.project.root
        availableProfiles = self.__profileManager.GetAvailableProfiles(projectRoot)

        profileApplications = self.__profileApplicationDiscovery.DiscoverProfileApplications(projectRoot)
        appliedProfiles = self.__GetAppliedProfiles(profileApplications, availableProfiles)

        CProfileListDialog(projectRoot, dict(appliedProfiles), availableProfiles.itervalues()).Show()

    def __GetAppliedProfiles(self, profileApplications, availableProfiles):
        return {package: self.__profileManager.GetAppliedProfiles(applications, availableProfiles)
                for package, applications in profileApplications.iteritems()}