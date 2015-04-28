from DomainTypes import KnownAttributes, KnownAttributeModifications, KnownDomainTypes
from ModificationBundleObjectBuilder import CModificationBundleObjectBuilder


class CProfilePackageTransformer(object):

    def TransformPackageToModificationBundle(self, bundleName, profilePackage):
        stereotypesPerMetaclass = self.__GetStereotypesPerMetaclass(profilePackage)

        bundleBuilder = CModificationBundleObjectBuilder(bundleName)
        for extendedElement, stereotypes in stereotypesPerMetaclass.iteritems():
            # TODO: support for inherited tags

            tagAttributes = []
            appliedStereotypesEnumValues = ['']
            for stereotype in stereotypes:
                tagAttributes.extend(self.__CreateTagAttributes(stereotype))
                appliedStereotypesEnumValues.append(stereotype.GetName())

            taggedValuesDomain = KnownDomainTypes.CreateTaggedValuesDomainNameForElement(extendedElement.GetElementTypeName())
            bundleBuilder.AppendDomainModifications(taggedValuesDomain, *tagAttributes)

            appliedStereotypeDomain = KnownDomainTypes.CreateAppliedStereotypeDomainNameForElement(extendedElement.GetElementTypeName())
            appliedStereotypeDomainModification = KnownAttributeModifications.CreateStereotypeEnumModification(appliedStereotypesEnumValues)

            bundleBuilder.AppendDomainModifications(appliedStereotypeDomain, appliedStereotypeDomainModification)

            elementDomainName = extendedElement.GetElementDomain().name
            bundleBuilder.AppendDomainModifications(elementDomainName,
                KnownAttributeModifications.CreateTaggedValuesModification(taggedValuesDomain),
                KnownAttributeModifications.CreateStereotypesListModification(appliedStereotypeDomain)
            )

        return bundleBuilder.BuildBundleObject()

    @classmethod
    def __GetStereotypesPerMetaclass(cls, profilePackage):
        stereotypesPerMetaclass = {}

        for stereotype in profilePackage.GetStereotypes():
            for extension in stereotype.GetExtensions():
                stereotypesPerMetaclass.setdefault(extension.GetExtendedElement(), set()).add(stereotype)

        return stereotypesPerMetaclass

    @classmethod
    def __CreateTagAttributes(cls, stereotype):
        for tag in stereotype.GetTags():
            yield KnownAttributeModifications.CreateTagAttributeModification(stereotype, tag)