from ast import literal_eval
from ProfileApplication import CProfileApplication


class CProfileApplicationExtractor(object):

    def ExtractApplications(self, packageElement):
        rawListOfProfiles = packageElement.values['applied_profiles']
        listOfProfiles = literal_eval(rawListOfProfiles)
        return [self.__CreateApplication(props) for props in listOfProfiles]

    def __CreateApplication(self, props):
        return CProfileApplication(props['package_id'], props['profile_name'], props['modification_bundle'])
