from ProfilePackageProcessor import CProfilePackageProcessor


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()

    def GetAvailableProfiles(self, packageElement):
        profilePackages = self.__profilePackageProcessor.ProcessPackage(packageElement)
        return profilePackages