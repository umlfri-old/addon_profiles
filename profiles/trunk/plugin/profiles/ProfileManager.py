from ProfilePackageProcessor import CProfilePackageProcessor
from OrphanedProfilePackage import COrphanedProfilePackage
from ProfilePackageTransformer import CProfilePackageTransformer
from DomainTypes import KnownAttributes
from DomainObjectHelper import AppendItemsIntoList


class CProfileManager(object):

    __profilePackageProcessor = CProfilePackageProcessor()
    __profilePackageTransformer = CProfilePackageTransformer()

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
                transformation = self.__profilePackageTransformer.TransformPackageToModificationBundle(profile)
                modificationBundleName = self.__CreateProfileApplicationBundleName(element, profile.GetPackageElement())
                profileApplicationBundle = (
                    modificationBundleName,
                    transformation.GetTagAttributesBundle()
                )

                miscBundle = (
                    modificationBundleName + '_misc',
                    transformation.GetTaggedValuesAndStereotypesBundle()
                )
                bundles.update(dict([profileApplicationBundle, miscBundle]))

                profileApplication = self.__CreateProfileApplicationProperties(modificationBundleName, profile)
                profileApplications.append(profileApplication)

            element.modify_metamodel(bundles)
            self.__AddProfileApplications(element, profileApplications)

    @classmethod
    def __CreateProfileApplicationBundleName(cls, packageElement, profileElement):
        return 'profile_application_{0}_{1}'.format(packageElement.uid, profileElement.uid)

    @classmethod
    def __CreateProfileApplicationProperties(cls, modificationBundleName, profile):
        # return CProfileApplication(profile.GetPackageElement().uid, profile.GetName(), modificationBundleName)
        return {
            KnownAttributes.ProfileApplication.PackageID: profile.GetPackageElement().uid,
            KnownAttributes.ProfileApplication.ProfileName: profile.GetName(),
            KnownAttributes.ProfileApplication.ModificationBundle: modificationBundleName
        }

    @classmethod
    def __AddProfileApplications(cls, element, profileApplications):
        AppendItemsIntoList(element, KnownAttributes.AppliedProfiles, profileApplications)