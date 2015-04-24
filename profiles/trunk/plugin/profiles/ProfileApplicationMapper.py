from ProfileApplication import CProfileApplication
from DomainTypes import KnownAttributes


class CProfileApplicationMapper(object):

    def CreateFromProperties(self, properties):
        return CProfileApplication(
            properties[KnownAttributes.ProfileApplication.PackageID],
            properties[KnownAttributes.ProfileApplication.ProfileName],
            properties[KnownAttributes.ProfileApplication.ModificationBundle])

    def ConvertToProperties(self, profileApplication):
        return {
            KnownAttributes.ProfileApplication.PackageID: profileApplication.GetProfilePackageID(),
            KnownAttributes.ProfileApplication.ProfileName: profileApplication.GetProfileName(),
            KnownAttributes.ProfileApplication.ModificationBundle: profileApplication.GetModificationBundleName()
        }