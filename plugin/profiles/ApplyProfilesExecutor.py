from ProfileManager import CProfileManager
from ProfileApplicationDiscovery import CProfileApplicationDiscovery
from AppliedProfilesDiffCalculator import CAppliedProfilesDiffCalculator


class ApplyProfilesExecutorError(Exception):
    pass


class NewProfilesNotSpecifiedError(ApplyProfilesExecutorError):
    pass


class CApplyProfilesExecutor(object):

    __profileManager = CProfileManager()
    __profileApplicationDiscovery = CProfileApplicationDiscovery()
    __appliedProfilesDiffCalculator = CAppliedProfilesDiffCalculator()

    def __init__(self, project):
        self.__project = project
        self.__availableProfiles = self.__profileManager.GetAvailableProfiles(project.root)

        self.__profileApplications = self.__profileApplicationDiscovery.DiscoverProfileApplications(project.root)
        self.__profileApplications = self.__CreateLookupForProfileApplications(self.__profileApplications)
        self.__currentProfiles = self.__GetAppliedProfiles(self.__profileApplications, self.__availableProfiles)
        self.__newProfiles = None

    @staticmethod
    def __CreateLookupForProfileApplications(profileApplications):
        return {
            package: {application.GetProfilePackageID(): application for application in applications}
            for package, applications in profileApplications.iteritems()
        }

    def __GetAppliedProfiles(self, profileApplications, availableProfiles):
        return {package: self.__profileManager.GetAppliedProfiles(applications.itervalues(), availableProfiles)
                for package, applications in profileApplications.iteritems()}

    def GetAvailableProfiles(self):
        for profile in self.__availableProfiles.itervalues():
            yield profile

    def GetCurrentProfiles(self):
        return {element: set(profiles) for element, profiles in self.__currentProfiles.iteritems()}

    def SetAppliedProfiles(self, profiles):
        self.__newProfiles = profiles

    def ApplyProfiles(self):
        if self.__newProfiles is None:
            raise NewProfilesNotSpecifiedError()

        # try:
        newProfiles, unchangedProfiles, deletedProfiles = \
            self.__appliedProfilesDiffCalculator.CalculateDiff(self.__currentProfiles, self.__newProfiles)

        deletedProfileApplications = self.__GetProfileApplications(deletedProfiles)
        self.__profileManager.RemoveProfiles(deletedProfileApplications)

        unchangedProfileApplications = self.__GetProfileApplications(unchangedProfiles)
        self.__profileManager.UpdateProfileApplications(unchangedProfileApplications, self.__availableProfiles)

        self.__profileManager.ApplyProfiles(newProfiles)
        # except Exception as error:
        #     raise ApplyProfilesExecutorError("Error occured while changing profile applications", error)

    def __GetProfileApplications(self, profilesPerElement):
        return {
            element: list(self.__GetProfileApplicationsForProfiles(self.__profileApplications[element], profiles))
            for element, profiles in profilesPerElement.iteritems()
        }

    def __GetProfileApplicationsForProfiles(self, profileApplications, profiles):
        for profile in profiles:
            if profile.GetUID() in profileApplications:
                yield profileApplications[profile.GetUID()]