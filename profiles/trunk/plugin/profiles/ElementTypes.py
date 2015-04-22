class KnownElementTypes:
    StereotypeType = 'Stereotype'
    PackageType = 'Package'

    @classmethod
    def IsStereotype(cls, element):
        return element.type.name == cls.StereotypeType

    @classmethod
    def IsPackage(cls, element):
        return element.type.name == cls.PackageType