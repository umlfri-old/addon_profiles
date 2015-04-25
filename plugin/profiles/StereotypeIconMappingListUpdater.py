from DomainObjectHelper import RemoveAllItemsFromList
from DomainTypes import KnownAttributes
from StereotypeIcons import stereotypeIconFileMappings
from DomainObjectHelper import AppendItemsIntoList


class CStereotypeIconMappingListUpdater(object):

    def UpdateIconList(self, project, stereotypes):
        RemoveAllItemsFromList(project, KnownAttributes.StereotypeIconFileMappings)
        mappings = self.__CreateStereotypeIconMappings(stereotypes)
        AppendItemsIntoList(project, KnownAttributes.StereotypeIconFileMappings, mappings)


    def __CreateStereotypeIconMappings(self, stereotypes):
        mappings = []

        for s in stereotypes:
            icon = s.GetIcon()
            if icon != 'None':
                filename = stereotypeIconFileMappings[icon]
                mapping = {
                    KnownAttributes.StereotypeIconFileMapping.Stereotype: s.GetName(),
                    KnownAttributes.StereotypeIconFileMapping.Filename: filename
                }
                mappings.append(mapping)

        return mappings
