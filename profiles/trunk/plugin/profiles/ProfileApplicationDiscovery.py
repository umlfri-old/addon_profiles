from ProfileApplicationExtractor import CProfileApplicationExtractor
from ElementTypes import KnownElementTypes


class CProfileApplicationDiscovery(object):

    __profileApplicationExtractor = CProfileApplicationExtractor()

    @classmethod
    def DiscoverProfileApplications(cls, element, searchChildren=True):
        projectTree = {}

        elements = [element]

        while len(elements) > 0:
            element = elements.pop()

            if KnownElementTypes.IsPackage(element):
                profileApplications = cls.__profileApplicationExtractor.ExtractApplications(element)
                if len(profileApplications) > 0:
                    projectTree[element] = profileApplications

            if searchChildren:
                elements.extend(element.children)

        return projectTree