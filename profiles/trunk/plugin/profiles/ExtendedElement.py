class CExtendedElement(object):
    def __init__(self, elementType):
        self.elementType = elementType
        self.elementTypeName = self.elementType.name

    def GetElementType(self):
        return self.elementType

    def GetElementTypeName(self):
        return  self.elementTypeName

    def GetElementDomain(self):
        return self.elementType.domain

    def __hash__(self):
        return self.elementTypeName.__hash__()

    def __cmp__(self, other):
        if other is None:
            return -1
        return self.elementTypeName.__cmp__(other.elementTypeName)

    def __eq__(self, other):
        if other is None:
            return False
        return self.elementTypeName == other.elementTypeName

    def __ne__(self, other):
        return not self.__eq__(other)