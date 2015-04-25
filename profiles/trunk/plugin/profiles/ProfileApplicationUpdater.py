from ast import literal_eval
from DomainTypes import KnownAttributes
from DomainObjectHelper import AppendItemsIntoList
from ProfileApplicationMapper import CProfileApplicationMapper

def enumerate_down(l, start=None, step=-1):
    if start is None:
        start = len(l) - 1
    for index, item in zip(xrange(start, -1, step), l.__reversed__()):
        yield index, item


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

        applicationsDict = {a.GetProfilePackageID(): a for a in profileApplications}
        for index, item in enumerate_down(values):
            profilePackageID = item[KnownAttributes.ProfileApplication.PackageID]
            wasRemoved = applicationsDict.pop(profilePackageID, None)
            if wasRemoved is not None:
                path = '{0}[{1}]'.format(KnownAttributes.AppliedProfiles, index)
                element.remove_item(path)

            if len(applicationsDict) == 0:
                break