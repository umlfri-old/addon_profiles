class CStereotype(object):
    def __init__(self, stereotypeElement, extensions, tags, parentStereotype=None):
        self.stereotypeElement = stereotypeElement
        self.extensions = extensions
        self.tags = tags
        self.parentStereotype = parentStereotype

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