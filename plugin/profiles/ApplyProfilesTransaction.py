from ProfileManager import CProfileManager
from ProfileApplicationDiscovery import CProfileApplicationDiscovery
from AppliedProfilesDiffCalculator import CAppliedProfilesDiffCalculator


class ApplyProfilesTransactionError(Exception):
    pass


class NewProfilesNotSpecifiedError(ApplyProfilesTransactionError):
    pass


class CApplyProfilesTransaction(object):

    __profileManager = CProfileManager()
    __profileApplicationDiscovery = CProfileApplicationDiscovery()
    __appliedProfilesDiffCalculator = CAppliedProfilesDiffCalculator()

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
        if self.__newProfiles is None:
            raise NewProfilesNotSpecifiedError()

        try:
            newProfiles, unchangedProfiles, deletedProfiles = \
                self.__appliedProfilesDiffCalculator.CalculateDiff(self.__currentProfiles, self.__newProfiles)

            deletedProfileApplications = {self.__profileApplications[None] for element in deletedProfiles.iterkeys()}
            self.__profileManager.RemoveProfiles(deletedProfileApplications)

            unchangedProfileApplications = {self.__profileApplications[element] for element in unchangedProfiles.iterkeys()}
            self.__profileManager.UpdateProfileApplications(unchangedProfileApplications, self.__availableProfiles)

            self.__profileManager.ApplyProfiles(newProfiles)
        except (RuntimeError, TypeError) as error:
            raise ApplyProfilesTransactionError("Error occured while changing profile applications", error)