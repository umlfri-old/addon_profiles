class CModificationBundleObjectBuilder(object):
    def __init__(self, name):
        self.name = name
        self.domainModifications = {}

    def AppendDomainModifications(self, domainName, *modifications):
        self.__GetDomainModifications(domainName).extend(modifications)

    def __GetDomainModifications(self, domainName):
        return self.domainModifications.setdefault(domainName, [])

    def BuildBundleObject(self):
        domainModificationsList = []

        for domain, modifications in self.domainModifications.iteritems():
            domainModificationsObject = {
                'name': domain,
                'modifications': modifications
            }
            domainModificationsList.append(domainModificationsObject)

        return {
            'name': self.name,
            'modifications': domainModificationsList
        }