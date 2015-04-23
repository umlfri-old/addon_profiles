class CExtendedElement(object):
    def __init__(self, elementType):
        self.elementType = elementType

    def GetElementType(self):
        return self.elementType

    def GetElementDomain(self):
        return self.elementType.domain