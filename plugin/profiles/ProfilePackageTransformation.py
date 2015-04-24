class CProfilePackageTransformation(object):

    def __init__(self, tagAttributesBundle, taggedValuesAndStereotypesBundle, extendedElements):
        self.tagAttributesBundle = tagAttributesBundle
        self.taggedValuesAndStereotypesBundle = taggedValuesAndStereotypesBundle
        self.extendedElements = extendedElements

    def GetTagAttributesBundle(self):
        return self.tagAttributesBundle

    def GetTaggedValuesAndStereotypesBundle(self):
        return self.taggedValuesAndStereotypesBundle
