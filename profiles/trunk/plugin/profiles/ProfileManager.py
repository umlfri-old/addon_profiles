from ProfilePackageProcessor import CProfilePackageProcessor
from ProfileApplicationExtractor import CProfileApplicationExtractor
from ElementTypes import KnownElementTypes


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()
    __profileApplicationExtractor = CProfileApplicationExtractor()

    def GetAvailableProfiles(self, packageElement):
        profilePackages = self.__profilePackageProcessor.ProcessPackage(packageElement)
        return {p.GetUID(): p for p in profilePackages}

    def GetAppliedProfiles(self, package, availableProfiles):
        applications = self.__profileApplicationExtractor.ExtractApplications(package)

        appliedProfiles = []
        for application in applications:
            if application.GetProfilePackageID() in availableProfiles:
                appliedProfiles.append(availableProfiles[application.GetProfilePackageID()])
            else:
                appliedProfiles.append(application.GetProfileName())

        return appliedProfiles

    def IsPackage(self, element):
        return element.type.name == KnownElementTypes.PackageType