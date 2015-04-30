from DomainTypes import KnownAttributes


class CStereotype(object):
    def __init__(self, stereotypeElement, extensions, tags):
        self.stereotypeElement = stereotypeElement
        self.extensions = extensions
        self.tags = tags

    def GetExtensions(self):
        for element in self.extensions:
            yield element

    def GetStereotypeElement(self):
        return self.stereotypeElement

    def GetTags(self):
        for tag in self.tags:
            yield tag

    def GetName(self):
        return self.stereotypeElement.name

    def GetIcon(self):
        return self.stereotypeElement.values[KnownAttributes.Stereotype.Icon]