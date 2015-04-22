class CStereotype(object):
    def __init__(self, stereotypeElement, tags, parentStereotype=None):
        self.stereotypeElement = stereotypeElement
        self.tags = tags
        self.parentStereotype = parentStereotype

    def GetStereotypeElement(self):
        return self.stereotypeElement

    def GetTags(self):
        for tag in self.tags:
            yield tag

    def GetName(self):
        return self.stereotypeElement.name