from DomainTypes import KnownAttributes
from DomainObjectHelper import AppendItemsIntoList
from ProfileApplicationMapper import CProfileApplicationMapper


class CProfileApplicationUpdater(object):

    __profileApplicationMapper = CProfileApplicationMapper()

    def AddProfileApplications(self, element, profileApplications):
        items = [self.__profileApplicationMapper.ConvertToProperties(a) for a in profileApplications]
        AppendItemsIntoList(element, KnownAttributes.AppliedProfiles, items)
