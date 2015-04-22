from ProfilePackageProcessor import CProfilePackageProcessor


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()

    def GetAvailableProfiles(self, packageElement):
        profilePackages = self.__profilePackageProcessor.ProcessPackage(packageElement)
        return {p.GetUID(): p for p in profilePackages}

    def IsPackage(self, element):
        return element.type.name == KnownElementTypes.PackageType