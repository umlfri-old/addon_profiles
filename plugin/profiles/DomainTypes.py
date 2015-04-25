class KnownDomainTypes:
    TaggedValues = 'tagged_values'
    TaggedValuesElementDomainTemplate = '{0}_{1}'.format('{0}', TaggedValues)

    AppliedStereotype = 'applied_stereotypes'
    AppliedStereotypeElementDomainTemplate = '{0}.{1}'.format('{0}', AppliedStereotype)

    @classmethod
    def CreateTaggedValuesDomainNameForElement(cls, elementName):
        return cls.TaggedValuesElementDomainTemplate.format(elementName.lower())

    @classmethod
    def CreateAppliedStereotypeDomainNameForElement(cls, elementName):
        return cls.AppliedStereotypeElementDomainTemplate.format(elementName.lower())

class KnownAttributes:
    TaggedValues = 'tagged_values'
    AppliedStereotypes = 'applied_stereotypes'
    AppliedStereotypeName = 'stereotype'

    AppliedProfiles = 'applied_profiles'

    class ProfileApplication:
        PackageID = 'package_id'
        ProfileName = 'profile_name'
        ModificationBundle = 'modification_bundle'


class KnownAttributeModifications:
    @classmethod
    def CreateTagAttributeModification(cls, stereotype, tag):
        stereotypeName = stereotype.GetName()
        return {
            'modification_type': 'replace',
            'attribute_id': '{0}_{1}'.format(stereotypeName.lower(), tag.GetName().lower()),
            'attribute_properties': {
                'name': tag.GetName(),
                'type': tag.GetType(),
                'condition': '#any(True for s in self._Parent.applied_stereotypes if s.stereotype == "{0}")'.format(stereotypeName)
            }
        }

    @classmethod
    def CreateTaggedValuesModification(cls, domainName):
        return {
            'modification_type': 'replace',
            'attribute_id': KnownAttributes.TaggedValues,
            'attribute_properties': {
                'name': 'Tagged values',
                'type': domainName
            }
        }

    @classmethod
    def CreateStereotypesListModification(cls, domainName):
        return {
            'modification_type': 'replace',
            'attribute_id': KnownAttributes.AppliedStereotypes,
            'attribute_properties': {
                'name': 'Applied stereotypes',
                'type': 'list',
                'list': {
                    'type': domainName
                },
            }
        }

    @classmethod
    def CreateStereotypeEnumModification(cls, stereotypeEnumValues):
        return {
            'modification_type': 'replace',
            'attribute_id': KnownAttributes.AppliedStereotypeName,
            'attribute_properties': {
                'name': 'Stereotype',
                'type': 'enum',
                'enum': stereotypeEnumValues
            }
        }