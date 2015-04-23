from ast import literal_eval
from Stereotype import CStereotype
from ProfilePackage import CProfilePackage
from Tag import CTag
from ElementTypes import KnownElementTypes
from ConnectionTypes import KnownConnectionTypes
from ExtendedElement import CExtendedElement
from Extension import CExtension


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
            extensions = self.__GetExtensions(element)
            stereotypesDict[element.uid] = CStereotype(element, extensions, tags)

        for element, stereotypeElements, childProfiles in profiles:
            packageStereotypes = [stereotypesDict[s.uid] for s in stereotypeElements]
            profile = CProfilePackage(element, packageStereotypes)
            profilePackages.append(profile)

        return profilePackages

    @staticmethod
    def __CreateTags(stereotypeElement):
        rawTagValues = literal_eval(stereotypeElement.values['tags'])
        return [CTag(rawTag['name'], rawTag['type']) for rawTag in rawTagValues]

    @classmethod
    def __GetExtensions(cls, stereotypeElement):
        extensions = {}
        for connection in stereotypeElement.connections:
            otherElement = connection.get_connected_object(stereotypeElement)
            if KnownConnectionTypes.IsExtension(connection):
                extendedElement = cls.__CreateExtendedElement(otherElement)
                extension = CExtension(extendedElement)
                extensions[otherElement] = extension

        return extensions.values()


    @classmethod
    def __CreateExtendedElement(cls, metaclassElement):
        elementTypeName = metaclassElement.values['metaclass_name']
        elementType = metaclassElement.type.metamodel.elements[elementTypeName]
        return CExtendedElement(elementType)
