from ast import literal_eval
from DomainTypes import KnownAttributes
from DomainObjectHelper import AppendItemsIntoList
from ProfileApplicationMapper import CProfileApplicationMapper


class ProfileApplicationNotFound(Exception):
    def __init__(self, profileApplication):
        self.profileApplication = profileApplication


class CProfileApplicationUpdater(object):

    __profileApplicationMapper = CProfileApplicationMapper()

    def AddProfileApplications(self, element, profileApplications):
        items = [self.__profileApplicationMapper.ConvertToProperties(a) for a in profileApplications]
        AppendItemsIntoList(element, KnownAttributes.AppliedProfiles, items)

    def RemoveProfileApplications(self, element, profileApplications):
        values = literal_eval(element.values[KnownAttributes.AppliedProfiles])
        indexes = self.__FindIndexes(values, profileApplications)
        indexes = sorted(indexes, key=lambda x: x[0], reverse=True)
        for index, application in indexes:
            path = '{0}[{1}]'.format(KnownAttributes.AppliedProfiles, index)
            element.remove_item(path)

    def __FindIndexes(self, values, profileApplications):
        for index, item in enumerate(values):
            application = self.__GetProfileApplication(item, profileApplications)
            if application is None:
                raise ProfileApplicationNotFound(application)

            yield index, application

    def __GetProfileApplication(self, item, profileApplications):
        for application in profileApplications:
            if item[KnownAttributes.ProfileApplication.PackageID] == application.GetProfilePackageID():
                return application