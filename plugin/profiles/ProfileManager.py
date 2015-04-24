from ProfilePackageProcessor import CProfilePackageProcessor
from OrphanedProfilePackage import COrphanedProfilePackage
from ProfilePackageTransformer import CProfilePackageTransformer
from ProfileApplicationUpdater import CProfileApplicationUpdater
from ProfileApplication import CProfileApplication


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()
    __profilePackageTransformer = CProfilePackageTransformer()
    __profileApplicationUpdater = CProfileApplicationUpdater()

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

    def RemoveProfiles(self, profileApplications):
        for element, applications in profileApplications.iteritems():
            bundles = [a.GetModificationBundleName() for a in applications]
            element.revert_modifications(bundles)

    def UpdateProfileApplications(self, profileApplications, profiles):
        self.RemoveProfiles(profileApplications)

        elementProfiles = {}
        for element, applications in profileApplications.iteritems():
            appliedProfiles = [profiles[application.GetProfilePackageID()] for application in applications]
            elementProfiles[element] = appliedProfiles

        self.ApplyProfiles(elementProfiles)

    def ApplyProfiles(self, elementProfiles):
        for element, profiles in elementProfiles.iteritems():
            bundles = {}
            profileApplications = []
            for profile in profiles:
                modificationBundle = self.__profilePackageTransformer.TransformPackageToModificationBundle(profile)
                modificationBundleName = self.__CreateProfileApplicationBundleName(element, profile.GetPackageElement())
                profileApplicationBundle = (
                    modificationBundleName,
                    modificationBundle
                )

                bundles.update(dict([profileApplicationBundle]))

                profileApplication = self.__CreateProfileApplication(modificationBundleName, profile)
                profileApplications.append(profileApplication)

            element.modify_metamodel(bundles)
            self.__profileApplicationUpdater.AddProfileApplications(element, profileApplications)

    @classmethod
    def __CreateProfileApplicationBundleName(cls, packageElement, profileElement):
        return 'profile_application_{0}_{1}'.format(packageElement.uid, profileElement.uid)

    @classmethod
    def __CreateProfileApplication(cls, modificationBundleName, profile):
        return CProfileApplication(profile.GetPackageElement().uid, profile.GetName(), modificationBundleName)

