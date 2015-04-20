from Stereotype import CStereotype
from ProfilePackage import CProfilePackage


class CProfilePackageProcessor(object):

    StereotypeType = 'Stereotype'
    PackageType = 'Package'

    def ProcessPackage(self, element):
        profiles = []
        stereotypes = []
        self.__DiscoverProfiles(element, profiles, stereotypes)
        self.__CreateProfilePackages(profiles, stereotypes)

    def __DiscoverProfiles(self, element, profiles, stereotypes):
        packageStereotypes = []
        childProfiles = []

        for child in element.children:
            childType = child.type.name
            if childType == self.PackageType:
                self.__DiscoverProfiles(child, profiles, stereotypes)
                childProfiles.append(child)
            elif childType == self.StereotypeType:
                stereotypes.append(element)
                packageStereotypes.append(child)

        profiles.append((element, packageStereotypes, childProfiles))

    def __CreateProfilePackages(self, profiles, stereotypes):
        stereotypesDict = {}
        profilePackages = []

        for element in stereotypes:
            stereotypesDict[element] = CStereotype(element)

        for element, stereotypeElements, childProfiles in profiles:
            packageStereotypes = [stereotypesDict[s] for s in stereotypeElements]
            profile = CProfilePackage(element, packageStereotypes)
            profilePackages.append(profile)

        return profilePackages