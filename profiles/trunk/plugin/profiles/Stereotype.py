class CStereotype(object):
    def __init__(self, stereotypeElement, parentStereotype=None):
        self.stereotypeElement = stereotypeElement
        self.parentStereotype = parentStereotype

    def GetStereotypeElement(self):
        return self.stereotypeElement

    def GetName(self):
        return self.stereotypeElement.GetName()