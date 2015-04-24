from ProfilePackageProcessor import CProfilePackageProcessor
from OrphanedProfilePackage import COrphanedProfilePackage
from ProfilePackageTransformer import CProfilePackageTransformer


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
        pass

    def ApplyProfiles(self, elementProfiles):
        for element, profiles in elementProfiles.iteritems():
            bundles = {}
            for profile in profiles:
                transformation = self.__profilePackageTransformer.TransformPackageToModificationBundle(profile)
                profileApplicationBundle = (
                    self.__CreateProfileApplicationBundleName(element, profile.GetPackageElement()),
                    transformation.GetTagAttributesBundle()
                )

                miscBundle = (
                    profileApplicationBundle[0] + '_misc',
                    transformation.GetTaggedValuesAndStereotypesBundle()
                )
                bundles.update(dict([profileApplicationBundle, miscBundle]))

            element.modify_metamodel(bundles)


    @classmethod
    def __CreateProfileApplicationBundleName(cls, packageElement, profileElement):
        return 'profile_application_{0}_{1}'.format(packageElement.uid, profileElement.uid)