from ast import literal_eval
from ProfileApplication import CProfileApplication
from DomainTypes import KnownAttributes


class CProfileApplicationExtractor(object):

    def ExtractApplications(self, packageElement):
        rawListOfProfiles = packageElement.values[KnownAttributes.AppliedProfiles]
        listOfProfiles = literal_eval(rawListOfProfiles)
        return [self.__CreateApplication(props) for props in listOfProfiles]

    def __CreateApplication(self, props):
        return CProfileApplication(
            props[KnownAttributes.ProfileApplication.PackageID],
            props[KnownAttributes.ProfileApplication.ProfileName],
            props[KnownAttributes.ProfileApplication.ModificationBundle])
