from ProfilePackageProcessor import CProfilePackageProcessor


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()

    def GetAvailableProfiles(self, packageElement):
        profilePackages = self.__profilePackageProcessor.ProcessPackage(packageElement)
        return {p.GetUID(): p for p in profilePackages}

    def GetAppliedProfiles(self, profileApplications, availableProfiles):
        appliedProfiles = []
        
        for application in profileApplications:
            if application.GetProfilePackageID() in availableProfiles:
                appliedProfiles.append(availableProfiles[application.GetProfilePackageID()])
            else:
                appliedProfiles.append(application.GetProfileName())

        return appliedProfiles