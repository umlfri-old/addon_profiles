from DomainTypes import KnownAttributes, KnownAttributeModifications, KnownDomainTypes
from ProfilePackageTransformation import CProfilePackageTransformation


class CProfilePackageTransformer(object):

    def TransformPackageToModificationBundle(self, profilePackage):
        stereotypesPerMetaclass = self.__GetStereotypesPerMetaclass(profilePackage)

        tagAttributesBundle = {}
        taggedValuesAndStereotypesBundle = {}
        for extendedElement, stereotypes in stereotypesPerMetaclass.iteritems():
            # TODO: support for inherited tags

            tagAttributes = []
            appliedStereotypesEnumValues = []
            for stereotype in stereotypes:
                tagAttributes.extend(self.__CreateTagAttributes(stereotype))
                appliedStereotypesEnumValues.append(stereotype.GetName())

            taggedValuesDomain = KnownDomainTypes.CreateTaggedValuesDomainNameForElement(extendedElement.GetElementTypeName())
            tagAttributesBundle[taggedValuesDomain] = tagAttributes

            appliedStereotypeDomain = KnownDomainTypes.CreateAppliedStereotypeDomainNameForElement(extendedElement.GetElementTypeName())
            appliedStereotypeDomainModification = KnownAttributeModifications.CreateStereotypeEnumModification(appliedStereotypesEnumValues)

            taggedValuesAndStereotypesBundle[appliedStereotypeDomain] = [appliedStereotypeDomainModification]
            taggedValuesAndStereotypesBundle[extendedElement.GetElementDomain().name] = [
                KnownAttributeModifications.CreateTaggedValuesModification(taggedValuesDomain),
                KnownAttributeModifications.CreateStereotypesListModification(appliedStereotypeDomain)
            ]

        extendedElements = stereotypesPerMetaclass.keys()
        return CProfilePackageTransformation(tagAttributesBundle, taggedValuesAndStereotypesBundle, extendedElements)

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