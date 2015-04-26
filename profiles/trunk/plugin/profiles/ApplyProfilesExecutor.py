from ProfileManager import CProfileManager
from ProfileApplicationDiscovery import CProfileApplicationDiscovery
from AppliedProfilesDiffCalculator import CAppliedProfilesDiffCalculator


class ApplyProfilesExecutorError(Exception):

    def GetMessage(self):
        if self.message:
            return self.message
        if len(self.args) > 0:
            return self.args[-1]
        else:
            return ''

    def GetInnerException(self):
        if len(self.args) == 0:
            return None
        else:
            return self.args[0]

    def GetInnerExceptionMessage(self):
        innerException = self.GetInnerException()
        if innerException is None:
            return self.GetMessage()

        return repr(innerException)


class NewProfilesNotSpecifiedError(ApplyProfilesExecutorError):
    message = 'New profiles not specified, there is nothing to apply'


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
        self.__orphanedProfileApplications = self.__GetOrphanedProfileApplications(self.__currentProfiles)
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

    @staticmethod
    def __GetOrphanedProfileApplications(appliedProfiles):
        return {package: [p for p in profiles if p.IsOrphaned()]
            for package, profiles in appliedProfiles.iteritems()}

    def GetAvailableProfiles(self):
        for profile in self.__availableProfiles.itervalues():
            yield profile

    def GetCurrentProfiles(self):
        return {element: set(profiles) for element, profiles in self.__currentProfiles.iteritems()}

    def GetOrphanedProfileApplications(self):
        return self.__orphanedProfileApplications

    def SetAppliedProfiles(self, profiles):
        self.__newProfiles = profiles

    def ApplyProfiles(self):
        if self.__newProfiles is None:
            raise NewProfilesNotSpecifiedError()

        try:
            newProfiles, unchangedProfiles, deletedProfiles = \
                self.__appliedProfilesDiffCalculator.CalculateDiff(self.__currentProfiles, self.__newProfiles)

            deletedProfileApplications = self.__GetProfileApplications(deletedProfiles)
            self.__profileManager.RemoveProfiles(deletedProfileApplications)

            unchangedProfileApplications = self.__GetProfileApplications(unchangedProfiles)
            self.__profileManager.UpdateProfileApplications(unchangedProfileApplications, self.__availableProfiles)

            self.__profileManager.ApplyProfiles(newProfiles)

            self.__profileManager.UpdateStereotypeIconMappings(self.__project, self.__newProfiles)
        except Exception as error:
            raise ApplyProfilesExecutorError(error, "Error occurred while changing profile applications")

    def __GetProfileApplications(self, profilesPerElement):
        return {
            element: list(self.__GetProfileApplicationsForProfiles(self.__profileApplications[element], profiles))
            for element, profiles in profilesPerElement.iteritems()
        }

    def __GetProfileApplicationsForProfiles(self, profileApplications, profiles):
        for profile in profiles:
            if profile.GetUID() in profileApplications:
                yield profileApplications[profile.GetUID()]