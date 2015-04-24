from ast import literal_eval
from DomainTypes import KnownAttributes
from ProfileApplicationMapper import CProfileApplicationMapper


class CProfileApplicationExtractor(object):

    __profileApplicationMapper = CProfileApplicationMapper()

    def ExtractApplications(self, packageElement):
        rawListOfProfiles = packageElement.values[KnownAttributes.AppliedProfiles]
        listOfProfiles = literal_eval(rawListOfProfiles)
        return [self.__profileApplicationMapper.CreateFromProperties(props) for props in listOfProfiles]