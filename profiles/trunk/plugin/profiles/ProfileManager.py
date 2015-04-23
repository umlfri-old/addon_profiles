from ProfilePackageProcessor import CProfilePackageProcessor
from OrphanedProfilePackage import COrphanedProfilePackage


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()

    def GetAvailableProfiles(self, packageElement):
        profilePackages = self.__profilePackageProcessor.ProcessPackage(packageElement)
        return {p.GetUID(): p for p in profilePackages}

    def GetAppliedProfiles(self, profileApplications, availableProfiles):
        appliedProfiles = set()
        
        for application in profileApplications:
            if application.GetProfilePackageID() in availableProfiles:
                appliedProfiles.add(availableProfiles[application.GetProfilePackageID()])
            else:
                appliedProfiles.add(COrphanedProfilePackage(application))

        return appliedProfiles