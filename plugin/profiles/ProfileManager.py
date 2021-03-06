from ProfilePackageProcessor import CProfilePackageProcessor
from OrphanedProfilePackage import COrphanedProfilePackage
from ProfilePackageTransformer import CProfilePackageTransformer
from ProfileApplicationUpdater import CProfileApplicationUpdater
from ProfileApplication import CProfileApplication
from StereotypeIconMappingListUpdater import CStereotypeIconMappingListUpdater


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()
    __profilePackageTransformer = CProfilePackageTransformer()
    __profileApplicationUpdater = CProfileApplicationUpdater()
    __stereotypeIconMappingListUpdater = CStereotypeIconMappingListUpdater()

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
            self.__profileApplicationUpdater.RemoveProfileApplications(element, applications)

    def UpdateProfileApplications(self, profileApplications, profiles):
        self.RemoveProfiles(profileApplications)

        elementProfiles = {}
        for element, applications in profileApplications.iteritems():
            appliedProfiles = [profiles[application.GetProfilePackageID()] for application in applications]
            elementProfiles[element] = appliedProfiles

        self.ApplyProfiles(elementProfiles)

    def ApplyProfiles(self, elementProfiles):
        for element, profiles in elementProfiles.iteritems():
            bundles = []
            profileApplications = []
            for profile in profiles:
                modificationBundleName = self.__CreateProfileApplicationBundleName(element, profile.GetPackageElement())
                profileApplicationBundle = self.__profilePackageTransformer.TransformPackageToModificationBundle(
                    modificationBundleName, profile)

                bundles.append(profileApplicationBundle)

                profileApplication = self.__CreateProfileApplication(modificationBundleName, profile)
                profileApplications.append(profileApplication)

            element.modify_metamodel(bundles)
            self.__profileApplicationUpdater.AddProfileApplications(element, profileApplications)

    def UpdateStereotypeIconMappings(self, project, appliedProfiles):
        stereotypes = {}
        for profiles in appliedProfiles.itervalues():
            for profile in profiles:
                for stereotype in profile.GetStereotypes():
                    stereotypes[stereotype.GetName()] = stereotype

        self.__stereotypeIconMappingListUpdater.UpdateIconList(project, stereotypes.values())

    @classmethod
    def __CreateProfileApplicationBundleName(cls, packageElement, profileElement):
        return 'profile_application_{0}_{1}'.format(packageElement.__id__, profileElement.__id__)

    @classmethod
    def __CreateProfileApplication(cls, modificationBundleName, profile):
        return CProfileApplication(profile.GetPackageElement().__id__, profile.GetName(), modificationBundleName)

