from ast import literal_eval
from Stereotype import CStereotype
from ProfilePackage import CProfilePackage
from Tag import CTag
from ElementTypes import KnownElementTypes


class CProfilePackageProcessor(object):

    def ProcessPackage(self, element):
        profiles = []
        stereotypes = []
        self.__DiscoverProfiles(element, profiles, stereotypes)
        return self.__CreateProfilePackages(profiles, stereotypes)

    def __DiscoverProfiles(self, element, profiles, stereotypes):
        packageStereotypes = []
        childProfiles = []

        for child in element.children:
            if KnownElementTypes.IsPackage(child):
                self.__DiscoverProfiles(child, profiles, stereotypes)
                childProfiles.append(child)
            elif KnownElementTypes.IsStereotype(child):
                stereotypes.append(child)
                packageStereotypes.append(child)

        if KnownElementTypes.IsPackage(element) and len(packageStereotypes) > 0:
            profiles.append((element, packageStereotypes, childProfiles))

    def __CreateProfilePackages(self, profiles, stereotypes):
        stereotypesDict = {}
        profilePackages = []

        for element in stereotypes:
            tags = self.__CreateTags(element)
            stereotypesDict[element.uid] = CStereotype(element, tags)

        for element, stereotypeElements, childProfiles in profiles:
            packageStereotypes = [stereotypesDict[s.uid] for s in stereotypeElements]
            profile = CProfilePackage(element, packageStereotypes)
            profilePackages.append(profile)

        return profilePackages

    @staticmethod
    def __CreateTags(stereotypeElement):
        rawTagValues = literal_eval(stereotypeElement.values['tags'])
        return [CTag(rawTag['name'], rawTag['type']) for rawTag in rawTagValues]